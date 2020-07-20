#!/bin/bash

PYTHONPATH=./src \
python3 -B -m modelmock generate promocodes \
--total=10000
