#!/bin/bash

PYTHONPATH=./src/ \
python3 -m modelmock generate candidates \
--total=10
