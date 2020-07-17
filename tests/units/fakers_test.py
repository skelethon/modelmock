#!/usr/bin/env python3

import unittest
import os, sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../src')

from modelmock.fakers import generate_agents


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

