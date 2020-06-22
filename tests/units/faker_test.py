#!/usr/bin/env python3

import unittest
import os, sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')

from modelmock.faker import generate_agents


class generate_agents_test(unittest.TestCase):

  def setUp(self):
    pass

  def test_ok(self):
    _agents = list(generate_agents(6, [
        {'level': 'A', 'count': 1},
        {'level': 'B', 'count': 2},
        {'level': 'C'}
    ]))
    self.assertEqual(len(_agents), 6)
