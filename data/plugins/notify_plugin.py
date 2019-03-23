import logging
from locale import gettext as _

import gi

gi.require_version("Notify", "0.7")

from gi.repository import Notify

import tomate.plugin
from tomate.constant import Sessions, State
from tomate.session import SessionPayload
from tomate.event import Events, on
from tomate.graph import graph
from tomate.utils import suppress_errors

logger = logging.getLogger(__name__)


class NotifyPlugin(tomate.plugin.Plugin):
    messages = {
        "pomodoro": {"title": _("Pomodoro"), "content": _("Get back to work!")},
        "shortbreak": {"title": _("Short Break"), "content": _("It's coffee time!")},
        "longbreak": {
            "title": _("Long Break"),
            "content": _("Step away from the machine!"),
        },
    }

    @suppress_errors
    def __init__(self):
        super(NotifyPlugin, self).__init__()
        self.config = graph.get("tomate.config")
        self.notification = Notify.Notification.new("tomate-notify-plugin")

    @suppress_errors
    def activate(self):
        super(NotifyPlugin, self).activate()
        Notify.init("tomate-notify-plugin")

    @suppress_errors
    def deactivate(self):
        super(NotifyPlugin, self).deactivate()
        Notify.uninit()

    @on(Events.Session, [State.started])
    def on_session_started(self, _, payload: SessionPayload):
        self.show_notification(*self.get_message(payload.type))

    @on(Events.Session, [State.finished])
    def on_session_finished(self, *args, **kwargs):
        self.show_notification(title="The time is up!")

    @on(Events.Session, [State.stopped])
    def on_session_stopped(self, *args, **kwargs):
        self.show_notification(title="Session stopped manually")

    def get_message(self, session_type: Sessions):
        return (
            self.messages[session_type.name]["title"],
            self.messages[session_type.name]["content"],
        )

    @suppress_errors
    def show_notification(self, title, message=""):
        self.notification.update(title, message, self.icon_path)
        result = self.notification.show()

        logger.debug(
            'component=notification action=show title="%s" message="%s" success=%r icon=%s',
            title,
            message,
            result,
            self.icon_path,
        )

    @property
    def icon_path(self):
        return self.config.get_icon_path("tomate", 32)
