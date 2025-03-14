from flask import Flask
from werkzeug.exceptions import HTTPException

from bebinca.configs import settings
from bebinca.utils.cors import cors
from bebinca.utils.tools import abort, jsonify_exc
from bebinca.utils.log_util import logger
from bebinca.utils.errors import ValidationError
from bebinca.views import user_view, chat_view


def create_app():
    app = Flask('bebinca')

    register_extensions(app)
    register_errors(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    cors.init_app(app)


def register_errors(app):
    @app.errorhandler(ValidationError)
    def validation_exception_handler(error):
        logger.opt(exception=True).info(error)
        return jsonify_exc(422)

    @app.errorhandler(HTTPException)
    def http_exception_handler(error):
        logger.opt(exception=True).info(error)
        return jsonify_exc(error.code)  # jsonify_exc(error.code, error.description)

    @app.errorhandler(Exception)
    def global_exception_handler(error):
        logger.exception(error)
        return abort(500)


def register_blueprints(app):
    app.register_blueprint(chat_view.route)
    app.register_blueprint(user_view.route, url_prefix='/user')


app = create_app()
