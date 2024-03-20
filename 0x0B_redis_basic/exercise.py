#!/usr/bin/env python3
"""Writing strings to Redis
"""


import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


class Cache:
    """A class for storing and retrieving data in Redis."""

    def __init__(self):
        """Initialize a connection to Redis."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis.

        Args:
            data (Union[str, bytes, int, float]): Data to be stored.

        Returns:
            str: The generated key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] =
            None) -> Union[str, bytes, int, float, None]:
        """Retrieve data from Redis.

        Args:
            key (str): The key under which the data is stored in Redis.
            fn (Optional[Callable]): A function to apply to the retrieved data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve string data from Redis.

        Args:
            key (str): The key under which the string data is stored in Redis.

        Returns:
            Union[str, None]: The retrieved string data.
        """
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve integer data from Redis.

        Args:
            key (str): The key under which the integer data is stored in Redis.

        Returns:
            Union[int, None]: The retrieved integer data.
        """
        return self.get(key, fn=lambda x: int(x))


def call_history(method: Callable) -> Callable:
    """Decorator to track history of method calls."""
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


def replay(method: Callable):
    """Replay history of method calls."""
    method_name = method.__qualname__
    input_list_key = method_name + ":inputs"
    output_list_key = method_name + ":outputs"

    # Retrieve input and output lists from Redis
    input_list = cache._redis.lrange(input_list_key, 0, -1)
    output_list = cache._redis.lrange(output_list_key, 0, -1)

    print(f"{method_name} was called {len(input_list)} times:")
    for inputs, output in zip(input_list, output_list):
        print(f"{method_name}(*{inputs.decode
                                ('utf-8')}) -> {output.decode('utf-8')}")


Cache.store = call_history(Cache.store)
