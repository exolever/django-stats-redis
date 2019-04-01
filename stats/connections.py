import redis

from django.conf import settings

from .objects import Stat


class RedisConnection(object):
    def __init__(self, **kwargs):
        self.connection = self.create_connection()

    def create_connection(self):
        return redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_AUTH_DB,
            charset='utf-8',
            decode_responses=True
        )


class Stats(RedisConnection):
    _stats = {}

    def __getitem__(self, key):
        if key in self._stats:
            return self._stats[key]

        raise Exception('Stat {key} does not exist'.format(key=key))

    def __getattr__(self, name):
        if name in self._stats:
            return self._stats[name]

    def create_stat(self, name=None, obj=None, obj_attr=None,
                    pk=None, key=None,
                    historical=False):
        stat = Stat(self.connection,
                    obj=obj, obj_attr=obj_attr,
                    pk=pk, key=key, name=name,
                    historical=historical)
        self._stats[stat.redis_key] = stat
        return stat


stats = Stats()
