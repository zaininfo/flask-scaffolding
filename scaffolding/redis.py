# -*- coding: utf8 -*-

"""Provide Redis connection."""

import os
import re
import sys

import redis

from .util.get_config import get_config
from .util.get_logger import get_logger

CONFIG = get_config()
LOGGER = get_logger()

REDIS_URL = os.getenv('REDIS_URL')

MATCH = None

if REDIS_URL:
    MATCH = re.match(r'redis://\S+:(\S+)@(\S+):(\d+)', REDIS_URL)

    if not MATCH:
        LOGGER.error('failed to validate Redis URL')
        sys.exit(1)

PASSWORD, HOSTNAME, PORT = MATCH.groups() if MATCH else [None] + CONFIG['host'].split(':')
REDIS_DB = redis.StrictRedis(host=HOSTNAME, port=PORT, db=CONFIG['database'], password=PASSWORD)


def get_redis():
    """Return Redis connection."""
    return REDIS_DB


def get_redis_config():
    """Return Redis configuration values."""
    return {
        'host': HOSTNAME,
        'port': PORT,
        'db': CONFIG['database'],
        'password': PASSWORD
    }
