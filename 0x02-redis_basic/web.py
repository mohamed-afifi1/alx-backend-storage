#!/usr/bin/env python3
"""
create a web cach
"""
import redis
import requests
cache = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """ get a page and cach value"""
    cache.set(f"cached:{url}", count)
    resp = requests.get(url)
    cache.incr(f"count:{url}")
    cache.setex(f"cached:{url}", 10000, cache.get(f"cached:{url}"))
    return resp.text
