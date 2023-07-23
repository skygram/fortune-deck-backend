import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    FAQ_FILE_UPLOAD_DIR = '/flask_chatbot/chatbot/upload'
    ML_VARS_DIR = '/flask_chatbot/chatbot/ml_vars'

    CELERY = {
        'broker': 'redis://redis:6379',
        'backend': 'redis://redis:6379',
        'imports': ['chatbot.admin.domain.tasks'],
    }


class ProductionConfig(Config):

    # SQLAlchemy
    dbCOnfig = {
        'user': 'skygram',
        'password': 'Sjtu24365!',
        'host': 'fd-db-server.mysql.database.azure.com',
        'database': 'fd_db_chat_history',
    }
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8'.format(
        **dbCOnfig)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    TESTING = True


def get_config():

    return ProductionConfig()
