from unittest.mock import Mock, patch

import gi
import pytest

from tomate.pomodoro import Sessions, State
from tomate.pomodoro.config import Config
from tomate.pomodoro.event import Events
from tomate.pomodoro.graph import graph
from tomate.pomodoro.session import Payload as SessionPayload

gi.require_version("Notify", "0.7")


def setup_function():
    graph.providers.clear()

    graph.register_instance(
        "tomate.config",
        Mock(spec=Config, **{"icon_path.return_value": "/path/to/mock/32/tomate.png"}),
    )

    Events.Session.receivers.clear()


@pytest.fixture()
@patch("gi.repository.Notify.Notification.new")
def plugin(_):
    from notify_plugin import NotifyPlugin

    return NotifyPlugin()


@patch("gi.repository.Notify.init")
def test_enable_notify_when_plugin_active(init, plugin):
    plugin.activate()

    init.assert_called_with("tomate-notify-plugin")


@patch("gi.repository.Notify.uninit")
def test_disable_notify_when_plugin_deactivate(uninit, plugin):
    plugin.deactivate()

    uninit.assert_called_with()


def test_show_notification_when_session_starts(plugin):
    plugin.activate()

    session_type = Sessions.pomodoro
    title = plugin.messages[session_type.name]["title"]
    message = plugin.messages[session_type.name]["content"]

    payload = SessionPayload(
        id="1234",
        state=State.started,
        type=Sessions.pomodoro,
        pomodoros=0,
        duration=25 * 60,
        task="",
    )

    Events.Session.send(State.started, payload=payload)

    plugin.notification.update.assert_called_once_with(
        title, message, "/path/to/mock/32/tomate.png"
    )

    plugin.notification.show.assert_called_once()


def test_show_notification_when_sessions_ends(plugin):
    plugin.activate()

    Events.Session.send(State.finished)

    plugin.notification.update.assert_called_once_with(
        "The time is up!", "", "/path/to/mock/32/tomate.png"
    )
    plugin.notification.show.assert_called_once()


def test_show_notification_when_session_stops(plugin):
    plugin.activate()

    Events.Session.send(State.stopped)

    plugin.notification.update.assert_called_once_with(
        "Session stopped manually", "", "/path/to/mock/32/tomate.png"
    )
    plugin.notification.show.assert_called_once()
