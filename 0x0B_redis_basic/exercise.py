#!/usr/bin/env python3
"""Writing strings to Redis
"""


import redis
import uuid
from typing import Union, Callable
from functools import wraps


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable =
            None) -> Union[str, bytes, int, float]:
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        return self.get(key, fn=lambda x: int(x))

    @staticmethod
    def count_calls(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    @staticmethod
    def call_history(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key_inputs = f"{method.__qualname__}:inputs"
            key_outputs = f"{method.__qualname__}:outputs"
            self._redis.rpush(key_inputs, str(args))
            result = method(self, *args, **kwargs)
            self._redis.rpush(key_outputs, str(result))
            return result
        return wrapper

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


def replay(func):
    inputs = cache._redis.lrange(f"{func.__qualname__}:inputs", 0, -1)
    outputs = cache._redis.lrange(f"{func.__qualname__}:outputs", 0, -1)
    print(f"{func.__qualname__} was called {len(inputs)} times:")
    for inp, out in zip(inputs, outputs):
        print(f"{func.__qualname__}(*{inp.decode
                                      ('utf-8')}) -> {out.decode('utf-8')}")
