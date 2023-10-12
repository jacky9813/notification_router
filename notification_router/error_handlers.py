import traceback

import flask
import werkzeug.exceptions

from . import base_types

bp = flask.Blueprint("error_handler", __name__)


@bp.app_errorhandler(werkzeug.exceptions.NotFound)
@bp.app_errorhandler(404)
def not_registered_method(e):
    return base_types.ErrorResponse("Not Found", 404)


@bp.app_errorhandler(werkzeug.exceptions.MethodNotAllowed)
@bp.app_errorhandler(405)
def not_registered_method(e):
    return base_types.ErrorResponse("Method Not Allowed", 405)


@bp.app_errorhandler(Exception)
@bp.app_errorhandler(500)
def general_exception(e):
    flask.current_app.logger.error(traceback.format_exc())
    return base_types.ErrorResponse("Internal Server Error", 500)
