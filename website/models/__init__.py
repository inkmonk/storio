from .core import db

from flask.ext.security import SQLAlchemyUserDatastore

from .user import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
