#!/usr/bin/env python3

import unittest
import os, sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')

from modelmock.faker import flatten_contract

class flatten_contract_test(unittest.TestCase):

  def setUp(self):
    pass

  def test_flatten_contract_ok(self):
    _contract = dict(
      period=15,
      extras=[
        dict(name='Peter', gender=True, age=21),
        dict(name='Daisy', gender=False, age=20),
      ]
    )
    _flatten = flatten_contract(_contract)
    self.assertEqual(_flatten, {
      'period': 15,
      'extra_0_name': 'Peter',
      'extra_0_gender': True,
      'extra_0_age': 21,
      'extra_1_name': 'Daisy',
      'extra_1_gender': False,
      'extra_1_age': 20
    })

  def test_flatten_contract_extras_is_empty(self):
    _contract = dict(period=15, extras=[])
    self.assertEqual(flatten_contract(_contract), {'period': 15})

  def test_flatten_contract_extras_not_found(self):
    _contract = dict(period=15)
    self.assertEqual(flatten_contract(_contract), {'period': 15})

  def test_flatten_contract_extras_is_undefined(self):
    self.assertIsNone(flatten_contract(None), None)
