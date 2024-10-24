#!/usr/bin/env python3
"""
Redis basic.
"""
from typing import Union, Callable, Optional
import redis
import uuid
from functools import wraps


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and outputs for a particular function"""
    method_key = method.__qualname__
    inputs, outputs = method_key + ':inputs', method_key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper method"""
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result
    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    decorator for counting calls
    """
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for counting calls"""
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)
    return wrapper


def replay(method: Callable):
    """
    Displays the history of calls of a particular function
    """
    method_key = method.__qualname__
    inputs, outputs = method_key + ':inputs', method_key + ':outputs'
    redis = method.__self__._redis
    method_count = redis.get(method_key).decode('utf-8')
    print(f'{method_key} was called {method_count} times:')
    IOTuple = zip(redis.lrange(inputs, 0, -1), redis.lrange(outputs, 0, -1))
    for inp, out in list(IOTuple):
        attr, data = inp.decode("utf-8"), out.decode("utf-8")
        print(f'{method_key}(*{attr}) -> {data}')


class Cache:
    """
    chache class
    """
    def __init__(self) -> None:
        """
        INIT FUNCTION
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> str:
        """
        GET FUNCTION
        """
        return self._redis.get(key) if fn is None else fn(self._redis.get(key))

    def get_str(self, data: str) -> str:
        return (data).decode('utf-8')

    def get_int(self, data: str) -> int:
        return int(data)
