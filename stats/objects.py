from django.utils import timezone

from redis.exceptions import DataError, ResponseError


class Stat(object):
    object = None
    name = None
    pk = None
    key = None
    historical = False
    object_attribute = None

    redis_key = None
    historical_redis_keys = {
        'total': 'total',
        'history': 'history',
    }
    _date_format = '%Y-%m-%d'

    def __init__(self, connection,
                 obj=None, obj_attr=None,
                 pk=None, key=None, name=None,
                 historical=False):
        self.connection = connection
        self.historical = historical
        self.object = obj
        self.object_attribute = obj_attr
        if self.object:
            self.name = self.object._meta.model_name
            self.pk = getattr(self.object, 'pk', pk)
        else:
            self.name = name
            self.pk = pk
        self.key = key
        self._set_redis_key()

    def _set_redis_key(self):
        if not self.redis_key:
            self.redis_key = self.name

            if self.pk:
                self.redis_key += ':{pk}'.format(pk=self.pk)

            if self.key:
                self.redis_key += ':{key}'.format(key=self.key)

        return self.redis_key

    def get_key(self, history='total'):
        key = self.redis_key
        if self.historical and history:
            key = u'{}:{}'.format(self.redis_key,
                                  self.historical_redis_keys[history])
        return key

    def get(self, history='total', date=None):
        key = self.get_key(history)
        if not self.historical or history == 'total':
            result = self.connection.get(key)
            if result is None:
                value = self.reset()
                if value is not None:
                    return self.get(history, date)
        elif self.historical:
            if not date:
                date = timezone.now().strftime(self._date_format)
            result = self.connection.hget(key, date)
        return result

    def getall(self, history='total'):
        key = self.get_key(history)
        if self.connection.exists(key):
            return self.connection.hgetall(key)
        else:
            self.reset()
            return self.getall(history)

    def hget(self, name, history='total'):
        key = self.get_key(history)
        if self.connection.exists(key):
            return self.connection.hget(key, name)
        else:
            value = self.reset()
            # when value is {} redis can't allow store this value so we have to manage it
            if not value:
                return value.get(name)
            return self.hget(name, history)

    def hset(self, name, value, history='total'):
        key = self.get_key(history)
        self.connection.hset(key, name, value)

    def sadd(self, value, history='total'):
        key = self.get_key(history)
        self.connection.sadd(key, value)

    def srem(self, value, history='total'):
        key = self.get_key(history)
        self.connection.srem(key, value)

    def smembers(self, history='total'):
        key = self.get_key(history)
        if self.connection.exists(key):
            return self.connection.smembers(key)
        else:
            value = self.reset()
            if not value:
                return value
            return self.smembers(history)

    def sismember(self, value, history='total'):
        key = self.get_key(history)
        return self.connection.sismember(key, value)

    def incr(self, amount=1):
        if self.historical:
            # Total
            self.connection.incrby(self.get_key('total'), amount=amount)
            # History
            self.connection.hincrby(
                self.get_key('history'),
                timezone.now().strftime(self._date_format),
                amount=amount)
        else:
            self.connection.incrby(self.get_key(), amount=amount)

    def decr(self, amount=1):
        if self.historical:
            # Total
            self.connection.decr(self.get_key('total'), amount=amount)
            # History
            self.connection.hincrby(
                self.get_key('history'),
                timezone.now().strftime(self._date_format),
                amount=-amount)
        else:
            self.connection.decr(self.get_key(), amount=amount)

    def set(self, value, history='total'):
        key = self.get_key(history)
        if not self.historical or history == 'total':
            if isinstance(value, dict):
                try:
                    self.connection.hmset(key, value)
                except DataError:
                    pass
            elif isinstance(value, set):
                try:
                    self.connection.sadd(key, *value)
                except (DataError, ResponseError):
                    pass
            else:
                self.connection.set(key, value)
        elif self.historical:
            self.connection.hset(key,
                                 timezone.now().strftime(self._date_format),
                                 value)
        return value

    def get_total(self):
        return self.get(history='total')

    def get_by_date(self, date):
        return self.connection.hget(self.get_key('history'),
                                    date.strftime(self._date_format))

    def reset(self):
        if self.object_attribute:
            value = getattr(self.object, self.object_attribute, None)
        else:
            value = 0
        if value is not None:
            self.set(value)
        return value
