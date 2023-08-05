from ..cache_strategy import CacheStrategy, time


class MemoryCache(CacheStrategy):
    def __init__(self, cache_seconds=None):
        super().__init__(cache_seconds)
        self.memory_cache = {}

    def get(self, key):
        return self.get_value_if_not_expired(self.memory_cache, key)

    def set(self, key, value, func, *args, **kwargs):
        self.memory_cache[key] = {
            'function': func.__name__,
            'args': str(args),
            'kwargs': str(kwargs),
            'timestamp': time.time(),
            'value': value
        }
        