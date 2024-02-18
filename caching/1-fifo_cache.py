#!/usr/bin/python3
""" Module for FIFOCache
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFOCache defines a caching system using the FIFO algorithm"""

    def __init__(self):
        """Initialize"""
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is not None and item is not None:
            self.cache_data[key] = item
            if key in self.queue:
                self.queue.remove(key)
            self.queue.append(key)
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                discarded = self.queue.pop(0)
                del self.cache_data[discarded]
                print("DISCARD:", discarded)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)