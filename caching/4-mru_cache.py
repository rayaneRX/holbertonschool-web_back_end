#!/usr/bin/python3
""" MRUCach Caching """
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCach class that inherits from BaseCaching """

    def __init__(self):
        """ Initialize """
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """ Add item in the cache """
        if key and item:
            if len(self.cache_data) >= self.MAX_ITEMS:
                if self.queue:
                    discard = self.queue.pop()
                    del self.cache_data[discard]
                    print("DISCARD: {}".format(discard))
            self.cache_data[key] = item
            self.queue.append(key)

    def get(self, key):
        """ Get item by key """
        if key in self.cache_data:
            self.queue.remove(key)
            self.queue.append(key)
        return self.cache_data.get(key)
