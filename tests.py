from __future__ import unicode_literals

import unittest

from mock import patch


class NotifyPluginConstructorTestCase(unittest.TestCase):

    @patch('tomate.profile.ProfileManager')
    def setUp(self, mock_profile):
        from notify_plugin import NotifyPlugin

        self.plugin = NotifyPlugin()
        self.mock_profile = mock_profile

    @patch('gi.repository.Notify.init')
    def test_should_init_dbus(self, mock_init):
        self.plugin.activate()

        mock_init.assert_called_with('Tomate')

    @patch('gi.repository.Notify.uninit')
    def test_should_uninit_dbus(self, mock_uninit):
        self.plugin.deactivate()

        mock_uninit.assert_called_with()

    def test_should_get_icon_path(self):
        self.mock_profile.return_value.get_icon_path.return_value = '/path/to/mock/22/tomate.png'

        self.assertEqual('/path/to/mock/22/tomate.png', self.plugin.icon)
        self.mock_profile.return_value.get_icon_path.assert_called_once_with('tomate', 32)


@patch('gi.repository.Notify.Notification.new')
class NotifyPluginTestCase(unittest.TestCase):

    @patch('tomate.profile.ProfileManager')
    def setUp(self, *args):
        from notify_plugin import NotifyPlugin

        self.plugin = NotifyPlugin()

    def test_should_show_pomodoro_start_session_message(self, mNotification):
        self.plugin.on_session_started()

        title = self.plugin.messages['pomodoro']['title']
        message = self.plugin.messages['pomodoro']['content']

        mNotification.assert_called_once_with(title, message, self.plugin.icon)

    def test_should_show_end_session_message(self, mNotification):
        from tomate.pomodoro import Task
        self.plugin.on_session_ended(task=Task.shortbreak)

        mNotification.assert_called_once_with("The time is up!", '', self.plugin.icon)
