
import os, sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')

from pprint import pprint
from modelmock.faker import generate_agents
from modelmock.utils import shuffle_nodes

_demo = os.environ.get('MODELMOCK_DEMO_GEN_AGENTS', '1')

if _demo == '1':
  pprint(list(shuffle_nodes(generate_agents(100,
      [
        {'level': 'ND', 'count': 1},
        {'level': 'RD', 'count': 2},
        {'level': 'DD', 'count': 2},
        {'level': 'SD', 'count': 4},
        {'level': 'AM', 'count': 0},
        {'level': 'SM', 'min': 2, 'max': 10},
        {'level': 'ST', 'count': 0},
        {'level': 'SA', 'count': 0}
      ],
      language='vi_VN'))))

if _demo == '2':
  pprint(list(shuffle_nodes(generate_agents(7,
      [
        {'level': 'ST', 'count': 2},
        {'level': 'SA', 'count': 3}
      ]))))
