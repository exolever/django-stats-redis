from django.apps import AppConfig
from django.conf import settings


class StatsConfig(AppConfig):
    name = 'stats'

    def ready(self):
        try:
            assert hasattr(settings, 'REDIS_HOST')
            assert hasattr(settings, 'REDIS_PORT')
            assert hasattr(settings, 'REDIS_AUTH_DB')
        except AssertionError:
            msg = 'Please provide REDIS_HOST, REDIS_PORT and REDIS_AUTH_DB vars in settings'
            raise Exception(msg)
