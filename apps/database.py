import logging
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate


db = SQLAlchemy()

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def init_db(app):
    db.init_app(app)
    Migrate(app, db)
