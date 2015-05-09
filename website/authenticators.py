from flask import request, abort
import base64
import hmac
from hashlib import sha512
import logging
from functools import wraps
from models import User
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from base64 import b64decode
from flask_login import login_user, logout_user


def get_signature(secret_key, request):
    path = (request.path[5:] if request.path.startswith('/api/')
            else request.path)
    message = "{0}:{1}:{2}".format(
        request.method, path, request.headers['Content-Type'])
    result = hmac.new(str(secret_key), str(message), sha512)
    return result.hexdigest()


def with_signed_authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' in request.headers:
            api_key, signature = b64decode(
                request.headers['Authorization']).split(":")
            try:
                user = User.first(api_key=api_key)
            except Exception as e:
                logging.exception(e)
                abort(401, description="No such User found")
            if signature == get_signature(user.secret_key, request):
                login_user(user)
                result = func(*args, **kwargs)
                logout_user()
                return result
            else:
                logging.error(request.headers)
                abort(401)
        else:
            logging.error(request.headers)
            abort(401)
    return wrapper


def with_basic_authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' in request.headers:
            encoded_key = request.headers['Authorization'].split()[1]
            api_key = base64.b64decode(encoded_key).rstrip(':')
            try:
                user = User.first(api_key=api_key)
                login_user(user)
            except (NoResultFound, MultipleResultsFound) as e:
                logging.exception(e)
                abort(401)
            result = func(*args, **kwargs)
            logout_user()
            return result
        else:
            logging.error(request.headers)
            abort(401)
    return wrapper
