# sextant

A tool to compose and manage helm charts from the wikimedia library of template modules.

It offers multiple functions:
* `sextant [OPTIONS] vendor [-f] CHART_DIR` allows you to generate the vendored modules bundle for your chart, provided you have a package.json in `CHART_DIR`
* `sextant [OPTIONS] search CHARTS_DIR NAMESPACE.MODULE:VERSION` finds, within a charts collection, all the ones that depend on a specific module
* `sextant [OPTIONS] update CHARTS_DIR NAMESPACE.MODULE:VERSION...` allows to update the module dependencies for a chart or multiple ones
* `sextant [OPTIONS] create-chart CHART_DIR [-s SCAFFOLD_DIR]` allows to create a chart based on templates defined in SCAFFOLD_DIR. See below for details
* `sextant [OPTIONS] update-version CHART_DIR [-v VERSION]` updates a chart version, either to the next patch level, or to the version provided

The available global options are:
* `--debug` to print out debug information; useful when reporting bugs (there are many)
* `--modulepath` to indicate where your modules are located; defaults to `./modules` which is ok if you're running from the root of the deployment-charts repository.

## Installation

Get the latest released version from pip:

    $ pip install sextant

If you want the latest improvements, clone this repository and run

    $ python3 setup.py install

## Create a new release

Create a version tag and push it to gitlab. Then clean previous build artifacts, rebuild the wheels for the package, and upload them using twine:

    $ rm -rf dist/ build/ *.egg-info/
    $ python setup.py sdist bdist_wheel
    $ python -m twine upload dist/*

Several folks on the wikimedia SRE team have the right to perform the upload

## Examples

### Vendor a new dependency
Say you added a dependency on a new module; just edit `package.json`, then run:

    $ sextant vendor charts/mychart

This should add the desired module, at the latest patch release of the requested version.

### Update all dependencies to the latest patch version
Force re-vendoring; you can either remove the package.lock file or use `-f`

    $ sextant vendor -f charts/mychart

All modules should be upgraded to the latest patch version.

### Update to a new minor/major version
You can do this either on a single chart:

    $ sextant update charts/mychart foo.bar:2.1 foo.baz:2.0

or on a whole collections of charts

    $ sextant update charts foo.bar:2.1 foo.baz:2.0

It must be noted that if one of the charts has failed dependencies, the process will stop there.

### Create a new chart from scaffolding models
Assuming you have already scaffolding models in a `models` directory, you can create a new chart using:

    $ sextant create-chart charts/mynewchart -s models

Depending on how you configured your "models" directory, you will be asked which modules you want to include,
and a series of other questions about your new chart.

## Modules
Modules are intended to be collections of reusable helm chart bits we might want to reuse across different charts.
Sextant helps manage them and bundle them together to be used in a chart, managing also their lifecycle.

Each module is expected to be a file, within a *namespace* directory, named `modulename_X.Y.Z.tpl`. Any template defined within it will have a name in the format `namespace.modulename.tplname`. Each namespace directory needs to contain a `module.json` file enumerating the available modules and the dependency of each module from other modules.

Give we assume *strict* semantic versioning for our modules, the dependencies only need to specify the `major.minor` version number.

See for instance `tests/fixtures/foo/module.json` for a complete example.

## Models
Writing a helm chart from scratch requires copying around a lot of boilerplate, or to create a base chart general enough to work with most applications and needing small modifications to work. Such charts would contain a lot of clutter and be quite hard to debug.

Sextant offers the idea of "models" for scaffolding, meaning you can define multiple scaffolding model systems that will allow sextant to tailor your chart to your needs, if there is a template for the functionality you want to use.

A model directory will contain what follows:
* A `_skel` subdirectory containing files to copy to the final chart. Under `templates`, any file with a `.skel` extension will be processed to enrich it with the components the user has chosen.
* A `_wizard` directory, containing yaml files that configure such components
* A `questions.yaml` file containing questions we want to ask the user to get user-defined variables to substitute in `values.yaml`

### How a model works
Each `.skel` file, will contain lines like this:

    # replace: <label> // no indentation
    # replace: <label>; indent: 4 // indent all templates and inserts within by 4 spaces

Sextant, when running in `create-chart` mode, will substitute this line with the text bits associated to that `label` in the component that the user has selected from `_wizard`, in order of priority.

### What is in a wizard component
Each component should provide a specific functionality to a chart.

So for instance, let's assume we are adding a mcrouter component. Here's how our component would look like:

    name: mcrouter
    description: Installs mcrouter as an optional sidecar
    priority: 90  # This will go after all main app stuff
    modules:
        - "base.name:1.0"
        - "cache.mcrouter:1.0"
    conflicts:
      - nutcracker
    templates:
        deployment: |
          {{- include "cache.mcrouter.deployment" . }}
          {{- if .Values.monitoring.enabled }}
            {{- include "cache.mcrouter.exporter" . }}
          {{- end }}
        configmap: |2
          {{- include "cache.mcrouter.configmap" }}
        np_egress: |
          {{ if .Values.networkpolicy.egress }}
          {{- include "cache.mcrouter.networkpolicy-egress" . }}
          {{- end }}
        service: |
          {{- include "cache.mcrouter.service" }}
    values: |
        # here we would add values to add to values.yaml
        cache:
          # Set to true to enable mcrouter
          enabled: true
          # Should mcrouter be exposed?
          expose: mcrouter_expose
    questions:
      - mcrouter_expose

Let's go through all entries.

* **priority** indicates where templates and values will be placed within the respective files.
* **modules** is a list of modules needed for this component to function
* **conflicts** a list of other components that can't operate together with this one. Omit if none.
* **templates** is a list of label -> replacements to inject in the `.skel` files.
* **values** is a chunk of a values file pertaining to this specific component
  that needs to be added to values.yaml


Let's dig slightly deeper on how templates work: whenever a `# replace: deployment` line is found in the `.skel` files, that line will be replaced with the content of the `templates.deployment` from all the wizard components that have one. If an indent level is indicated, all lines will have the
desired indent level prepended, and any `include` instruction that has the trailing spaces removed (by using `{{-`) will have the desired indentation level inserted.

So, say our `.skel` file looks like this:

    apiVersion: apps/v1
    kind: Deployment
    spec:
      ...
      template:
        spec:
          containers:
    # replace: deployment; indent: 8

if we only declared the mcrouter component, our resulting helm template will look as follows:


    apiVersion: apps/v1
    kind: Deployment
    spec:
      ...
      template:
        spec:
          containers:
            {{- include "cache.mcrouter.deployment" . | indent 8 }}
            {{- if .Values.monitoring.enabled }}
              {{- include "cache.mcrouter.exporter" . | indent 8 }}
            {{- end }}

A similar mechanism works for the values.yaml file, without the complication of
indentation levels.

### questions.yaml

This file should contain a `label: question` dictionary  of questions to ask input for to the user, and the responses will be used to substitute all occurrences of `__label__` in the `values.yaml` file of the chart we're creating.

For every component that was selected, the list of questions required will be collected and the user will be asked them.

### Example
An example of a model can be found under `tests/fixtures/scaffold`

## License
See the LICENSE file.