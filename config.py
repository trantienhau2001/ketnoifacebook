import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config (object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "khong doan duoc dau"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:@localhost/demo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False