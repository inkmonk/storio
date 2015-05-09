from .core import db
from toolspy import ist_now


class Story(db.Model):

    __tablename__ = 'story'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.Unicode(100))
    created_at = db.Column(db.DateTime())

    snippets = db.relationship("Snippet")

    def __init__(self, title=None, user_id=None):
        self.title = title
        self.created_at = ist_now()
