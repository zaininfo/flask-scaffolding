# -*- coding: utf8 -*-

"""Provide authentication for HTTP server."""

from flask import abort, Blueprint, jsonify, request
from flask_jwt_extended import (  # pylint: disable=unused-import
    JWTManager, create_access_token, create_refresh_token, fresh_jwt_required as authenticate_fresh,
    get_jwt_claims, get_jwt_identity as get_user_name, jwt_refresh_token_required, jwt_required as authenticate
)

from .util.get_config import get_secrets
from .util.get_logger import get_logger

SECRETS = get_secrets()
LOGGER = get_logger()

AUTH = Blueprint('authenticator', __name__)
JWT = JWTManager()


def get_blueprint(app):
    """Initialize JWT and return the authentication blueprint."""
    app.config['JWT_PUBLIC_KEY'] = SECRETS['public_key']
    app.config['JWT_PRIVATE_KEY'] = SECRETS['private_key']
    app.config['JWT_ALGORITHM'] = 'RS256'
    app.config['JWT_CLAIMS_IN_REFRESH_TOKEN'] = True
    JWT.init_app(app)
    return AUTH


def get_user_role():
    """Return role of the current user."""
    return get_jwt_claims()['role']


@JWT.user_claims_loader
def get_user_claims(user):
    """Return claims of the given user."""
    return {'role': user['role']}


@JWT.user_identity_loader
def get_user_identity(user):
    """Return identity of the given user."""
    return user['username']


@AUTH.route('/login', methods=['POST'])
def login():  # pylint: disable=inconsistent-return-statements
    """Return a new fresh access and refresh token."""
    body = request.get_json()

    if not body or 'username' not in body or 'password' not in body:
        LOGGER.info('no username or password provided')
        abort(400)

    valid, role = _validate_login(body['username'], body['password'])
    if valid:
        return jsonify({
            'access_token': create_access_token(identity={'username': body['username'], 'role': role}, fresh=True),
            'refresh_token': create_refresh_token(identity={'username': body['username'], 'role': role})
        })

    LOGGER.info('username %s and password %s does not exist', body['username'], body['password'])
    abort(401)


@AUTH.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """Return a new non-fresh access token."""
    current_user_name = get_user_name()
    current_user_role = get_user_role()

    return jsonify({
        'access_token': create_access_token(identity={
            'username': current_user_name,
            'role': current_user_role
        }, fresh=False)
    })


@AUTH.route('/fresh-login', methods=['POST'])
def fresh_login():  # pylint: disable=inconsistent-return-statements
    """Return a new fresh access token."""
    body = request.get_json()

    if not body or 'username' not in body or 'password' not in body:
        LOGGER.info('no username or password provided')
        abort(400)

    valid, role = _validate_login(body['username'], body['password'])
    if valid:
        return jsonify({
            'access_token': create_access_token(identity={'username': body['username'], 'role': role}, fresh=True)
        })

    LOGGER.info('username %s and password %s does not exist', body['username'], body['password'])
    abort(401)


def _validate_login(req_username, req_password):
    access_credentials = SECRETS['access_credentials'].split(',')

    for access_credential in access_credentials:
        try:
            username, password, role = access_credential.split(':')
        except ValueError:
            LOGGER.warning('invalid credential found in secrets')
            continue

        if req_username == username and req_password == password:
            return True, role

    return False, None
