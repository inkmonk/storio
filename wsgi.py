from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from website import app_factory, socketio

webapp = app_factory.create_app()

application = DispatcherMiddleware(webapp)


if __name__ == "__main__":
    socketio.run(webapp)
    # run_simple(
    #     '0.0.0.0', 5000, application,
    #     use_reloader=True, use_debugger=True, threaded=True)
