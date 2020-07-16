#!/bin/bash

PYTHONPATH=./lib/ python3 -m modelmock generate purchases \
--total_agents=100 \
--total_contracts=600 \
--contract_price=15 \
--multiplier=1000000
