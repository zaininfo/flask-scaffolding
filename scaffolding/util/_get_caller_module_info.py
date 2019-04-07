# -*- coding: utf8 -*-

"""Provide meta information about a module."""

import inspect


def get_caller_module_info():
    """Return the name and path of the module that calls this function."""
    caller_frame = inspect.stack()[2]

    try:
        caller_module = inspect.getmodule(caller_frame[0])
        caller_module_name = caller_module.__name__
        caller_module_file_path = caller_module.__file__
    finally:
        del caller_frame

    return {
        '__name__': caller_module_name,
        '__file__': caller_module_file_path
    }
