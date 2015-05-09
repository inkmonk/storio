from .core import db
from toolspy import ist_now


class Snippet(db.Model):

    __tablename__ = 'snippet'

    _attrs_to_serialize_ = ['text', 'segment_id', 'is_first', 'created_at']
    _rels_to_serialize_ = [('user', 'name')]

    id = db.Column(db.Integer, primary_key=True, unique=True)
    text = db.Column(db.UnicodeText)
    is_first = db.Column(db.Boolean())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime())
    segment_id = db.Column(db.Integer, db.ForeignKey('segment.id'))

    user = db.relationship("User")
    segment = db.relationship("Segment")

    def __init__(self, text=None, user_id=None, user=None,
                 segment_id=None, segment=None,
                 is_first=False):
        self.text = text
        if user_id:
            self.user_id = user_id
        elif user:
            self.user = user
        self.created_at = ist_now()
        if segment_id:
            self.segment_id = segment_id
        elif segment:
            self.segment = segment
        self.is_first = is_first

