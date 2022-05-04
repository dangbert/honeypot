import os
from flask import Flask
from config import ProductionConfig, DevelopmentConfig, TestingConfig

def getConfigForEnv():
    """get appropriate config Class based on ENV variable"""
    if 'ENV' in os.environ and os.environ['ENV'] == "dev":
        print("USING DEV ENV CONFIG!!!")
        return DevelopmentConfig
    elif 'ENV' in os.environ and os.environ['ENV'] == "test":
        print("USING TEST ENV CONFIG")
        return TestingConfig
    print("Using prod env config.")
    return ProductionConfig

def create_app(configClass=ProductionConfig):
    """
    factory for creating an application object with the desire config.
    (useful for testing to be able to create separate application objects).

    inspired by https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
    https://github.com/miguelgrinberg/microblog/blob/6e63377838a573e853249ebb4a86ff09f7e9e500/app/__init__.py#L28
    https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/
    """
    app = Flask(__name__)
    app.config.from_object(configClass)
    # register blueprints:
    from app.blueprints import tracker
    app.register_blueprint(tracker.bp, url_prefix="/")

    print("\ncreated app:")
    print("SAVE_PATH = '{}'".format(configClass.SAVE_DIR))
    return app
