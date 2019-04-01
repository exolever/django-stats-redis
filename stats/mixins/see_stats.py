from actstream import action

from django.contrib.contenttypes.models import ContentType

from ..conf import settings
from .stats import StatsMixin


class ActionStatsMixin(StatsMixin):
    _stats_notification = []
    _default_stats = [
        ('views', 'count_views', False),
    ]

    def _notify(self, action_verb, *args, **kwargs):
        stats_notification = getattr(self, '_stats_notification', ())
        for key, notification_signal_hook in stats_notification:
            if key == action_verb and notification_signal_hook:
                notification_signal_hook.send(**kwargs)

    def can_see(self, user_from, raise_exceptions=True):
        return True

    @property
    def count_views(self):
        return self.action_object_actions.filter(
            verb=settings.STATS_ACTION_GENERIC_SEE).count()

    def see(self, user_from, timestamp=None, notify=True, raise_exceptions=False):
        self.can_see(user_from=user_from, raise_exceptions=raise_exceptions)
        action_verb = settings.STATS_ACTION_GENERIC_SEE
        data = {
            'verb': action_verb,
            'action_object': self,
        }
        if timestamp:
            data['timestamp'] = timestamp

        action.send(user_from, **data)
        self.increment_stat('views')

        if notify:
            self._notify(
                action_verb,
                sender=self.__class__,
                instance=self,
                action=action_verb,
            )

    def has_seen(self, user):
        ct = ContentType.objects.get_for_model(user)
        return self.action_object_actions.filter(
            actor_content_type=ct,
            actor_object_id=user.id,
            verb=settings.STATS_ACTION_GENERIC_SEE).exists()
