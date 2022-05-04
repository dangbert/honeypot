# this file contains configuration settings for flask
import os
from passlib.context import CryptContext
baseDir = os.path.abspath(os.path.dirname(__file__))

SECRET = 'cb841fe3c50f2b1df6dc6fc3e34b1d7181909d0cbfac230539578684a890cacf'

CTX = CryptContext(
    schemes=["argon2"],
    argon2__rounds = 25
)

class BaseConfig(object):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = SECRET
    #SQLALCHEMY_DATABASE_URI = "postgresql://" + db_user + ":" + db_pw + "@localhost/" + db_name
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

    SAVE_DIR = os.path.join(baseDir, 'data')
    REDIRECT_URL = os.environ.get('REDIRECT_URL')


# inherits from BaseConfig class
# TODO: consider using flask-paranoid
#   https://blog.miguelgrinberg.com/post/cookie-security-for-flask-applications
class ProductionConfig(BaseConfig):
    DEBUG = False
    # https://blog.miguelgrinberg.com/post/cookie-security-for-flask-applications
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True


class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True