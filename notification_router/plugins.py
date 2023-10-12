import importlib.metadata

import flask

bp = flask.Blueprint("plugins", __name__)


for entry_point in importlib.metadata.entry_points(group="notification_router.plugin_endpoints"):
    plugin_bp = flask.Blueprint(entry_point.name, __name__, url_prefix=f"/{entry_point.name}")
    plugin_bp.register_blueprint(entry_point.load())
    bp.register_blueprint(plugin_bp)
