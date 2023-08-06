"""Test the scaffolding module."""
import json
import pathlib
import shutil
import tempfile
from unittest import mock

import pytest
import yaml

from sextant.scaffold import Component, ScaffoldWizard

from . import fixtures

scaffold = fixtures / "scaffold"


def get_component(name: str) -> Component:
    """Load a single component."""
    component_path = scaffold / "_wizard" / f"{name}.yaml"
    return Component(component_path)


@pytest.fixture(name="component")
def get_scaffold() -> Component:
    """Get the more complete objects"""
    return get_component("scaffold")


@pytest.fixture(name="ingress")
def get_ingress() -> Component:
    """Get the istio-ingress ccomponent"""
    return get_component("ingress")


# Tests for the component class
def test_component_init(component: Component):
    """Verify that the component is correctly initialized."""
    assert "deployment" in component.templates
    assert component.conflicts == []
    assert component.priority == 1
    assert component.values.startswith("# Sample values")
    assert "lamp.httpd:1.0" in component.modules
    assert component.name == "tests"
    assert component.questions == []


def test_component_init_no_prio(ingress: Component):
    """Verify that conflicts are loaded, default priority is used."""
    assert ingress.conflicts == ["nginx-ingress"]
    assert ingress.priority == 99
    assert ingress.questions == ["host"]


def test_template_for_no_match(component: Component):
    """Should return an empty list if no match is found."""
    # Template absent yields an empty list
    assert component.template_for("invalid") == []
    assert component.template_for("invalid", indent=10) == []


def test_template_match(component: Component):
    """Should return the proper template."""
    # Template is correctly returned.
    assert component.template_for("deployment")[0] == '{{- include "lamp.httpd.container" . }}'


def test_template_for_indent_match(component: Component):
    """The template gets properly indented."""
    with_indent = component.template_for("deployment", indent=2)
    assert with_indent[0] == '  {{- include "lamp.httpd.container" . | indent 2 }}'
    # in absence of an include, no additional indent command is added.
    assert with_indent[4] == "  {{- if .Values.monitoring.enabled . }}"


def test_is_compatible_with(ingress: Component):
    """Should return false if two component conflict, true otherwise"""
    ingress_nginx = get_component("ingress_nginx")
    assert ingress.is_compatible_with(ingress_nginx) is False
    tests = get_component("scaffold")
    assert ingress.is_compatible_with(tests)
    # Now let's test the case where the other module has a conflict with the current one, but not
    # vice-versa.
    assert ingress_nginx.is_compatible_with(tests) is False


# Tests for the ScaffoldWizard class
class TestScaffoldWizard:
    """Test the scaffold wizard"""

    def setup_class(self):
        """Create the temp dir"""
        # pylint: disable=attribute-defined-outside-init
        self.chart_base = tempfile.mkdtemp()

    def setup_method(self):
        """Initialize the test environment"""
        # pylint: disable=attribute-defined-outside-init
        self.wizard = ScaffoldWizard(pathlib.Path(self.chart_base) / "foobar", scaffold)

    def teardown_method(self):
        """Removes the leftovers from the tests."""
        shutil.rmtree(self.wizard.chart_dir, ignore_errors=True)

    def teardown_class(self):
        """Remove the temp dir"""
        shutil.rmtree(self.chart_base)

    def _preselect(self):
        """Fake component selection for tests where we're uninterested in testing that specifically."""
        to_sel = ["tests", "istio-ingress"]
        for component in self.wizard.available_components:
            if component.name in to_sel:
                self.wizard.selected_components.append(component)
        # empty the available components list as a consequence.
        self.wizard.available_components = []
        # Now let's not forget to copy over the files.
        self.wizard.copy()

    def test_component_load(self):
        """All components are correctly loaded."""
        assert len(self.wizard.available_components) == 3
        assert "nginx-ingress" in [c.name for c in self.wizard.available_components]

    def test_copy(self):
        """Copying works as expected."""
        self._preselect()
        for dst in ["Chart.yaml", "templates/deployment.yaml.skel"]:
            should_exist = self.wizard.chart_dir / dst
            assert should_exist.exists()

    def test_write_packagefile(self):
        """Writing a package file preserves all information."""
        self._preselect()
        packagefile_path = self.wizard.write_packagefile()
        assert isinstance(packagefile_path, pathlib.Path)
        packages = json.loads(packagefile_path.read_text())
        assert "base.name:1.0" in packages
        assert "lamp.common:1.0" in packages

    def test_patch_chartfile(self):
        """The chart file is correctly patched."""
        self._preselect()
        chartsfile = self.wizard.chart_dir / "Chart.yaml"
        chartname = self.wizard.chart_dir.name
        self.wizard.patch_chartfile()
        assert f"name: {chartname}" in chartsfile.read_text()

    def test_modify_values(self):
        """Values files get correctly built and interpolated with the values from responses."""
        responses = {"host": "pinkunicorn.local"}
        self._preselect()
        self.wizard.modify_values(responses)
        values = self.wizard.chart_dir / "values.yaml"

        # The file exists and is a valid yaml document after patching.
        assert values.exists()
        values_content = yaml.safe_load(values.read_text())

        # It contains entries from all selected modules, and does interpolate with responses.
        assert values_content["ingress"]["hostname"] == "pinkunicorn.local"
        assert values_content["monitoring"]["enabled"]

    @mock.patch("sextant.scaffold.Component.template_for")
    def test_process_skel(self, mocker):
        """A skel file is correctly processed."""
        self._preselect()
        skelfile = self.wizard.chart_dir / "templates/deployment.yaml.skel"
        self.wizard.process_skel(skelfile)
        assert skelfile.exists() is False
        transformed = self.wizard.chart_dir / "templates/deployment.yaml"
        assert transformed.exists()
        mocker.assert_has_calls([mock.call("deployment", indent=8)])

    def test_process_skel_no_mod(self):
        """A skel file with no modifications is discarded."""
        self._preselect()
        skelfile = self.wizard.chart_dir / "templates/spurious.yaml.skel"
        self.wizard.process_skel(skelfile)
        assert skelfile.exists() is False
        transformed = self.wizard.chart_dir / "templates/spurious.yaml"
        assert transformed.exists() is False

    @mock.patch("sextant.scaffold.interactive.ask_input")
    def test_select_components(self, mocker):
        """Selecting a component conflicting with another removes the latter from the available modules."""
        mocker.side_effect = ["istio-ingress", "q"]
        self.wizard.select_components()
        assert len(self.wizard.answers.available_components) == 1
        assert self.wizard.answers.available_components[0].name == "tests"

    @mock.patch("sextant.scaffold.interactive.ask_input")
    def test_synth(self, mocker):
        """Synth works correctly if the right modules are selected."""
        # We select the nginx-ingress and the tests component,
        # No need to call quit here.
        mocker.side_effect = ["tests", "istio-ingress"]
        with mock.patch("sextant.scaffold.input") as input_mock:
            input_mock.return_value = "pinkunicorn.dev"
            self.wizard.synth()
        chart = self.wizard.chart_dir
        self._check_scaffolded(chart)

    def test_preset_file(self):
        """Components get selected correctly"""
        preset_file = scaffold / "presets.yaml"
        wiz = ScaffoldWizard(pathlib.Path(self.chart_base) / "foobar", scaffold, preset_file=preset_file)
        # no need to patch.
        wiz.synth()
        self._check_scaffolded(wiz.chart_dir)

    def _check_scaffolded(self, chart: pathlib.Path):
        # Check the chartfile
        chartfile = chart / "Chart.yaml"
        assert chartfile.exists()
        assert "name: foobar" in chartfile.read_text()
        deployment = chart / "templates/deployment.yaml"
        assert deployment.exists()
        deployment_content = deployment.read_text()
        # Indent works as expected.
        assert '\n        {{- include "lamp.httpd.container" . | indent 8 }}' in deployment_content
        assert "\n        {{- if .Values.monitoring.enabled . }}" in deployment_content
        assert '\n        {{ include "ingress.istio.sidecar" . }}' in deployment_content
        values = chart / "values.yaml"
        assert values.exists()
