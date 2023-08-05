import json
from ..cache_strategy import CacheStrategy, time


class FileCache(CacheStrategy):
    def __init__(self, cache_file, cache_seconds=None):
        super().__init__(cache_seconds)
        self.cache_file = cache_file

    def get(self, key):
        try:
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
            return self.get_value_if_not_expired(cache, key)
        except FileNotFoundError:
            pass
        return None

    def set(self, key, value, func, *args, **kwargs):
        try:
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
        except FileNotFoundError:
            cache = {}

        cache[key] = {
            'function': func.__name__,
            'args': str(args),
            'kwargs': str(kwargs),
            'timestamp': time.time(),
            'value': value
        }

        with open(self.cache_file, 'w') as f:
            json.dump(cache, f, indent=4)
            