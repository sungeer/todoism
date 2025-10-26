from flask import Flask, request

from todoism import settings
from todoism.blueprints.home import home_bp
from todoism.blueprints.todo import todo_bp
from todoism.cores.core_http import abort


def create_app():
    app = Flask('todoism')

    app.config.from_object(settings)

    register_blueprints(app)
    register_errors(app)
    return app


def register_blueprints(app):
    app.register_blueprint(todo_bp)
    app.register_blueprint(home_bp)


def register_errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return abort(404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return abort(405)

    @app.errorhandler(500)
    def internal_server_error(e):
        return abort(500)
