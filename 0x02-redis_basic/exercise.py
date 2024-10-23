#!/usr/bin/env python3
"""
Redis basic.
"""
from typing import Union, Callable, Optional
import redis
import uuid


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
