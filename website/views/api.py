from flask.ext.security import login_required, current_user
from flask import Blueprint, request
from flask_sqlalchemy_plus.responses import as_processed_list, as_obj
from ..models import Story, Snippet


@as_processed_list
def list_stories():
    return Story


@as_obj
def get_story(story_id):
    return Story.first(id=story_id, user_id=current_user.id)


@as_obj
def create_story():
    """
    POST /json/stories

    {
        'title': <title of story>
    }
    """
    json_data = request.get_json()
    return Story.create(title=json_data['title'])


@as_obj
def create_snippet(story_id):
    """
    POST /json/stories/<story_id>/snippets

    {
        'text': 'snippet text'
    }
    """
    json_data = request.get_json()
    return Snippet.create(
        text=json_data['text'],
        user_id=current_user.id,
        story_id=story_id)


def create_api_bp(
        name='json', authenticator=login_required):

    api_bp = Blueprint(name, __name__)

    api_bp.route('/stories', methods=['GET'], endpoint='list_stories')(
        list_stories)
    api_bp.route('/stories/<story_id>', methods=['GET'], endpoint='get_story')(
        get_story)
    api_bp.route('/stories', methods=['POST'], endpoint='create_story')(
        authenticator(create_story))
    api_bp.route('/stories/<story_id>/snippets', methods=['POST'],
                 endpoint='create_snippet')(
        authenticator(create_snippet))

    return api_bp
