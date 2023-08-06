"""Offer a scaffolding wizard that can be used to start a new
chart from a template.

Using ScaffoldingWizard, you can define a set of "scaffolding components"
that people can include. These should typically be 'chart features' that you want
people to allow composing their templates from. These components will be loaded from
$scaffold_dir/_wizard/*.yaml.

Once the components have been picked, the content of $scaffold_dir/_skel are copied over
to the new chart directory. Any file under templates/*.skel will be processed using the
components described above as follows:
when a line in the skeleton template only contains '# replace: <label>', that line will
be substituted with the contents of the scaffolding components that were selected earlier
corresponding to that label, in order of component priority.

Finally, based on a $scaffold_dir/questions.yaml file, we get labels and questions to ask
the user, and then substitute any occurrence of "__label__" in values.yaml from the
skeleton with the user inputs.
"""
import argparse
import json
import pathlib
import re
import shutil
import textwrap
from typing import Optional

import yaml
from wmflib import interactive

from sextant import DEPFILE, log


class Component:
    """Generic scaffolding component container"""

    # pylint: disable=too-many-instance-attributes
    indent_re = re.compile(r"(\{\{\-\s*include.*?)(\-?\}\})")

    def __init__(self, path: pathlib.Path):
        """Loads the scaffolding component.

        Arguments:
            path (pathlib.Path): the path to the yaml file for the component.
        """
        with path.open("r") as yamlfile:
            values = yaml.safe_load(yamlfile)
        self.name = values["name"]
        self.description = values.get("description", f"Scaffold for {self.name}")
        self.modules: list[str] = values.get("modules", [])
        self.priority: int = values.get("priority", 99)
        self.templates: dict[str, str] = values.get("templates", {})
        self.values: str = values.get("values", "")
        self.conflicts: list[str] = values.get("conflicts", [])
        self.questions: list[str] = values.get("questions", [])

    def pprint(self):
        """Pretty-print information about this scaffolding component."""
        print(f"* {self.name}")
        for line in textwrap.wrap(self.description, 70):
            print(f"  {line}")

    def template_for(self, label: str, indent: int = 0) -> list[str]:
        """Get the template bit for the given label, if available."""
        tpl = self.templates.get(label, "")
        if tpl == "":
            return []
        lines = tpl.splitlines()
        # If an indent value is provided, add it to the start of each line as whitespace,
        # the add the | indent N to any include that removes trailing whitespace.
        if indent:
            return [" " * indent + self.indent_re.sub(rf"\1| indent {indent} \2", line) for line in lines]

        return lines

    def is_compatible_with(self, other: "Component") -> bool:
        """Verify if this component is compatible with another one."""
        if other.name in self.conflicts or self.name in other.conflicts:
            return False
        return True


class Answers:
    """Class that encapsulates loading components and answers, either from a presets file or from cli."""

    def __init__(self, available_components: list[Component], preset_file: Optional[pathlib.Path]):
        """Read answers and components from a preset file, if present"""
        self.components: list[Component] = []
        self.responses: dict[str, str] = {}
        self.available_components = available_components
        self.presets = argparse.Namespace(components=[], responses={})
        if preset_file is not None and preset_file.is_file():
            data = yaml.safe_load(preset_file.read_text())
            if "components" in data:
                self.presets.components.extend(data["components"])
            if "responses" in data:
                self.presets.responses = data["responses"]

    def get_components(self) -> list[Component]:
        """Return the list of components selected"""
        if self.presets.components:
            for compname in self.presets.components:
                self._select(compname)
        else:
            do_exit = False
            while do_exit is False:
                all_names = [m.name for m in self.available_components]
                print("===> Available components:")
                for mod in self.available_components:
                    print("")
                    mod.pprint()
                if self.components:
                    print(f"Already selected: {','.join([m.name for m in self.components])}")

                modname = interactive.ask_input("Please select a component by name (q to quit)", all_names + ["q"])
                if modname == "q":
                    do_exit = True
                    continue
                self._select(modname)
                if len(self.available_components) == 0:
                    do_exit = True
        return self.components

    def get_responses(self) -> dict[str, str]:
        """Get preset responses, if any."""
        return self.presets.responses

    def _select(self, compname: str):
        selected = None
        for comp in self.available_components:
            if comp.name == compname:
                selected = comp
                break
        if selected is None:
            raise ValueError(f"Could not find component {compname}")
        self.components.append(selected)
        # now let's remove any component incompatible with the selected one
        cleaned = []
        for comp in self.available_components:
            if comp != selected and selected.is_compatible_with(comp):
                cleaned.append(comp)
        self.available_components = cleaned


class ScaffoldWizard:
    """Scaffolding wizard."""

    def __init__(self, dst_dir: pathlib.Path, scaffold_dir: pathlib.Path, preset_file: Optional[pathlib.Path] = None):
        self.chart_dir = dst_dir
        self.scaffold = scaffold_dir
        log.info("Loading available components")
        self.available_components: list[Component] = sorted(
            [Component(f) for f in self.scaffold.glob("_wizard/*.yaml")], key=lambda x: x.priority
        )
        self.selected_components: list[Component] = []
        self.features = {"port": 0, "image": ""}
        self.to_replace = re.compile(r"^# replace:\s*(\w+)(; indent:\s*(\d+))?\s*$")
        self.answers = Answers(self.available_components, preset_file)

    def synth(self) -> pathlib.Path:
        """Synthetize every file in the skeleton using this template."""
        log.info("Creating the chart from %s", self.scaffold)
        # copy the files to the destination
        self.copy()
        # Patch the chart.yaml file
        self.patch_chartfile()
        # Select the components
        self.select_components()
        # Now let's cycle through all the files in the new chart dir's "templates" folder.
        # Any file ending in ".skel" will be scanned for things to template out, and renamed
        for skel in self.chart_dir.glob("templates/*.skel"):
            log.debug("Now processing %s", skel)
            self.process_skel(skel)
        # Ask any relevant questions
        responses = self.ask_questions()
        # Patch the values file
        self.modify_values(responses)
        # finally, write package.json, and return its path for usage by cli.Clart.create
        return self.write_packagefile()

    def write_packagefile(self) -> pathlib.Path:
        """Write the package.json file."""
        pkg = self.chart_dir / DEPFILE
        log.debug("Writing the package file %s", pkg)
        if pkg.exists():
            libmodules = set(json.loads(pkg.read_text()))
        else:
            libmodules = set()
        for component in self.selected_components:
            for libmodule in component.modules:
                libmodules.add(libmodule)
        with pkg.open("w", encoding="utf-8") as packagefile:
            json.dump(sorted(list(libmodules)), packagefile, indent=4)
        return pkg

    def copy(self):
        """Copy the scaffolding files to a destination directory."""
        skel = self.scaffold / "_skel"
        log.debug("Copying scaffolding files to %s", self.chart_dir)
        shutil.copytree(str(skel), str(self.chart_dir))

    def patch_chartfile(self):
        """Patch the Chart.yaml file."""
        chart = self.chart_dir / "Chart.yaml"
        if not chart.exists():
            raise RuntimeError(f"Error patching the chart file '{chart}': no such file or directory")
        patched_chart = chart.read_text().replace("__chartname__", self.chart_dir.name)
        chart.write_text(patched_chart)

    def ask_questions(self) -> dict[str, str]:
        """Read the questions file, select the ones that are relevant and ask them."""
        presets = self.answers.get_responses()
        if presets != {}:
            return presets
        # First of all, let's check if the selected components require any questions.
        questions_to_ask = {question for component in self.selected_components for question in component.questions}
        if not questions_to_ask:
            return {}
        # Load the questions
        questions_file = self.scaffold / "questions.yaml"
        if not questions_file.exists():
            raise RuntimeError(f"No questions file found at '{questions_file}' but the selected components require it")
        questions = yaml.safe_load(questions_file.read_text())
        if not isinstance(questions, dict):
            raise RuntimeError(f"Malformed questions file: {questions_file}")
        # Now let's just select the ones we want to ask
        return self._input_values({q: v for q, v in questions.items() if q in questions_to_ask})

    def modify_values(self, responses: dict[str, str]):
        """Patch the values.yaml file in the chart"""
        values_file = self.chart_dir / "values.yaml"
        input_data = values_file.read_text().splitlines()
        content: list[str] = []
        for line in input_data:
            if line == "# replace: values":
                for component in self.selected_components:
                    content.append(component.values)
            else:
                content.append(line)
        values = "\n".join(content)
        for label, value in responses.items():
            log.debug("Replacing label %s with value '%s'", label, value)
            values = values.replace(f"__{label}__", value)
        values_file.write_text(values)

    def select_components(self):
        """Make your component selection"""
        self.selected_components = sorted(self.answers.get_components(), key=lambda x: x.priority)
        print(f"Selected components: {','.join([m.name for m in self.selected_components])}\n")

    def _input_values(self, questions: dict[str, str]) -> dict[str, str]:
        """Fill in the values required"""
        print("\n===> Please answer the following questions:\n")
        responses: dict[str, str] = {}
        for label, question in questions.items():
            wrapped = textwrap.wrap(question, 70)
            formatted_q = f"* {wrapped[0]}\n"
            # visual indent all lines but the first
            if len(wrapped) > 1:
                formatted_q += textwrap.indent("\n".join(wrapped[1:]), 2 * " ")
            print(formatted_q)
            response = input("> ").rstrip()
            if response == "":
                log.debug("Not registering the response as it was empty")
                continue
            responses[label] = response
        return responses

    def _select(self, compname: str):
        selected = None
        for comp in self.available_components:
            if comp.name == compname:
                selected = comp
                break
        if selected is None:
            raise ValueError(f"Could not find component {compname}")
        self.selected_components.append(selected)
        # now let's remove any component incompatible with the selected one
        cleaned = []
        for comp in self.available_components:
            if comp != selected and selected.is_compatible_with(comp):
                cleaned.append(comp)
        self.available_components = cleaned

    def process_skel(self, skel: pathlib.Path):
        """Process a .skel file to generate the final product."""
        has_modifications = False
        dest_file = skel.parent / skel.stem
        content: list[str] = []
        for line in skel.read_text().splitlines():
            match = self.to_replace.match(line)
            if match is None:
                content.append(line)
                continue

            label = match.group(1)
            indent_match = match.group(3)
            indent = 0 if indent_match is None else int(indent_match)
            for comp in self.selected_components:
                output = comp.template_for(label, indent=indent)
                if output:
                    has_modifications = True
                content.extend(output)
        # check we're not writing an empty file, or a file with
        # no changes
        if has_modifications:
            dest_file.write_text("\n".join(content))
        # now remove the skeleton file
        skel.unlink()
