from flask import Flask
from .views import create_api_bp, pages_bp
from .models import db, user_datastore
from authenticators import with_basic_authentication
from flask.ext.security import Security

security = Security()


def create_app(database=db):
    app = Flask(__name__)
    app.config.from_object('website.config')
    database.init_app(app)

    security.init_app(app, user_datastore)

    app.register_blueprint(pages_bp)
    app.register_blueprint(create_api_bp(), url_prefix='/json')
    app.register_blueprint(create_api_bp(
        name='api', authenticator=with_basic_authentication))
    return app
