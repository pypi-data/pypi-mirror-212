"""
Evaluation blocks to get results for a given timeseries model prediction
"""

# Local
from ...toolkit.hoist_module_imports import hoist_module_imports
from . import forecasting_evaluator

# Block classes hoisted to the top level
# NOTE: These must come after the module imports so that the block modules
#   themselves can be tracked cleanly for optional modules
hoist_module_imports(globals())
