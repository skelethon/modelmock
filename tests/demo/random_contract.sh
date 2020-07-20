#!/bin/bash

PYTHONPATH=./src \
python -B - << EOF
from pprint import pprint
from modelmock.fakers import ContractsFaker

pprint(ContractsFaker.generate_contract(
  id=1,
  price=15,
  multiplier=1000000,
  extra_descriptor=dict(
    total_min=3,
    total_max=7,
    type_choices=[1, 1, 2, 3],
    price_choices=[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    period_choices=[6, 12, 12, 12, 12, 24, 36],
  )
))
EOF
