from .core import db
from toolspy import ist_now


class Segment(db.Model):

    __tablename__ = 'segment'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'))
    created_at = db.Column(db.DateTime())

    story = db.relationship("Story")

    def __init__(self, story_id=None):
        self.story_id = story_id
        self.created_at = ist_now()
