# -*- coding: utf8 -*-

"""Provide authorization for HTTP server."""

from functools import wraps

from flask import abort

from .authenticator import get_user_name, get_user_role
from .util.get_logger import get_logger

LOGGER = get_logger()


def authorize(*roles):
    """Verify that the requesting user has one of the specified roles."""
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):  # pylint: disable=inconsistent-return-statements
            if get_user_role() in roles:
                return func(*args, **kwargs)

            LOGGER.info('user %s does not have required permissions', get_user_name())
            abort(403)

        return decorated_function
    return decorator
