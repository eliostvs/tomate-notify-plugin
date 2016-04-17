from __future__ import unicode_literals

import pytest
from mock import Mock, patch

from tomate.constant import Task
from tomate.graph import graph


@pytest.fixture()
def plugin():
    graph.register_factory('tomate.config', Mock)

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

    assert plugin.iconpath == '/path/to/mock/32/tomate.png'


@patch('gi.repository.Notify.Notification.new')
def test_should_show_pomodoro_start_session_message(notification, plugin):
    plugin.on_session_started()

    title = plugin.messages['pomodoro']['title']
    message = plugin.messages['pomodoro']['content']

    notification.assert_called_once_with(title, message, plugin.iconpath)


@patch('gi.repository.Notify.Notification.new')
def test_should_show_end_session_message(notification, plugin):
    plugin.on_session_ended(task=Task.shortbreak)

    notification.assert_called_once_with("The time is up!", '', plugin.iconpath)
