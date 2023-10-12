import importlib.metadata
import itertools
import typing

import flask
import flasgger

from . import base_types
from . import error_handlers
from . import plugins


app = flask.Flask(__name__)
app.register_blueprint(error_handlers.bp)
app.register_blueprint(plugins.bp)
app.config["SWAGGER"] = {
    "title": "Notification Router",
    "uiVersion": 3,
    "openapi": "3.0.2",
    "version": importlib.metadata.version("notification_router")
}
flasgger.Swagger(
    app,
    template={
        "openapi": "3.0.2",
        "info": {
            "title": "Notification Router",
            "description": "A webhook translator that converts support "
            "notification source to notification services.",
            "version": importlib.metadata.version("notification_router"),
            "license": {
                "name": "MIT License",
                "url": "https://github.com/jacky9813/notification_router/blob/master/LICENSE"
            }
        },
        "components": {
            "schemas": {
                "error": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The reason of the error."
                        },
                        "error": {
                            "type": "number",
                            "description": "The represented HTTP status code.",
                            "example": 200
                        }
                    }
                }
            },
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer"
                },
                "basicAuth": {
                    "type": "http",
                    "scheme": "basic"
                }
            }
        }
    }
)
@app.get("/")
def redirect_to_apidocs():
    return flask.redirect(flask.url_for("flasgger.apidocs"))

SUPPORTED_SOURCES: typing.Dict[str, base_types.NotificationSource] = {
    entry_point.name: entry_point.load()
    for entry_point in importlib.metadata.entry_points(
        group="notification_router.source_plugins"
    )
}
SUPPORTED_DESTINATIONS: typing.Dict[str, base_types.NotificationDestination] = {
    entry_point.name: entry_point.load()
    for entry_point in importlib.metadata.entry_points(
        group="notification_router.destination_plugins"
    )
}

@app.get("/notify")
@flasgger.swag_from({
    "responses": {
        "200": {
            "description": "Success",
            "schema": {
                "type": "object",
                "properties": {
                    k: {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                    for k in ["sources", "destinations"]
                }
            }
        }
    }
})
def list_available_plugins() -> flask.Response:
    """
    List available sources and destinations.
    """
    return flask.jsonify(
        {
            "sources": [src for src in SUPPORTED_SOURCES.keys()],
            "destinations": [dst for dst in SUPPORTED_DESTINATIONS.keys()]
        }
    )


@app.get("/notify/<plugin_name>")
def view_plugin_detail(plugin_name) -> flask.Response:
    response = []
    if plugin_name in SUPPORTED_SOURCES:
        response.append({
            "name": plugin_name,
            "type": "source",
            "description": (SUPPORTED_SOURCES[plugin_name].__doc__ or "").strip()
        })
    if plugin_name in SUPPORTED_DESTINATIONS:
        response.append({
            "name": plugin_name,
            "type": "destination",
            "description": (SUPPORTED_DESTINATIONS[plugin_name].__doc__ or "").strip()
        })
    
    if not response:
        flask.abort(404)

    return response
    
    



@app.post("/notify/<source>/<destination>")
@flasgger.swag_from({
    "parameters": [
        {
            "name": "source",
            "in": "path",
            "type": "string",
            "enum": [src for src in SUPPORTED_SOURCES.keys()],
            "required": "true"
        },
        {
            "name": "destination",
            "in": "path",
            "type": "string",
            "enum": [dst for dst in SUPPORTED_DESTINATIONS.keys()],
            "required": "true"
        }
    ],
    "responses": {
        "200": {"description": "Success"},
        "401": {"description": "Invalid access token"}
    },
    "security": [
        {"basicAuth": []},
        {"bearerAuth": []}
    ]
})
def route_notification(source: str, destination: str) -> flask.Response:
    """
    Retrieve request data and send it out to the destination with converted data.
    """
    if source not in SUPPORTED_SOURCES or destination not in SUPPORTED_DESTINATIONS:
        unsupported = list(itertools.chain(
            [src for src in [source] if src not in SUPPORTED_SOURCES],
            [dst for dst in [destination] if dst not in SUPPORTED_DESTINATIONS]
        ))

        return base_types.ErrorResponse(
            error_message=f'Unsupported source and / or destination: {", ".join(unsupported)}'
        )
    src: base_types.NotificationSource = SUPPORTED_SOURCES[source]()
    dst: base_types.NotificationDestination = SUPPORTED_DESTINATIONS[destination]()

    return dst.notify(src)


