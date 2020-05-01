
import os, sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')

from pprint import pprint

from jsonfaker.faker import generate_agents

if True:
  pprint(list(generate_agents(10,
      [
        {'level': 'ND', 'count': 1},
        {'level': 'RD', 'count': 2},
        {'level': 'DD', 'count': 2},
        {'level': 'SD', 'count': 4},
        {'level': 'AM', 'count': 0},
        {'level': 'SM', 'min': 2, 'max': 10},
        {'level': 'ST', 'count': 0},
        {'level': 'SA', 'count': 0}
      ])))
