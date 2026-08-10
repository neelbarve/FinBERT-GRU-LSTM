import functools

CACHE = {}

def cache_result(ttl=None):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args):
            key = (fn.__name__, args)
            if key in CACHE:
                return CACHE[key]
            result = fn(*args)
            CACHE[key] = result
            return result
        return wrapper
    return decorator
