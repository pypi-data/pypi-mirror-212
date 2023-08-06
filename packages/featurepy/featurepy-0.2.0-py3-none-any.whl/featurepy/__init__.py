from aspectlib import Aspect, weave, Proceed, Return
from .model_constraints import model_constraints

from featuremonkey3 import Composer, select, select_equation
weave(select, model_constraints)
