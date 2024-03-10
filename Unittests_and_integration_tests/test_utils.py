#!/usr/bin/env python3
""" Unittests for utils module """

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):

    """Class testing access_nested_map fn"""
    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected):
        """ Test access_nested_map fn """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand(
        [
            ({}, ("a",)),
            ({"a": 1}, ("a", "b"))
        ]
    )
    def test_access_nested_map_exception(self, nested_map, path):
        """ Test access_nested_map fn with exception """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """ Class testing get_json fn """
    @parameterized.expand(
        [
            ("http://exemple.com", {"payload": True}),
            ("http://holberton.io", {"payload": False})
        ])
    @patch('requests.get')
    def test_get_json(self, url, payload, mock_request):
        """ Test get_json fn """
        mock_request.return_value.json.return_value = payload
        self.assertEqual(get_json(url), payload)
        mock_request.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """Class testing memoize decorator"""
    def test_memoize(self):
        """ Test memoize decorator """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_method:
            test_obj = TestClass()
            test_obj.a_property
            test_obj.a_property
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
