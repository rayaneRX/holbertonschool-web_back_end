#!/usr/bin/env python3
"""helper function"""


def index_range(page: int, page_size: int):
    """ Return a tuple of size 2"""
    start = (page - 1) * page_size
    end = page * page_size
    return (start, end)
