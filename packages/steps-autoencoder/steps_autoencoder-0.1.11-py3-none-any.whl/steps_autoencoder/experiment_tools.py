import datetime
import itertools
import pandas as pd
import mlflow
import ray
import neptune

class GridSearchExperiment:
    def __init__(self, settings, experiment_suffix='exp', experiment_support=[]):
        self.settings = settings
        self.default_params = settings['default_params']
        self.variable_params = settings['variable_params']
        self.experiment_support = experiment_support
        self.experiment_prefix = experiment_suffix
        self.launch_time = datetime.datetime.now()
        self.experiment_name = "{} - {}".format(self.experiment_prefix, self.launch_time.strftime("%Y-%m-%d %H%M%S"))

        # create pandas data frame of all combinations of variable parameters
        variable_param_keys = list(self.variable_params.keys())

        # use itertools.product to create a list of all combinations of variable parameters
        variable_param_values = list(itertools.product(*[self.variable_params[key] for key in variable_param_keys]))

        # create a pandas data frame from the list of combinations
        df = pd.DataFrame(variable_param_values, columns=variable_param_keys)

        # shuffle the data frame's rows
        df = df.sample(frac=1).reset_index(drop=True)

        # mlflow and neptune cannot be together in the experiment_support list
        assert not ('mlflow' in self.experiment_support and 'neptune' in self.experiment_support), "mlflow and neptune cannot be together in the experiment_support list"

        if 'mlflow' in self.experiment_support:
            experiment_id = mlflow.create_experiment(name=self.experiment_name, artifact_location="mlruns")
            mlflow.set_experiment(experiment_id)
            mlflow.log_param('launch_time', self.launch_time.strftime("%Y-%m-%d %H%M%S"))
            mlflow.log_param('experiment_prefix', self.experiment_prefix)
            mlflow.log_param('variable_params', self.variable_params)
            mlflow.log_param('default_params', self.default_params)
            mlflow.log_param('experiment_support', self.experiment_support)
            mlflow.log_param('settings', self.settings)
            mlflow.log_param('num_planned_runs', len(df))

        if 'ray' in self.experiment_support:
            ray.init(ignore_reinit_error=True)

        if 'neptune' in self.experiment_support:
            pass