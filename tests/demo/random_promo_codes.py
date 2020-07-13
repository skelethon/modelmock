
import os, sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')

from pprint import pprint

from modelmock.faker import (PromotionCodeFaker)

_faker = PromotionCodeFaker(
  total_codes=10000,
  unit=1000000,
)

for item in _faker.generate():
  pprint(item)
