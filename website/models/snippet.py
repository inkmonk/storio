from .core import db
from toolspy import ist_now


class Snippet(db.Model):

    __tablename__ = 'snippet'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    text = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime())

    user = db.relationship("User")

    def __init__(self, text=None, user_id=None):
        self.text = text
        self.user_id = user_id
        self.created_at = ist_now()
