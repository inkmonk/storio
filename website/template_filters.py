"""
Custom filters for use in Jinja2 templates
"""
import time
import hashlib
import hmac
from flask.json import _json
from flask_sqlalchemy_plus.responses import _json_encoder


def timestampize(dt):
    return time.mktime(dt.timetuple())


def hash_hmac(message, secret_key, algo_name):
    return hmac.new(
        secret_key, message, getattr(hashlib, algo_name)).hexdigest()


def json_dumps(obj):
    return _json.dumps(obj, default=_json_encoder)


def todict(
        item, rels_to_expand=None, attrs_to_serialize=None,
        rels_to_serialize=None, group_listrels_by=None):
    if item is None:
        return None
    if isinstance(item, list):
        return[m.todict(
            rels_to_expand=rels_to_expand,
            attrs_to_serialize=attrs_to_serialize,
            rels_to_serialize=rels_to_serialize,
            group_listrels_by=group_listrels_by) for m in item]
    return item.todict(
        rels_to_expand=rels_to_expand,
        attrs_to_serialize=attrs_to_serialize,
        rels_to_serialize=rels_to_serialize,
        group_listrels_by=group_listrels_by)
