from flask.ext.socketio import SocketIO
socketio = SocketIO()
from flask.ext.socketio import emit, send, join_room, leave_room
from .authenticators import authenticated_socket
from flask.ext.security import current_user


@socketio.on('connect')
def connect_user(data):
    print data
    emit('welcome', {'data': 'Connected'})


@socketio.on('join')
@authenticated_socket
def on_join(data):
    story = data['story_id']
    join_room(story)
    send(current_user.name + ' has entered the room.', room=story)


@socketio.on('leave')
@authenticated_socket
def on_leave(data):
    story = data['story_id']
    leave_room(story)
    send(current_user.name + ' has left the room.', room=story)
