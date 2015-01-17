from __future__ import unicode_literals

import unittest

from mock import patch


class NotifyPluginConstructorTestCase(unittest.TestCase):

    @patch('notify_plugin.ProfileManagerSingleton.get')
    def setUp(self, mProfileManagerSingleton):
        from notify_plugin import NotifyPlugin

        self.plugin = NotifyPlugin()
        self.mProfileManagerSingleton = mProfileManagerSingleton

    @patch('gi.repository.Notify.init')
    def test_should_init_dbus(self, mock_init):
        self.plugin.activate()

        mock_init.assert_called_with('Tomate')

    @patch('gi.repository.Notify.uninit')
    def test_should_uninit_dbus(self, mock_uninit):
        self.plugin.deactivate()

        mock_uninit.assert_called_with()

    def test_should_get_icon_path(self):
        self.mProfileManagerSingleton.return_value.get_icon_path.assert_called_once_with('tomate', 32)


@patch('gi.repository.Notify.Notification.new')
class NotifyPluginTestCase(unittest.TestCase):

    @patch('notify_plugin.ProfileManagerSingleton.get')
    def setUp(self, mProfileManagerSingleton):
        from notify_plugin import NotifyPlugin

        self.plugin = NotifyPlugin()

    def test_should_show_pomodoro_notification(self, mNotification):
        self.plugin.on_pomodoro_started_signal()

        title, message = self.plugin.messages['pomodoro']

        mNotification.assert_called_once_with(title, message, self.plugin.iconpath)

    def test_should_show_session_end_notification(self, mNotification):
        self.plugin.on_pomodoro_finished_signal()

        title, message = self.plugin.messages['finished']

        mNotification.assert_called_once_with(title, message, self.plugin.iconpath)

    def test_should_show_short_break_notification(self, mNotification):
        from tomate.pomodoro import Task

        self.plugin.on_pomodoro_started_signal(task=Task.shortbreak)

        title, message = self.plugin.messages['shortbreak']

        mNotification.assert_called_once_with(title, message, self.plugin.iconpath)
