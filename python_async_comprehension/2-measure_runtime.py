#!/usr/bin/env python3
""" measure_runtime should measure the total runtime and return it."""

import asyncio

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    measure_runtime should measure the total runtime and return it.
    """
    start = asyncio.get_event_loop().time()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    end = asyncio.get_event_loop().time()
    return end - start
