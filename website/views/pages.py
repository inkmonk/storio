from flask import (
    Blueprint, render_template, abort, request, redirect,
    url_for)
from ..models import Story
from flask.ext.security import login_required, current_user


pages_bp = Blueprint('standalone_pages_bp', __name__)


# @pages_bp.route('/')
# def home():
#     return render_template('index.html')


@pages_bp.route('/')
@login_required
def index_stories():
    stories = Story.all()
    return render_template(
        'stories.html', stories=stories)


@pages_bp.route('/stories/<story_id>')
@login_required
def get_story(story_id):
    story = Story.get(story_id)
    if story is None:
        abort(404)
    return render_template('story.html', story=story)


@pages_bp.route('/stories', methods=['POST'])
@login_required
def create_story():
    if 'title' in request.form:
        story = Story.create(
            title=request.form['title'],
            user_id=current_user.id)
        return redirect(url_for('.get_story', story_id=story.id))
    else:
        abort(400)


@pages_bp.route('/stories/angular-notify.html')
def notify():
    return render_template('angular-notify.html')
