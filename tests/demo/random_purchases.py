
import os, sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')

from pprint import pprint

from modelmock.fakers import (generate_purchases)

pprint(list(generate_purchases(
  total_agents=100,
  total_contracts=300,
  contract_price=15,
  multiplier=1000000,
)))
