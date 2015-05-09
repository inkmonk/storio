from .core import db
from toolspy import ist_now


class Snippet(db.Model):

    __tablename__ = 'snippet'

    _attrs_to_serialize_ = ['id', 'text', 'story_id']
    _rels_to_serialize_ = [('user', 'name')]

    id = db.Column(db.Integer, primary_key=True, unique=True)
    text = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime())
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'))

    user = db.relationship("User")
    story = db.relationship("Story")

    def __init__(self, text=None, user_id=None, user=None,
                 story_id=None, story=None):
        self.text = text
        if user_id:
            self.user_id = user_id
        elif user:
            self.user = user
        self.created_at = ist_now()
        if story_id:
            self.story_id = story_id
        elif story:
            self.story = story
