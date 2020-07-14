#!/usr/bin/env python3

import argparse
import json
import sys
from pprint import pprint
from elgoogapi.auth.oauthlib.flow import authorize
from modelmock.faker import (CandidatesFaker, PromotionCodeFaker)

def main(argv=sys.argv):
  parser = argparse.ArgumentParser(prog='python3 -m modelmock')
  subparsers = parser.add_subparsers(help='Sub-commands', dest='sub_command')

  # create the parser for the "authen" command
  parser_generate = subparsers.add_parser('generate', help='Generate a type-based collection of records')
  parser_generate.add_argument("--type", type=str, choices=['Agents', 'Candidates', 'PromotionCodes', 'Contracts'],
      help="Type of record will be generated")

  parser_generate.add_argument("--total", type=int,
      help="Number of items will be generated")

  parser_generate.add_argument("--options", type=str, default="{}", required=False,
      help="The options in the JSON format")

  args = parser.parse_args(args=argv[1:])

  if args.sub_command == 'generate':
    _type = args.type
    if _type == 'Candidates':
      display(CandidatesFaker(args.total))
    if _type == 'PromotionCodes':
      display(PromotionCodeFaker(args.total))
    return 0

  parser.print_help()
  return -1

def display(_faker):
  _total = _faker.total
  _count = 0
  sys.stdout.write('[' + '\n')
  for item in _faker.records:
    _count += 1
    sys.stdout.write('  ' + json.dumps(item) + (',\n' if _count<_total else '\n'))
  sys.stdout.write(']' + '\n')

if __name__ == "__main__":
  sys.exit(main(sys.argv))
