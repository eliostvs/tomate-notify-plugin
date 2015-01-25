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
        ('session_started', 'on_pomodoro_started_signal'),
        ('session_ended', 'on_pomodoro_finished_signal'),
    )

    messages = {
        'finished': (_('Take a break!'), _('The time is up!')),
        'pomodoro': (_('Pomodoro'), _("It's time to work. Focus now!")),
        'shortbreak': (_('Short break'), _('Go take a coffee!')),
        'longbreak': (_('Long break'), _('Time to rest. Go take a walk!'))}

    def on_init(self):
        self.profile = ProfileManagerSingleton.get()
        self.iconpath = self.profile.get_icon_path('tomate', 32)

    def on_activate(self):
        Notify.init('Tomate')

    def on_deactivate(self):
        Notify.uninit()

    def on_pomodoro_started_signal(self, sender=None, **kwargs):
        task = kwargs.get('task', Task.pomodoro)
        self.show_notification(*self.messages[task.name])

    @suppress_errors
    def on_pomodoro_finished_signal(self, sender=None, **kwargs):
        self.show_notification(*self.messages['finished'])

    @suppress_errors
    def show_notification(self, title, message):
        notify = Notify.Notification.new(title, message, self.iconpath)
        notify.show()

        logger.debug('Notify %s was sent', message)
