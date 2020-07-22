#!/bin/bash

PYTHONPATH=./src \
python3 - << EOF
from pprint import pprint
from modelmock.fakers import EntitiesFaker
from modelmock.injectors import DateTimeInjector

datetime_injector = DateTimeInjector(10, [
  dict(field_name='created_time', format='%d/%m/%Y'),
  dict(field_name='enabled_time', format='%d/%m/%Y', delta_unit='days', delta_min=0, delta_max=5, step=1),
  dict(field_name='updated_time', format='%d/%m/%Y', delta_unit='days', delta_min=0, delta_max=15, step=2),
])

faker = EntitiesFaker(10, injectors=[datetime_injector])
for r in faker.records:
  pprint(r)
EOF
