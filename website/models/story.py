from .core import db
from toolspy import ist_now


class Story(db.Model):

    __tablename__ = 'story'

    _attrs_to_serialize_ = ['title', 'created_at']

    _rels_to_expand_ = ['segments']

    _rels_to_serialize_ = [('user', 'email')]

    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.Unicode(100))
    created_at = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    segments = db.relationship("Segment")
    user = db.relationship("User")

    def __init__(self, title=None, user_id=None):
        self.title = title
        self.created_at = ist_now()
        self.user_id = user_id
