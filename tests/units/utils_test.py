#!/usr/bin/env python3

import unittest
import os, sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../src')

from modelmock.utils import array_random_split, flatten_sub_list, set_deep_child


class array_random_split_test(unittest.TestCase):

  def setUp(self):
    pass

  def test_array_random_split_ok(self):
    _arr = range(20)
    _chunks = array_random_split(_arr, 5)
    self.assertEqual(len(_chunks), 5)


class flatten_sub_list_test(unittest.TestCase):

  def setUp(self):
    pass

  def test_flatten_sub_list_ok(self):
    _contract = dict(
      period=15,
      extras=[
        dict(name='Peter', gender=True, age=21),
        dict(name='Daisy', gender=False, age=20),
      ]
    )
    _flatten = flatten_sub_list(_contract)
    self.assertEqual(_flatten, {
      'period': 15,
      'extra_0_name': 'Peter',
      'extra_0_gender': True,
      'extra_0_age': 21,
      'extra_1_name': 'Daisy',
      'extra_1_gender': False,
      'extra_1_age': 20
    })

  def test_flatten_sub_list_extras_is_empty(self):
    _contract = dict(period=15, extras=[])
    self.assertEqual(flatten_sub_list(_contract), {'period': 15})

  def test_flatten_sub_list_extras_not_found(self):
    _contract = dict(period=15)
    self.assertEqual(flatten_sub_list(_contract), {'period': 15})

  def test_flatten_sub_list_extras_is_undefined(self):
    self.assertIsNone(flatten_sub_list(None), None)


class set_deep_child_test(unittest.TestCase):

  def setUp(self):
    pass

  def test_set_deep_child_without_root(self):
    self.assertEqual(set_deep_child(None), None)
    self.assertEqual(set_deep_child(None, path=['none']), {'none': None})
    self.assertEqual(set_deep_child('Hello world'), 'Hello world')
    self.assertEqual(set_deep_child('Hello world', path=[]), 'Hello world')
    self.assertEqual(set_deep_child('Hello world', path=['msg']), {'msg': 'Hello world'})
    self.assertEqual(set_deep_child('Hello world', path=['msg', 0]), {'msg': {'0': 'Hello world'}})
    self.assertEqual(set_deep_child('Hello world', path=['I', 'say']), {'I': {'say': 'Hello world'}})
