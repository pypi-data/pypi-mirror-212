import itertools
import pandas as pd

class GridSearchExperiment:
    def __init__(self, settings):
        self.settings = settings
        self.default_params = settings['default_params']
        self.variable_params = settings['variable_params']

        # create pandas data frame of all combinations of variable parameters
        variable_param_keys = list(self.variable_params.keys())

        # use itertools.product to create a list of all combinations of variable parameters
        variable_param_values = list(itertools.product(*[self.variable_params[key] for key in variable_param_keys]))

        # create a pandas data frame from the list of combinations
        df = pd.DataFrame(variable_param_values, columns=variable_param_keys)

        print(df)
