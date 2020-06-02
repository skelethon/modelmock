#!/usr/bin/env python3

import unittest
import os, sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')

from modelmock.utils import array_random_split

class array_random_split_test(unittest.TestCase):

  def setUp(self):
    pass

  def test_array_random_split_ok(self):
    _arr = range(20)
    _chunks = array_random_split(_arr, 5)
    self.assertEqual(len(_chunks), 5)
