#!/usr/bin/env python3
import random
import unittest
import os, sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../src')

from modelmock.fakers import generate_agents, generate_contracts


class generate_agents_test(unittest.TestCase):

  def setUp(self):
    pass

  def test_default_subpath_ok(self):
    _agents = list(generate_agents(6, [
        {'level': 'A', 'count': 1},
        {'level': 'B', 'count': 2},
        {'level': 'C'}
    ]))
    self.assertEqual(len(_agents), 6)

    _counts = dict(A=0,B=0,C=0)
    for _agent in _agents:
      _counts[_agent['record']['level']] = _counts[_agent['record']['level']] + 1

    self.assertEqual(_counts, dict(A=1,B=2,C=3))


  def test_without_subpath_ok(self):
    _agents = list(generate_agents(6, [
        {'level': 'A', 'count': 2},
        {'level': 'B', 'count': 4},
        {'level': 'C'}
    ], subpath=None))
    self.assertEqual(len(_agents), 6)

    _counts = dict(A=0,B=0,C=0)
    for _agent in _agents:
      _counts[_agent['level']] = _counts[_agent['level']] + 1

    self.assertEqual(_counts, dict(A=2,B=4,C=0))

class generate_contracts_test(unittest.TestCase):

  def setUp(self):
    pass

  def test_defaul_ok(self):
    _records = generate_contracts(6, 100, 1000)
    self.assertEqual(len(list(_records)), 6)

  def test_value_of_contract_price_less_than_2(self):
    with self.assertRaises(ValueError) as context:
      for i in range(5):
        _price = random.randint(0,1)
        generate_contracts(8, _price, 1000)
        self.assertEqual('variance must be greater than 0',context.exception)

  def test_sum_fyps_equal_multiple_totalagents_and_contract_price(self):
    _records = generate_contracts(10, 100, 1000)
    _total = sum([record['fyp'] for record in list(_records)])
    self.assertEqual(_total, 10*100*1000)

  def test_value_type(self):
    _records = generate_contracts(6, 9, 10000)
    _check = True

    for record in _records:
      _fields = list(record)
      _fields_type = []

      for i in _fields:
        if 'type' in i:
          _fields_type.append(i)

      for field in _fields_type:
        _check = False if record[field] > 3 else True

    self.assertEqual(True,_check)
