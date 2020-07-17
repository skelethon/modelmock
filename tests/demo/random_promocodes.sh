#!/bin/bash

PYTHONPATH=./src/ \
python3 -m modelmock generate promocodes \
--total=10000
