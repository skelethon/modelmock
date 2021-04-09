#!/usr/bin/env python3

import unittest
import os, sys
import itertools
import random

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../src')

from modelmock.utils import array_random_split, flatten_sub_list, set_deep_child, transform_dict_item_names, propagate_patterns, random_fixed_sum_array


class array_random_split_test(unittest.TestCase):

  def setUp(self):
    pass

  def test_array_random_split_ok(self):
    _arr = range(20)
    _chunks = array_random_split(_arr, 5)
    self.assertEqual(len(_chunks), 5)

  def test_array_random_split_with_number_of_subarrays_greater_than_array_size(self):
    _arr = [1, 2, 3]
    _chunks = array_random_split(_arr, 5, empty_accepted=True)
    self.assertEqual(len(_chunks), 5)
    self.assertEqual(list(itertools.chain.from_iterable(_chunks)), _arr)

  def test_array_random_split_empty_array_to_5_subarrays(self):
    _arr = []
    _chunks = array_random_split(_arr, 3, empty_accepted=True)
    self.assertEqual(len(_chunks), 3)
    self.assertEqual(list(itertools.chain.from_iterable(_chunks)), _arr)

  def test_array_random_split_with_number_of_subarrays_equals_to_array_size(self):
    _arr = [1, 2, 3, 4, 5]
    for _ in range(3):
      _chunks = array_random_split(_arr, 5, empty_accepted=False)
      self.assertEqual(len(_chunks), 5)
      self.assertEqual(_chunks, [[1], [2], [3], [4], [5]])

  def test_array_random_split_with_number_of_subarrays_less_than_array_size(self):
    _arr = [1, 2, 3, 4]
    with self.assertRaises(ValueError):
      array_random_split(_arr, 5, empty_accepted=False)


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

  def test_set_deep_child_with_root(self):
    self.assertEqual(set_deep_child(None, root={ 'id': 17779 }), None)
    self.assertEqual(set_deep_child(None, root={ 'id': 17779 }, path=['none']), {'none': None, 'id': 17779})
    self.assertEqual(set_deep_child('Hello world', root={ 'id': 17779 }), 'Hello world')
    self.assertEqual(set_deep_child('Hello world', root={ 'id': 17779 }, path=[]), 'Hello world')
    self.assertEqual(set_deep_child('Hello world', root={ 'id': 17779 }, path=['msg']), {'msg': 'Hello world', 'id': 17779})
    self.assertEqual(set_deep_child('Hello world', root={ 'id': 17779 }, path=['msg', 0]), {'msg': {'0': 'Hello world'}, 'id': 17779})
    self.assertEqual(set_deep_child('Hello world', root={ 'id': 17779 }, path=['I', 'say']), {'I': {'say': 'Hello world'}, 'id': 17779})


class transform_dict_item_names_test(unittest.TestCase):

  def setUp(self):
    pass

  def test_transform_dict_item_names_ok(self):
    record = dict(p1=1024, p2='Hello world', p3=True, p4=None, p5=[1, 2, 3])
    self.assertEqual(transform_dict_item_names(record, mappings={ 'p1': 'int', 'p2': 'str' }), {
      'int': 1024,
      'str': 'Hello world',
      'p3': True,
      'p4': None,
      'p5': [1, 2, 3],
    })

  def test_transform_dict_item_names_with_not_dicttype_record(self):
    self.assertEqual(transform_dict_item_names(None, {'p1': 'int'}), None)
    self.assertEqual(transform_dict_item_names(1234, {'p1': 'int'}), 1234)
    self.assertEqual(transform_dict_item_names([1, 2], {'p1': 'int'}), [1, 2])

  def test_transform_dict_item_names_with_not_dicttype_mappings(self):
    self.assertEqual(transform_dict_item_names(dict(p1=1234), None), {'p1': 1234})
    self.assertEqual(transform_dict_item_names(dict(p1=1234), 1234), {'p1': 1234})


class propagate_patterns_test(unittest.TestCase):

  def setUp(self):
    pass

  def test_propagate_patterns_ok(self):
    self.assertEqual(propagate_patterns(10, [], shuffle=False), [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
    self.assertEqual(propagate_patterns(10, [2, 3], shuffle=False), [0, 0, 1, 1, 1, -1, -1, -1, -1, -1])
    self.assertEqual(propagate_patterns(10, [2, 9], shuffle=False), [0, 0, 1, 1, 1, 1, 1, 1, 1, 1])


class random_fixed_sum_array__test(unittest.TestCase):

  def setUp(self):
    pass

  # when mean<2, the process will not finish
  def test_mean_is_zero(self):
    for _ in range(10):
      n = random.randint(1, 50)
      s = int(n*random.random()*2)
      # s = random.randint(1, 50)
      # n = s//2 + random.randint(1, 50)
      self.assertRaises(ValueError, random_fixed_sum_array, s, n)

  """
  s>0 & n>0: must satisfy 2 conditions
    - n = len(arr)
    - s = sum(arr)
  """
  def test_sum_and_n_greater_than_zero(self):
    for _ in range(10):
      n = random.randint(1, 50)
      s = n*2 + random.randint(0, 50)
      arr = random_fixed_sum_array(s, n)

      self.assertEqual(sum(arr), s)
      self.assertEqual(len(arr), n)
