# *****************************************************************#
# (C) Copyright IBM Corporation 2021.                             #
#                                                                 #
# The source code for this program is not published or otherwise  #
# divested of its trade secrets, irrespective of what has been    #
# deposited with the U.S. Copyright Office.                       #
# *****************************************************************#
"""IBM Watson Core AI Framework library.  This is the base framework for core AI/ML libraries, such
as NLP and Vision.
"""

# the import order cannot adhere to the linter here because we must do things like
# disable warnings, initialize the JVM and configure logging in a specific order
# pylint: disable=wrong-import-position,wrong-import-order

# We're filtering (most) warnings for now
import warnings as _warnings

_warnings.filterwarnings("ignore")


# Backwards compatibility: Some users may have done `from autoai_ts_libs.deps.watson_core import beta`
# Any usage of the module will obviously break, but it was a beta after all
class _DeprecationMeta(type):
    def __getattr__(self, name):
        # Allow DeprecationWarnings through if somebody tries to access the beta
        _warnings.filterwarnings("default", category=DeprecationWarning)
        # And actually warn them
        _warnings.warn("watson_core.beta has been fully removed", DeprecationWarning)
        return self


class beta(metaclass=_DeprecationMeta):
    """watson_core.beta is deprecated"""


# must import toolkit first since we need alog to be set up before it is used
from . import toolkit
from .toolkit import *

from . import data_model
from .data_model import dataobject

from . import module
from .module import *

from . import module_config
from .module_config import ModuleConfig

from .model_manager import *

from . import config
from .config import *

from . import blocks
from .blocks.base import block, BlockBase

from . import workflows
from .workflows.base import workflow, WorkflowBase

from . import resources
from .resources.base import resource, ResourceBase

 
