from dynaconf import settings
from flask import Flask
from flask_cors import CORS

from .search_api import search_api


class Config:
    """Set Flask configuration vars."""

    DEBUG = settings.FLASK_CONFIG.DEBUG


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization,x-api-key"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,OPTION,PUT,POST,DELETE"
        )
        return response

    app.register_blueprint(search_api)

    return app
