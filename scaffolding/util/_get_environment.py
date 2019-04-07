# -*- coding: utf8 -*-

"""Provide information about the active environment."""

import os

from dotenv import load_dotenv

from ._get_file_path import get_file_path

load_dotenv(dotenv_path=get_file_path('../../.env'), override=True)

PYTHON_ENV = os.getenv('PYTHON_ENV')

if PYTHON_ENV not in ('development', 'staging', 'production'):
    PYTHON_ENV = 'development'

ENVIRONMENT_VARIABLES = {
    'JWT_PUBLIC_KEY': os.getenv('JWT_PUBLIC_KEY'),
    'JWT_PRIVATE_KEY': os.getenv('JWT_PRIVATE_KEY'),
    'ACCESS_CREDS': os.getenv('ACCESS_CREDS')
}


def get_environment(environment_variable=None):
    """Return the name of the active environment or the value of the given environment variable."""
    return ENVIRONMENT_VARIABLES[environment_variable] if environment_variable else PYTHON_ENV
