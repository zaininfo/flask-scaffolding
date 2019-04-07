# -*- coding: utf8 -*-

"""Provide validation of API version."""

from functools import wraps
import re

from flask import abort, request

from .util.get_logger import get_logger

LOGGER = get_logger()


def verify_version(func):
    """Verify that a request is either GET or POST and that it includes a version (SemVer) header."""
    @wraps(func)
    def decorated_function(*args, **kwargs):  # pylint: disable=inconsistent-return-statements
        mime_type = r'^application/(?:v([0-9]\.[0-9]\.[0-9])\+)?json$'
        match = None

        if request.method == 'GET':
            match = re.match(mime_type, request.headers.get('Accept', ''))

        elif request.method == 'POST':
            match = re.match(mime_type, request.headers.get('Content-Type', ''))

        if match:
            return func(*args, **kwargs, version=match.group(1))

        LOGGER.info('version not found')
        abort(406)

    return decorated_function
