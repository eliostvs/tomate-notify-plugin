from __future__ import unicode_literals

import logging
from locale import gettext as _

from gi.repository import Notify

from tomate.enums import Task
from tomate.graph import graph
from tomate.plugin import Plugin
from tomate.utils import suppress_errors

logger = logging.getLogger(__name__)


class NotifyPlugin(Plugin):

    subscriptions = (
        ('session_started', 'on_session_started'),
        ('session_ended', 'on_session_ended'),
    )

    messages = {
        'pomodoro': {
            'title': _('Pomodoro'),
            'content': _("It's time to work!"),
        },

        'shortbreak': {
            'title': _('Short Break'),
            'content': _("Go take a coffee!"),
        },

        'longbreak': {
            'title': _('Long Break'),
            'content': _("Got take a walk!"),
        },
    }

    @suppress_errors
    def __init__(self):
        super(NotifyPlugin, self).__init__()
        self.config = graph.get('tomate.config')

    @suppress_errors
    def activate(self):
        super(NotifyPlugin, self).activate()
        Notify.init('Tomate')

    @suppress_errors
    def deactivate(self):
        super(NotifyPlugin, self).deactivate()
        Notify.uninit()

    @suppress_errors
    def on_session_started(self, *args, **kwargs):
        self.show_notification(*self.get_message(**kwargs))

    @suppress_errors
    def on_session_ended(self, *args, **kwargs):
        self.show_notification("The time is up!")

    def get_message(self, **kwargs):
        task = kwargs.get('task', Task.pomodoro)

        return (self.messages[task.name]['title'],
                self.messages[task.name]['content'])

    def show_notification(self, title, message=''):
        notify = Notify.Notification.new(title, message, self.iconpath)
        notify.show()

        logger.debug('Message %s sent!', message)

    @property
    def iconpath(self):
        return self.config.get_icon_path('tomate', 32)
