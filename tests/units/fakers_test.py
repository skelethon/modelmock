#!/usr/bin/env python3
import random
import unittest
import os, sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../src')

from modelmock.fakers import generate_agents, generate_contracts, generate_purchases


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

        _counts = dict(A=0, B=0, C=0)
        for _agent in _agents:
            _counts[_agent['record']['level']] = _counts[_agent['record']['level']] + 1

        self.assertEqual(_counts, dict(A=1, B=2, C=3))

    def test_without_subpath_ok(self):
        _agents = list(generate_agents(6, [
            {'level': 'A', 'count': 2},
            {'level': 'B', 'count': 4},
            {'level': 'C'}
        ], subpath=None))
        self.assertEqual(len(_agents), 6)

        _counts = dict(A=0, B=0, C=0)
        for _agent in _agents:
            _counts[_agent['level']] = _counts[_agent['level']] + 1

        self.assertEqual(_counts, dict(A=2, B=4, C=0))


class generate_purchases_test(unittest.TestCase):

    def setUp(self):
        pass

    def test_default_ok(self):
        _record = generate_purchases(10, 50, 2, 100)
        self.assertEqual(len(list(_record)), 50)

    def test_generate_purchases_with_value_of_totalcontracts_less_than_double_value_of_totalagents(self):
        errmsgs = 'variance must be greater than 0'
        check_num = 0

        for i in range(5):
            check_num += 1
            with self.assertRaisesRegex(Exception) as context:
                generate_purchases(10, random.randint(0, 19), 100, 10000000)
                self.assertEqual(errmsgs, context.exception)

        self.assertEqual(check_num, 5)

    def test_length_of_purchases_ids(self):
        _records = generate_purchases(10, 20, 50, 100000)
        check_num = 0
        check_bool = True

        for _record in list(_records):
            check_num += 1
            if not 12 == len(_record['id']):
                check_bool = False

        self.assertEqual(check_bool, True)
        self.assertEqual(check_num, 20)



