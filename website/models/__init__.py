from .core import db

from flask.ext.security import SQLAlchemyUserDatastore

from .user import User, Role
from .snippet import Snippet
from .story import Story


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
