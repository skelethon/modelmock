#!/bin/bash

read -r -d '' LEVEL_MAPPINGS <<EOF
[
  {
    "level": "ND",
    "count": 1
  },
  {
    "level": "RD",
    "count": 2
  },
  {
    "level": "DD",
    "count": 2
  },
  {
    "level": "SD",
    "count": 4
  },
  {
    "level": "AM",
    "count": 0
  },
  {
    "level": "SM",
    "min": 2,
    "max": 10
  },
  {
    "level": "ST",
    "count": 0
  },
  {
    "level": "SA",
    "count": 0
  }
]
EOF

PYTHONPATH=./lib/ \
python3 -m modelmock generate agents \
--total=10 \
--mappings="$LEVEL_MAPPINGS" \
--language=vi_VN
