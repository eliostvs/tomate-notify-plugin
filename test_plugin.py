from unittest.mock import Mock, patch

import pytest

from tomate.config import Config
from tomate.constant import Sessions, State
from tomate.event import Events
from tomate.graph import graph
from tomate.session import SessionPayload


def setup_function(function):
    graph.providers.clear()

    graph.register_instance(
        "tomate.config",
        Mock(
            spec=Config, **{"get_icon_path.return_value": "/path/to/mock/32/tomate.png"}
        ),
    )

    Events.Session.receivers.clear()


@pytest.fixture()
def plugin(mocker):
    with mocker.patch("gi.repository.Notify.Notification.new"):
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
    # given
    plugin.activate()

    session_type = Sessions.pomodoro
    title = plugin.messages[session_type.name]["title"]
    message = plugin.messages[session_type.name]["content"]

    payload = SessionPayload(
        type=session_type, sessions=[], state=State.started, duration=0, task=0
    )

    # when
    Events.Session.send(State.started, payload=payload)

    # then
    plugin.notification.update.assert_called_once_with(
        title, message, "/path/to/mock/32/tomate.png"
    )

    plugin.notification.show.assert_called_once()


def test_show_notification_when_sessions_ends(plugin):
    # given
    plugin.activate()

    # when
    Events.Session.send(State.finished)

    # then
    plugin.notification.update.assert_called_once_with(
        "The time is up!", "", "/path/to/mock/32/tomate.png"
    )

    plugin.notification.show.assert_called_once()


def test_show_notification_when_session_stops(plugin):
    # given
    plugin.activate()

    # when
    Events.Session.send(State.stopped)

    # then
    plugin.notification.update.assert_called_once_with(
        "Session stopped manually", "", "/path/to/mock/32/tomate.png"
    )

    # then
    plugin.notification.show.assert_called_once()
