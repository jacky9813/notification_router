import flask
from notification_router import base_types

class EchoDestination(base_types.NotificationDestination):
    """
    A destination that echoes the source generated text straight into the response of the call.
    """
    def notify(self, source: base_types.NotificationSource) -> flask.Response:
        return flask.Response(
            source.to_text(),
            mimetype="text/plain"
        )
