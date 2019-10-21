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

from .operators import MaxOperator, MinOperator, Lookup, Trend, Smooth, Step, Exp, Time, OperatorError, Delay
from .constant import Constant
from .element import Element


def time():
    return Time()


def max(x, y):
    return MaxOperator(x, y)


def min(x, y):
    return MinOperator(x, y)


def lookup(element, points):
    return Lookup(element, points)


def trend(model, input_function,averaging_time,initial_value):
    if isinstance(initial_value, (float, Constant)):
        return Trend(model, input_function, averaging_time, initial_value)
    else:
        raise OperatorError("The initial value must be a floating point values or a constants")


def smooth(model, input_function, averaging_time, initial_value):
    if isinstance(initial_value, (float, Constant)):
        return Smooth(model, input_function, averaging_time, initial_value)
    else:
        raise OperatorError("The initial value must be a floating point values or a constants")


def step(height, timestep):
    return Step(height, timestep)


def exp(x):
    return Exp(x)


def delay(model, input_function, delay_duration, initial_value=None):
    if not isinstance(input_function, Element):
        raise OperatorError("The input function must be a model element")
    if not isinstance(delay_duration, (Element, float)):
        raise OperatorError("The delay duration must be a model element or a floating point value")
    if initial_value is not None and isinstance(initial_value, (float, Constant)):
        raise OperatorError("The initial value must be a floating point values or a constant")

    return Delay(model, input_function, delay_duration, initial_value)

