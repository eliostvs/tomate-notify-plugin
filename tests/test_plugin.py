import os
from unittest.mock import patch

import gi
import pytest
from blinker import Namespace
from tomate.pomodoro import Sessions, State
from tomate.pomodoro.config import Config
from tomate.pomodoro.event import Events
from tomate.pomodoro.graph import graph
from tomate.pomodoro.session import Payload as SessionPayload

gi.require_version("Notify", "0.7")

IconPath = os.path.join(
    os.path.dirname(__file__), "data", "icons", "hicolor", "32x32", "apps", "tomate.png"
)


@pytest.fixture()
def dispatcher():
    return Namespace().signal("dispatcher")


@pytest.fixture()
@patch("gi.repository.Notify.Notification.new")
def subject(_, dispatcher):
    graph.providers.clear()
    graph.register_instance("tomate.config", Config(dispatcher))
    Events.Session.receivers.clear()

    from notify_plugin import NotifyPlugin

    return NotifyPlugin()


@patch("gi.repository.Notify.init")
def test_enable_notify_when_plugin_active(init, subject):
    subject.activate()

    init.assert_called_with("tomate-notify-plugin")


@patch("gi.repository.Notify.uninit")
def test_disable_notify_when_plugin_deactivate(uninit, subject):
    subject.deactivate()

    uninit.assert_called_with()


def test_show_notification_when_session_starts(subject):
    subject.activate()

    session_type = Sessions.pomodoro
    title = subject.messages[session_type.name]["title"]
    message = subject.messages[session_type.name]["content"]

    payload = SessionPayload(
        id="1234",
        state=State.started,
        type=Sessions.pomodoro,
        pomodoros=0,
        duration=25 * 60,
    )

    Events.Session.send(State.started, payload=payload)

    subject.notification.update.assert_called_once_with(title, message, IconPath)

    subject.notification.show.assert_called_once()


def test_show_notification_when_sessions_ends(subject):
    subject.activate()

    Events.Session.send(State.finished)

    subject.notification.update.assert_called_once_with("The time is up!", "", IconPath)
    subject.notification.show.assert_called_once()


def test_show_notification_when_session_stops(subject):
    subject.activate()

    Events.Session.send(State.stopped)

    subject.notification.update.assert_called_once_with("Session stopped manually", "", IconPath)
    subject.notification.show.assert_called_once()
