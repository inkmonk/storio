from flask.ext.socketio import SocketIO
socketio = SocketIO()
from flask.ext.socketio import emit, send, join_room, leave_room
from .authenticators import authenticated_socket
from flask.ext.security import current_user
from .models import Segment, Snippet, Story

"""
EVENTS:

    CLIENT EMITS:

    join
    ----
    {
        'story_id': 1
    }

    SERVER EMITS

    welcome
    -------
    {
        'current_segment_id': 12
    }

    SERVER BROADCASTS:

    user_joined
    -----------
    {
        'user': 'sibi'
    }

    CLIENT EMITS:

    leave
    -----
    {
        'story_id': 1
    }

    SERVER BROADCASTS:

    user_left
    -----------
    {
        'user': 'sibi'
    }

    CLIENT EMITS:
    (Every time text changes)

    modify_snippet_text
    -------------------

    {
        'story_id': 1,
        'segment_id': 13,
        'text': 'Hello worl'
    }

    SERVER BROADCASTS:

    user_modified_snippet_text
    --------------------------
    {
       'user': 'sibi',
       'text': 'Hello worl',
       'seigment_id': 13
    }

    CLIENT EMITS:

    submit_snippet
    --------------
    {
        'story_id': 1,
        'segment_id': 13,
        'text': 'Hello world. I finished my snippet'
    }

    SERVER BROADCASTS:

    handover_snippet_and_start_next_segment
    ---------------------------------------
    {
        'current_segment_id': 13,
        'first_snippet': {
            'segment_id': 13,
            'text': 'Hello world. I finished my snippet',
            'is_first': true,
            'user': 'sibi'
        },
        'next_segment_id': 14

    }

    SERVER BROADCASTS

    append_snippet
    ---------------
    {
        'segment_id': 13,
        'snippet': {
            'segment_id': 13,
            'text': 'Hello world. i am slow',
            'is_first': false,
            'user': 'surya'
        }

    }




"""


@socketio.on('join')
@authenticated_socket
def on_join(data):
    story_id = data['story_id']
    current_segment = Segment.last(story_id=story_id)
    if current_segment is None:
        current_segment = Segment.create(story_id=story_id)
    join_room(story_id)
    emit('welcome', {
        'current_segment_id': current_segment.id
        }, room=story_id)
    emit('user_joined', {
        'user': current_user.email,
        }, broadcast=True, room=story_id)


@socketio.on('leave')
@authenticated_socket
def on_leave(data):
    story_id = data['story_id']
    leave_room(story_id)
    send(current_user.email + ' has left the room.', room=story_id)
    emit('user_left', {'user': current_user.email},
         room=story_id, broadcast=True)


@socketio.on('modify_snippet_text')
@authenticated_socket
def on_modify_snippet_text(data):
    emit('user_modified_snippet_text', {
        'user': current_user.email,
        'text': data['text'],
        'segment_id': data['segment_id']
        }, room=data['story_id'], broadcast=True)


@socketio.on('submit_snippet')
@authenticated_socket
def on_submit_snippet(data):
    segment_id = data['segment_id']
    story_id = data['story_id']
    text = data['text']
    segment = Segment.get(segment_id)
    if len(segment.snippets) == 0:
        snippet = Snippet.create(
            segment_id=segment_id,
            text=text, is_first=True)
        next_segment = Segment.create(story_id)
        emit('handover_snippet_and_start_next_segment', {
            'current_segment_id': segment_id,
            'first_snippet': snippet.todict(),
            'next_segment_id': next_segment.id
            }, broadcast=True, room=data['story_id'])
    else:
        snippet = Snippet.create(
            segment_id=segment_id,
            text=text)
        emit('append_snippet', {
            'segment_id': segment_id,
            'snippet': snippet.todict()
            }, broadcast=True, room=data['story_id'])
