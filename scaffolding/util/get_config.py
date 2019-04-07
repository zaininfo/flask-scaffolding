# -*- coding: utf8 -*-

"""Provide configurations."""

import sys

from configobj import ConfigObj
from validate import Validator

from ._get_caller_module_info import get_caller_module_info
from ._get_environment import get_environment
from ._get_file_path import get_file_path
from .get_logger import get_logger

LOGGER = get_logger()

CONFIG = ConfigObj(
    get_file_path('../../config/{}.ini').format(get_environment()),
    configspec=get_file_path('../../config/configspec.ini')
)

VALIDATOR = Validator()
RESULT = CONFIG.validate(VALIDATOR)

if RESULT is not True:
    LOGGER.error('failed to validate config file')
    sys.exit(1)


def get_config():
    """Return the configuration values for the module that calls this function."""
    app_config = {}

    try:
        app_config = CONFIG['app']['_'.join(get_caller_module_info()['__name__'].split('.'))]
    except KeyError:
        pass

    return {
        **app_config,
        'env': get_environment()
    }


def get_secrets():
    """Return the secret values used for authentication."""
    return {
        'public_key': get_environment('JWT_PUBLIC_KEY'),
        'private_key': get_environment('JWT_PRIVATE_KEY'),
        'access_credentials': get_environment('ACCESS_CREDS')
    }
