from flask.ext.socketio import SocketIO
socketio = SocketIO()
from flask.ext.socketio import emit


@socketio.on('connect')
def connect_user(data):
    print data
    emit('welcome', {'data': 'Connected'})
