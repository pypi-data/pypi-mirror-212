from abc import ABC, abstractmethod
import time


class CacheStrategy(ABC):
    def __init__(self, cache_seconds=None):
        self.cache_seconds = cache_seconds

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value):
        pass

    def is_expired(self, timestamp):
        return self.cache_seconds is not None and time.time() > timestamp + self.cache_seconds

    def get_value_if_not_expired(self, cache, key):
        if key in cache:
            cache_item = cache[key]
            timestamp = cache_item['timestamp']
            if not self.is_expired(timestamp):
                return cache_item['value']
        return None
    