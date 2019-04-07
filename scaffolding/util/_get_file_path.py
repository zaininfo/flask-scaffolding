# -*- coding: utf8 -*-

"""Resolve file paths."""

import os

from ._get_caller_module_info import get_caller_module_info


def get_file_path(file_name):
    """Return the absolute path for a given relative file path."""
    module_path = os.path.dirname(os.path.realpath(get_caller_module_info()['__file__']))
    return os.path.normpath(os.path.join(module_path, file_name))
