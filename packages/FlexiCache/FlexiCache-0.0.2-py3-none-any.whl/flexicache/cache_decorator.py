import functools
from hashlib import md5


class Cache:
    def __init__(self, cache_strategy):
        self.cache_strategy = cache_strategy

    def __call__(self, func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            cache_key = self.get_cache_key(func, *args, **kwargs)
            cache_result = self.cache_strategy.get(cache_key)

            if cache_result is not None:
                return cache_result

            result = func(*args, **kwargs)
            self.cache_strategy.set(cache_key, result, func, *args, **kwargs)
            return result

        return wrapped_func

    def get_cache_key(self, func, *args, **kwargs):
        key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
        return md5(key.encode('utf-8')).hexdigest()
    
    