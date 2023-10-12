import typing
import http
import urllib.parse

import flask


def ErrorResponse(
    error_message: str,
    status: typing.Union[int, str, http.HTTPStatus]
) -> flask.Response:
    """
    :param error_message: A string that contains the reason of the error.
    :param status: The status code form the response. Can be int or a str formatted
        in the form ``{code} {message}``, like ``404 Not Found``. Defaults to 400.
    """
    if isinstance(status, str):
        try:
            status_code = int(status.split(" ")[0])
        except ValueError:
            status_code = 400
        if status_code >= 100 and status_code < 600:
            status = status_code
    if not isinstance(status, int):
        try:
            status = int(status)
        except ValueError:
            status = 400

    response = flask.jsonify({
        "error": status,
        "message": error_message
    })
    response.status_code = status
    return response


class NotificationPlugin:
    name: str = "notification-plugin"

    def render_documentation(self) -> flask.Response:
        raise NotImplementedError()


class NotificationSource(NotificationPlugin):
    def __init__(self):
        self.data = flask.request.data or flask.request.get_data(as_text=False)

    def to_text(self) -> str:
        raise NotImplementedError()

    def to_markdown(self, tablefmt: typing.Optional[str] = None) -> str:
        raise NotImplementedError()
    
    @property
    def authorization(self):
        return flask.request.authorization
    

class JsonSource(NotificationSource):
    def __init__(self):
        self.data = flask.request.get_json(force=True)


class UrlEncodedBodySource(NotificationSource):
    def __init__(self):
        self.data = urllib.parse.parse_qs(flask.request.get_data(as_text=True))


class NotificationDestination(NotificationPlugin):
    def notify(
        self,
        source: NotificationSource
    ) -> flask.Response:
        raise NotImplementedError()
