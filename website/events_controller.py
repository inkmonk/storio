from flask.ext.socketio import SocketIO
socketio = SocketIO()
from flask.ext.socketio import emit, send, join_room, leave_room
from .authenticators import authenticated_socket
from flask.ext.security import current_user
from .models import Segment, Snippet


@socketio.on('connect')
def connect_user(data):
    print data
    emit('welcome', {'data': 'Connected'})


@socketio.on('join')
@authenticated_socket
def on_join(data):
    story_id = data['story_id']
    join_room(story_id)
    emit('user_joined', {'user': current_user.name}, room=story_id)


@socketio.on('leave')
@authenticated_socket
def on_leave(data):
    story_id = data['story_id']
    leave_room(story_id)
    send(current_user.name + ' has left the room.', room=story_id)
    emit('user_left', {'user': current_user.name}, room=story_id)


@socketio.on('modify_snippet_text')
@authenticated_socket
def on_modify_snippet_text(data):
    emit('user_modified_snippet_text', {
        'user': current_user.name,
        'text': data['text'],
        'segment_id': data['segment_id']
        }, room=data['story_id'])


@socketio.on('submit_snippet')
@authenticated_socket
def on_submit_snippet(data):
    segment_id = data['segment_id']
    text = data['text']
    segment = Segment.get(segment_id)
    if len(segment.snippets) == 0:
        snippet = Snippet.create(
            segment_id=segment_id,
            text=text, is_first=True)
        emit('handover_snippet', {
            'segment_id': segment_id,
            'first_snippet': snippet.todict(),
            })
