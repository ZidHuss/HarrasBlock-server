from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from config import config

db = SQLAlchemy()


def add_cors_headers(response):
    """
    Setup response headers for api requests
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = (
        'Origin, '
        'X-Requested-With, Content-Type, Accept')
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


def create_app(config_name):
    """
    Flask app factory
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    api = Api(prefix='/api')
    db.init_app(app)

    add_resources(api)

    api.init_app(app)
    # Make api globally accessible
    app.api = api
    # Cross Origin requests
    app.after_request(add_cors_headers)

    return app


def add_resources(api):
    from .resources import SiteResource, AnalyzeResource, VoteResource

    api.add_resource(SiteResource, '/site/<int:id>', endpoint='site')
    api.add_resource(AnalyzeResource, '/analyze', endpoint='analyze')
    api.add_resource(VoteResource, '/vote', endpoint='vote')
