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


@pytest.mark.parametrize(
    "state, session, title, message",
    [
        (State.started, Sessions.pomodoro, "Pomodoro", "Get back to work!"),
        (State.started, Sessions.shortbreak, "Short Break", "It's coffee time!"),
        (State.started, Sessions.longbreak, "Long Break", "Step away from the machine!"),
        (State.stopped, Sessions.pomodoro, "Session stopped manually", ""),
        (State.finished, Sessions.pomodoro, "The time is up!", ""),
    ],
)
def test_show_notification_when_session_starts(state, session, title, message, subject):
    subject.activate()

    payload = SessionPayload(
        duration=0,
        id="",
        pomodoros=0,
        state=state,
        type=session,
    )

    Events.Session.send(state, payload=payload)

    subject.notification.update.assert_called_once_with(title, message, IconPath)
    subject.notification.show.assert_called_once()
