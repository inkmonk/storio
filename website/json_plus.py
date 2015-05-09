from datetime import datetime
from decimal import Decimal
from .models import db
from flask.json import _json
from .utils import is_list_like, is_dict_like, dict_map
from flask import current_app


def json_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return str(obj)
    elif isinstance(obj, unicode):
        return obj
    elif isinstance(obj, db.Model):
        return obj.todict()
    elif is_list_like(obj):
        return [json_encoder(i) for i in obj]
    elif is_dict_like(obj):
        return dict_map(obj, lambda v: json_encoder(v))
    else:
        try:
            return _json.JSONEncoder().default(obj)
        except Exception as e:
            current_app.logger.debug("Cannot serialize")
            current_app.logger.debug(obj)
            current_app.logger.debug(type(obj))
            current_app.logger.debug(e)
            return unicode(obj)
