#!/usr/bin/env python3
'''
    function sum_list which takes a list input_list of floats
    as argument and returns their sum as a float.
'''


from typing import Union, Tuple

def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    '''
        function sum_list
    '''
    return k, v*v
