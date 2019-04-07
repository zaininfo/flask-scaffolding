# -*- coding: utf8 -*-

"""Provide logging facility."""

import logging
import logging.config

from ._get_caller_module_info import get_caller_module_info
from ._get_environment import get_environment
from ._get_file_path import get_file_path

logging.config.fileConfig(fname=get_file_path('../../config/{}.ini').format(get_environment()))


def get_logger():
    """Return a logger for the module that calls this function."""
    return logging.getLogger(get_caller_module_info()['__name__'])
