from mlxpy.launcher import launch, Context
from mlxpy.reader import Reader
from mlxpy.logger import DefaultLogger
from mlxpy.version_manager import GitVM

from mlxpy.scheduler import Scheduler, SLURMScheduler, OARScheduler

from mlxpy.data_structures.config_dict import ConfigDict
from mlxpy.data_structures.data_dict import DataDictList


__all__ = [
    "launch", 
    "Reader",
    "DefaultLogger",
    "Scheduler",
    "ConfigDict",
    "Context",
    "DataDictList",
    "OARScheduler",
    "SLURMScheduler",
    "GitVM"
]



VERSION = (0, 0, 1)
PROJECT = 'MLXP'
AUTHOR = "Michael Arbel"
AUTHOR_EMAIL = "michael.n.arbel@gmail.com"
URL = "https://github.com/MichaelArbel/mlxpy"
LICENSE = "MIT License"
VERSION_TEXT = ".".join(str(x) for x in VERSION)
COPYRIGHT = "Copyright (C) 2023 " + AUTHOR


VERSION_STATUS = ""
RELEASE = VERSION_TEXT + VERSION_STATUS


__version__ = VERSION_TEXT
__author__ = AUTHOR
__copyright__ = COPYRIGHT 
__credits__ = ["Romain Ménégaux",
                "Alexandre Zouaoui",
                "Juliette Marrie",
                "Pierre Wolinski"]

