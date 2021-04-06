import os
from unittest.mock import patch

import gi
import pytest
from blinker import NamedSignal
from tomate.pomodoro.config import Config
from tomate.pomodoro.event import Events
from tomate.pomodoro.graph import graph
from tomate.pomodoro.session import Payload as SessionPayload, Type as SessionType

gi.require_version("Notify", "0.7")

IconPath = os.path.join(os.path.dirname(__file__), "data", "icons", "hicolor", "32x32", "apps", "tomate.png")


@pytest.fixture
def bus():
    return NamedSignal("Test")


@pytest.fixture()
@patch("gi.repository.Notify.Notification.new")
def subject(_, bus):
    graph.providers.clear()
    graph.register_instance("tomate.bus", bus)
    graph.register_instance("tomate.config", Config(bus))

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
    "event,session,title,message",
    [
        (Events.SESSION_START, SessionType.POMODORO, "Pomodoro", "Get back to work!"),
        (Events.SESSION_START, SessionType.SHORT_BREAK, "Short Break", "It's coffee time!"),
        (Events.SESSION_START, SessionType.LONG_BREAK, "Long Break", "Step away from the machine!"),
        (Events.SESSION_INTERRUPT, SessionType.POMODORO, "Session stopped manually", ""),
        (Events.SESSION_END, SessionType.POMODORO, "The time is up!", ""),
    ],
)
def test_show_notification_when_session_starts(event, session, title, message, bus, subject):
    subject.activate()

    payload = SessionPayload(
        duration=0,
        id="",
        pomodoros=0,
        type=session,
    )

    bus.send(event, payload=payload)

    subject.notification.update.assert_called_once_with(title, message, IconPath)
    subject.notification.show.assert_called_once()
