import datetime
import typing

from tabulate import tabulate

from notification_router import base_types


class SampleSource(base_types.NotificationSource):
    """
    A source sample that response current time with message.
    """
    def to_text(self) -> str:
        return "\n".join([
            "This is a sample notification from Notification Router.",
            f'Time: {datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}'
        ])
    
    def to_markdown(self, tablefmt: typing.Optional[str] = None) -> str:
        return tabulate(
            [
                ["Message", "This is a sample notification from Notification Router in Markdown format."],
                ["Time", datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")]
            ],
            [
                "Property",
                "Value"
            ],
            tablefmt=tablefmt or "github"
        )
