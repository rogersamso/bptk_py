#                                                       /`-
# _                                  _   _             /####`-
#| |                                | | (_)           /########`-
#| |_ _ __ __ _ _ __  ___  ___ _ __ | |_ _ ___       /###########`-
#| __| '__/ _` | '_ \/ __|/ _ \ '_ \| __| / __|   ____ -###########/
#| |_| | | (_| | | | \__ \  __/ | | | |_| \__ \  |    | `-#######/
# \__|_|  \__,_|_| |_|___/\___|_| |_|\__|_|___/  |____|    `- # /
#
# Copyright (c) 2018 transentis labs GmbH
# MIT License


from .operators import *

import BPTK_Py.config.config as config
import statistics
import pandas as pd
import numpy as np



import matplotlib as plt

class Element:
    """
    Generic element in a SD model. Other model elements implement concrete logic within
    """

    type = "Element"

    def __init__(self, model, name, function_string = None):

        self.model = model
        self.name = name
        self.converters = []
        if function_string is None:
            self.function_string = self.default_function_string()
        else:
            self.function_string = function_string
        self._equation = None
        self.generate_function()

    def default_function_string(self):
        """
        Returns a stub lambda function as string: For each T, return 0
        :return:
        """
        return "lambda model, t: 0"

    def generate_function(self):
        """
        Generate the function using the function_string value and eval()
        :return: None
        """
        fn = eval(self.function_string)
        self.model.equations[self.name] = lambda t: fn(self.model, t)
        self.model.memo[self.name] = {}

    def term(self, time="t"):
        return "model.memoize('{}',{})".format(self.name, time)

    @property
    def equation(self):
        """

        :return: self._equation
        """
        return self._equation

    @equation.setter
    def equation(self, equation):
        """
        Set the equation
        :param equation: equation as String
        :return: None
        """
        self._equation = equation

        self.model.reset_cache()

        self.function_string = "lambda model, t: {}".format(equation)
        self.generate_function()


    def plot(self,starttime = None, stoptime = None, dt = None, return_df=False):

        ## Equation von start bis stop
        dt = self.model.dt if dt is None else dt
        stoptime = self.model.stoptime if stoptime is None else stoptime
        starttime = self.model.starttime if starttime is None else starttime

        try:
            df = pd.DataFrame({self.name: {t: self(t) for t in np.arange(starttime,stoptime+dt,dt)}})
        except:
            df = pd.DataFrame({self.name: {t: self(t) for t in np.arange(self.model.starttime,self.model.stoptime+dt, dt)}})
        # ensure column is of float type and not e.g. an integer

        if return_df:
            return df
        else:
            ax = df.plot(kind="area",
                stacked=False,
                figsize=config.configuration["figsize"],
                title=self.name,
                alpha=config.configuration["alpha"], color=config.configuration["colors"],
                lw=config.configuration["linewidth"])

            for ymaj in ax.yaxis.get_majorticklocs():
                ax.axhline(y=ymaj, ls='-', alpha=0.05, color=(34.1 / 100, 32.9 / 100, 34.1 / 100))

            self.update_plot_formats(ax)

    ### Operator overrides

    def __str__(self):
        return self.term()

    def __call__(self, *args, **kwargs):
        return self.model.evaluate_equation(self.name, args[0])

    def __mul__(self, other):
        return MultiplicationOperator(self, other)

    def __rmul__(self, other):
        return NumericalMultiplicationOperator(self, other)

    def __add__(self, other):
        return AdditionOperator(self, other)

    def __sub__(self, other):
        return SubtractionOperator(self, other)

    def __truediv__(self, other):
        return DivisionOperator(self, other)

    def __neg__(self):
        return NumericalMultiplicationOperator(self, (-1))

    def update_plot_formats(self, ax):
        """
        Configure the plot formats for the labels. Generates the formatting for y labels
        :param ax:
        :return:
        """
        ylabels_mean = statistics.mean(ax.get_yticks())

        # Override the format based on the mean values
        if ylabels_mean <= 2.0 and ylabels_mean >= -2.0:
            ylabels = [format(label, ',.2f') for label in ax.get_yticks()]

        elif ylabels_mean <= 10.0 and ylabels_mean >= -10.0:
            ylabels = [format(label, ',.1f') for label in ax.get_yticks()]

        else:
            ylabels = [format(label, ',.0f') for label in ax.get_yticks()]

        ax.set_yticklabels(ylabels)


class ElementError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
