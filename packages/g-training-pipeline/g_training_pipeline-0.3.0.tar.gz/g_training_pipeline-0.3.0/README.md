# Training Pipeline

Check out this
[Medium article](https://medium.com/towards-data-science/a-guide-to-building-effective-training-pipelines-for-maximum-results-6fdaef594cee)
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

```shell
~/energy-forecasting                   $ cd training-pipeline && rm poetry.lock
~/energy-forecasting/training-pipeline $ bash ../scripts/devops/virtual_environment/poetry_install.sh
~/energy-forecasting/training-pipeline $ source .venv/bin/activate
```

Check the
[Set Up Additional Tools](https://github.com/iusztinpaul/energy-forecasting#-set-up-additional-tools-)
and [Usage](https://github.com/iusztinpaul/energy-forecasting#usage) sections to
see **how to set up** the **additional tools** and **credentials** you need to
run this project.

## Usage for Development

**Run the scripts in the following order:**

1. Start the hyperparameter tuning script:

    ```shell
    ~/energy-forecasting/training-pipeline $ python -m training_pipeline.hyperparameter_tuning
    ```

2. Upload the best config based on the previous hyperparameter tuning step:

    ```shell
    ~/energy-forecasting/training-pipeline $ python -m training_pipeline.best_config
    ```

3. Start the training script using the best configuration uploaded one step
   before:

    ```shell
    ~/energy-forecasting/training-pipeline $ python -m training_pipeline.train
    ```

**NOTE:** Be careful to set the `ML_PIPELINE_ROOT_DIR` variable as explain in
this
[section](https://github.com/iusztinpaul/energy-forecasting#set-up-the-ml_pipeline_root_dir-variable).
