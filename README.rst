###################
Notification Router
###################

Transform an incoming webhook content to a supported notification service.

===================
Recommended Plugins
===================

Notification Source
===================

* AWS Resource State Change via EventBridge (Planned for EC2 and RDS)
* AWS CloudWatch with AWS SNS (Planned)
* Google Cloud Compute Engine VM State Change via Cloud Logging Sink and Cloud Pub/Sub (Planned)
* Google Cloud Monitoring (Planned)
* Uptime Kuma (Planned)

Notification Destination
========================

.. _LINE Notify: https://github.com/jacky9813/notification_router_plugin_line_notify

* `LINE Notify`_, using text format
* Mattermost, using Markdown format(Planned)
* Opsgenie, which requires customized convertion function (Planned)
* Telegram, using text format (Planned)
