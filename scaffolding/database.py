# -*- coding: utf8 -*-

"""Provide an interface to database."""

from .redis import get_redis


def get_value(resource_id):
    """Return the value of the resource."""
    redis_db = get_redis()
    value = redis_db.get(_generate_key(resource_id))
    return value if value is None else value.decode('utf-8')


def set_value(resource_id, value):
    """Save the value of the resource."""
    redis_db = get_redis()
    return redis_db.set(_generate_key(resource_id), value, nx=True)


def _generate_key(resource_id):
    return 'flask_scaffolding:{}'.format(resource_id)
