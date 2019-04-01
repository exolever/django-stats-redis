from ..connections import stats


class StatsMixin:
    _stats = []
    _default_stats = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats = {}
        self.do_stats()

    def do_stats(self):
        stats_list = getattr(self, '_default_stats', [])
        stats_list.extend(getattr(self, '_stats', []))
        for key, attribute, historical in stats_list:
            if not self.pk:
                continue
            self.stats[key] = stats.create_stat(
                obj=self,
                key=key,
                historical=historical,
                obj_attr=attribute)

    def increment_stat(self, stat):
        self.stats[stat].incr(1)

    def decrement_stat(self, stat):
        self.stats[stat].decr(1)
