from flask import Flask
from .views import create_api_bp, pages_bp
from .models import db, user_datastore
from authenticators import with_basic_authentication
from .core import security
from .events_controller import socketio
import template_filters
from .forms import LoginForm


def create_app(database=db):
    app = Flask(__name__)
    app.config.from_object('website.config')
    app.config.from_envvar('STORIO_CONFIG')
    database.init_app(app)

    security.init_app(
        app, user_datastore,
        login_form=LoginForm,
        register_form=LoginForm,
        confirm_register_form=LoginForm,
        )
    socketio.init_app(app)

    app.register_blueprint(pages_bp)
    app.register_blueprint(create_api_bp(), url_prefix='/json')
    app.register_blueprint(create_api_bp(
        name='api', authenticator=with_basic_authentication))
    app.jinja_env.filters['timestampize'] = template_filters.timestampize
    app.jinja_env.filters['hash_hmac'] = template_filters.hash_hmac
    app.jinja_env.filters['json'] = template_filters.json_dumps
    app.jinja_env.filters['todict'] = template_filters.todict
    return app
