#!/usr/bin/env python3
"""Writing strings to Redis
"""


import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] =
            None) -> Union[str, bytes, int, float, None]:
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=lambda x: int(x))


def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_list_key = method.__qualname__ + ":inputs"
        output_list_key = method.__qualname__ + ":outputs"

        input_data = str(args)
        self._redis.rpush(input_list_key, input_data)

        output = method(self, *args, **kwargs)

        self._redis.rpush(output_list_key, str(output))

        return output
    return wrapper


Cache.store = call_history(Cache.store)
