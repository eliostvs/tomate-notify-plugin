from __future__ import unicode_literals

import logging
from locale import gettext as _

from gi.repository import Notify
from tomate.plugin import TomatePlugin
from tomate.pomodoro import Task
from tomate.profile import ProfileManagerSingleton
from tomate.utils import suppress_errors

logger = logging.getLogger(__name__)


class NotifyPlugin(TomatePlugin):

    signals = (
        ('session_started', 'on_session_started'),
        ('session_ended', 'on_session_ended'),
    )

    messages = {
        'pomodoro': {
            'name': _('Pomodoro'),
            'start': _("It's time to work!"),
        },

        'shortbreak': {
            'name': _('Short Break'),
            'start': _("Go take a coffee!"),
        },

        'longbreak': {
            'name': _('Long Break'),
            'start': _("Got take a walk!"),
        },
    }

    def on_init(self):
        self.profile = ProfileManagerSingleton.get()
        self.iconpath = self.profile.get_icon_path('tomate', 32)

    def on_activate(self):
        Notify.init('Tomate')

    def on_deactivate(self):
        Notify.uninit()

    def on_session_started(self, sender=None, **kwargs):
        task = kwargs.get('task', Task.pomodoro)

        title = self.messages[task.name]['name']
        message = self.messages[task.name]['start']

        self.show_notification(title, message)

    @suppress_errors
    def on_session_ended(self, sender=None, **kwargs):
        self.show_notification("The time is up!")

    @suppress_errors
    def show_notification(self, title, message=''):
        notify = Notify.Notification.new(title, message, self.iconpath)
        notify.show()

        logger.debug('Message %s sent!', message)
