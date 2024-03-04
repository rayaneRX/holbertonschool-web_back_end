#!/usr/bin/env python3
"""test_utils.py
"""


import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({}, ("a",), "Key 'a' not found in nested_map"),
        ({"a": 1}, ("a", "b"), "Key 'b' not found in nested_map['a']")
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_error_message):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_error_message)

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

if __name__ == "__main__":
    unittest.main()
