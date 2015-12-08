from __future__ import unicode_literals

import unittest

from mock import Mock, patch

from tomate.constant import Task
from tomate.graph import graph


class TestNotifyPlugin(unittest.TestCase):

    def setUp(self):
        graph.register_factory('tomate.config', Mock)
        from notify_plugin import NotifyPlugin

        self.plugin = NotifyPlugin()

    def create_instance(self):
        return self.plugin

    @patch('gi.repository.Notify.init')
    def test_init_dbus(self, mock_init):
        self.plugin.activate()

        mock_init.assert_called_with('Tomate')

    @patch('gi.repository.Notify.uninit')
    def test_uninit_dbus(self, mock_uninit):
        self.plugin.deactivate()

        mock_uninit.assert_called_with()

    def test_get_icon_path(self):
        self.plugin.config.get_icon_path.return_value = '/path/to/mock/32/tomate.png'

        self.assertEqual('/path/to/mock/32/tomate.png', self.plugin.iconpath)

    @patch('gi.repository.Notify.Notification.new')
    def test_should_show_pomodoro_start_session_message(self, mock_notification):
        self.plugin.on_session_started()

        title = self.plugin.messages['pomodoro']['title']
        message = self.plugin.messages['pomodoro']['content']

        mock_notification.assert_called_once_with(title, message, self.plugin.iconpath)

    @patch('gi.repository.Notify.Notification.new')
    def test_should_show_end_session_message(self, mock_notification):
        self.plugin.on_session_ended(task=Task.shortbreak)

        mock_notification.assert_called_once_with("The time is up!", '', self.plugin.iconpath)
