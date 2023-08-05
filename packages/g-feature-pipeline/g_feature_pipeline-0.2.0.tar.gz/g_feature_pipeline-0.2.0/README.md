# Feature Pipeline

Check out this
[Medium article](https://medium.com/towards-data-science/a-framework-for-building-a-production-ready-feature-engineering-pipeline-f0b29609b20f)
for more details about this module.

## Create Environment File

```shell
~/energy-forecasting $ cp .env.default .env
```

The command `cp .env.default .env` is used to create a copy of the
`.env.default` file and name it `.env`. In many projects, the `.env` file is
used to store environment variables that the application needs to run. The
`.env.default` file is usually a template that includes all the environment
variables that the application expects, but with default values. By copying it
to `.env`, you can customize these values for your own environment.

## Set Up the ML_PIPELINE_ROOT_DIR Variable

```shell
~/energy-forecasting $ export ML_PIPELINE_ROOT_DIR=$(pwd)
```

The command `export ML_PIPELINE_ROOT_DIR=$(pwd)` is setting the value of the
`ML_PIPELINE_ROOT_DIR` environment variable to the current directory. In this
context, `$(pwd)` is a command substitution that gets replaced with the output
of the `pwd` command, which prints the path of the current directory. The
`export` command then makes this variable available to child processes of the
current shell.

In essence, `ML_PIPELINE_ROOT_DIR` is an environment variable that is set to the
path of the current directory. This can be useful for scripts or programs that
need to reference the root directory of the ML pipeline, as they can simply
refer to `ML_PIPELINE_ROOT_DIR` instead of needing to know the exact path.

## Install for Development

Create virtual environment:

```shell
~/energy-forecasting                  $ cd feature-pipeline && rm poetry.lock
~/energy-forecasting/feature-pipeline $ bash ../scripts/devops/virtual_environment/poetry_install.sh
~/energy-forecasting/feature-pipeline $ source .venv/bin/activate
```

1. We first navigate to the `feature-pipeline` directory and remove the
   `poetry.lock` file. This step is essential if we intend to add new
   dependencies to the `pyproject.toml` file, as it ensures that Poetry
   accurately resolves and installs the latest compatible versions of all
   dependencies.
2. We then execute the `poetry_install.sh` script. This script
   is responsible for creating the virtual environment and installing the
   project dependencies. Importantly, it also includes steps to resolve
   potential issues related to the macOS arm64 architecture.
3. Finally, we activate the virtual environment. This step provides an isolated
   workspace for our project, preventing conflicts between the project's
   dependencies and those installed globally on the system.

Check the
[Set Up Additional Tools](https://github.com/iusztinpaul/energy-forecasting#-set-up-additional-tools-)
and [Usage](https://github.com/iusztinpaul/energy-forecasting#usage) sections to
see **how to set up** the **additional tools** and **credentials** you need to
run this project.

## Usage for Development

To start the ETL pipeline run:

```shell
~/energy-forecasting/feature-pipeline $ python -m feature_pipeline.pipeline
```

To create a new feature view run:

```shell
~/energy-forecasting/feature-pipeline $ python -m feature_pipeline.feature_view
```

**NOTE:** Be careful to set the `ML_PIPELINE_ROOT_DIR` variable as explained in
this
[section](https://github.com/iusztinpaul/energy-forecasting#set-up-the-ml_pipeline_root_dir-variable).
