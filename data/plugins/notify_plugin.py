from __future__ import unicode_literals

import logging
from locale import gettext as _

import gi

gi.require_version('Notify', '0.7')

from gi.repository import Notify

import tomate.plugin
from tomate.constant import Task, State
from tomate.event import Events, on
from tomate.graph import graph
from tomate.utils import suppress_errors

logger = logging.getLogger(__name__)


class NotifyPlugin(tomate.plugin.Plugin):
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
            'content': _("Go take a walk!"),
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
    @on(Events.Session, [State.started])
    def on_session_started(self, *args, **kwargs):
        self.show_notification(*self.get_message(**kwargs))

    @suppress_errors
    @on(Events.Session, [State.finished])
    def on_session_finished(self, *args, **kwargs):
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
