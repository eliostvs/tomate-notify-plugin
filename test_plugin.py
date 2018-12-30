from unittest.mock import Mock, patch

import pytest
from tomate.config import Config
from tomate.constant import Sessions, State
from tomate.event import Events
from tomate.graph import graph


def method_called(result):
    return result[0][0]


def setup_function(function):
    graph.providers.clear()

    graph.register_instance('tomate.config', Mock(spec=Config))

    Events.Session.receivers.clear()


@pytest.fixture()
def plugin():
    from notify_plugin import NotifyPlugin

    return NotifyPlugin()


@patch('gi.repository.Notify.init')
def test_init_dbus(init, plugin):
    plugin.activate()

    init.assert_called_with('Tomate')


@patch('gi.repository.Notify.uninit')
def test_uninit_dbus(uninit, plugin):
    plugin.deactivate()

    uninit.assert_called_with()


def test_get_icon_path(plugin):
    plugin.config.get_icon_path.return_value = '/path/to/mock/32/tomate.png'

    assert plugin.icon_path == '/path/to/mock/32/tomate.png'


@patch('gi.repository.Notify.Notification.new')
def test_should_show_pomodoro_start_session_message(notification, plugin):
    plugin.on_session_started()

    title = plugin.messages['pomodoro']['title']
    message = plugin.messages['pomodoro']['content']

    notification.assert_called_once_with(title, message, plugin.icon_path)


@patch('gi.repository.Notify.Notification.new')
def test_should_show_session_finished_message(notification, plugin):
    plugin.on_session_finished(task=Sessions.shortbreak)

    notification.assert_called_once_with("The time is up!", '', plugin.icon_path)


def test_should_call_on_session_finished_when_session_finished(plugin):
    plugin.activate()

    result = Events.Session.send(State.finished)

    assert len(result) == 1
    assert plugin.on_session_finished == method_called(result)


def test_should_call_on_session_started_when_session_started(plugin):
    plugin.activate()

    result = Events.Session.send(State.started)

    assert len(result) == 1
    assert plugin.on_session_started == method_called(result)
