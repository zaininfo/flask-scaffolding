# -*- coding: utf8 -*-

"""Provide an HTTP server."""

import uuid

from flask import abort, Flask, jsonify, request

from . import __version__
from .authenticator import authenticate, authenticate_fresh, get_blueprint
from .authorizer import authorize
from .database import get_value, set_value
from .util.get_config import get_secrets
from .util.get_logger import get_logger
from .versioner import verify_version

SECRETS = get_secrets()
LOGGER = get_logger()

APP = Flask(__name__)
APP.register_blueprint(get_blueprint(APP))


def start_server():
    """Start HTTP server."""
    APP.run()


@APP.route('/version', methods=['GET'])
def meta():
    """Return the version of flask scaffolding."""
    return jsonify({'version': __version__})


@APP.route('/resources/<resource_id>', methods=['GET'])
@authenticate
@authorize('viewer', 'editor')
@verify_version
def get_resource(version, resource_id):  # pylint: disable=unused-argument,inconsistent-return-statements
    """Return a specific resource."""
    value = get_value(resource_id)

    if value:
        return jsonify(value)

    LOGGER.info('no resource found for %s', resource_id)
    abort(404)


@APP.route('/resources', methods=['POST'])
@authenticate_fresh
@authorize('editor')
@verify_version
def add_resource(version):  # pylint: disable=unused-argument,inconsistent-return-statements
    """Add a new resource."""
    body = request.get_json()

    if not body or 'value' not in body:
        LOGGER.info('no value provided for new resource')
        abort(400)

    resource_id = body['id'] if 'id' in body else uuid.uuid4()

    saved = set_value(resource_id, body['value'])

    if saved:
        return jsonify({
            'id': resource_id,
            'value': body['value']
        })

    LOGGER.info('resource for %s already exists', resource_id)
    abort(409)
