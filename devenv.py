from contextlib import contextmanager
from website.models import db, Story, Segment, Snippet, User, Role

import json

from website.app_factory import create_app

app = create_app()

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

# Needed for making the console work in app request context
ctx = app.test_request_context()
ctx.push()
# app.preprocess_request()

# The test client. You can do .get and .post on all endpoints
client = app.test_client()


q = db.session.query
add = db.session.add
addall = db.session.add_all
commit = db.session.commit
delete = db.session.delete

def create_first_story():
    s = Story.create(title = "my secret story", user_id = 1)
    return s.id
