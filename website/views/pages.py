from flask import Blueprint, render_template, abort
from ..models import Story
from flask.ext.security import login_required


pages_bp = Blueprint('standalone_pages_bp', __name__)


@pages_bp.route('/')
def home():
    return render_template('index.html')


@pages_bp.route('/stories')
def index_stories():
    return render_template('stories.html')


@pages_bp.route('/stories/<story_id>')
@login_required
def get_story(story_id):
    story = Story.get(story_id)
    if story is None:
        abort(404)
    return render_template('story.html', story=story)
