from flask.ext.security import login_required
from flask import Blueprint


def create_api_bp(
        name='json', authenticator=login_required):

    api_bp = Blueprint(name, __name__)

    return api_bp
