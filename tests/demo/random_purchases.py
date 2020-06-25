
import os, sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')

from pprint import pprint

from modelmock.faker import (generate_purchases)

pprint(generate_purchases(
  contract_price=15,
  total_contracts=300,
  total_agents=100,
  unit=1000000,
))
