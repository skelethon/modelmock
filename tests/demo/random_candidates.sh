#!/bin/bash

PYTHONPATH=./src \
python3 -B -m modelmock generate candidates \
--total=10
