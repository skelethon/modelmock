#!/usr/bin/env python3

import argparse
import json
import sys
from pprint import pprint
from elgoogapi.auth.oauthlib.flow import authorize
from modelmock.fakers import AgentsFaker, CandidatesFaker, PromotionCodeFaker, ContractsFaker
from modelmock.fakers import generate_purchases
from modelmock.utils import pick_object_fields

def main(argv=sys.argv):
  parser = argparse.ArgumentParser(prog='python3 -m modelmock')
  subparsers = parser.add_subparsers(help='Sub-commands', dest='sub_command')

  # create the parser for the "generate" command
  generate_abc_parser = subparsers.add_parser('generate', help='Generate a type-based collection of records')
  generate_subparsers = generate_abc_parser.add_subparsers(help='[generate] sub-commands', dest='generated_target')

  generate_agents_parser = generate_subparsers.add_parser('agents', help='Generate a collection of agents')
  generate_agents_parser.add_argument("--total", type=int, help="Number of agents will be generated")
  generate_agents_parser.add_argument("--mappings", type=str, help="level_mappings in JSON format")
  generate_agents_parser.add_argument("--language", type=str, help="The language which used to generate the user information (phone, email, name, ...)")

  generate_candidates_parser = generate_subparsers.add_parser('candidates', help='Generate a collection of candidates')
  generate_candidates_parser.add_argument("--total", type=int, help="Number of candidates will be generated")

  generate_promocodes_parser = generate_subparsers.add_parser('promocodes', help='Generate a collection of promotion-codes')
  generate_promocodes_parser.add_argument("--total", type=int, help="Number of promotion-codes will be generated")

  generate_contracts_parser = generate_subparsers.add_parser('contracts', help='Generate a collection of contracts')
  generate_contracts_parser.add_argument("--total", type=int, required=True, help="Number of contracts will be generated")
  generate_contracts_parser.add_argument("--price", type=int, required=True, help="Average price of contracts will be generated")
  generate_contracts_parser.add_argument("--multiplier", type=int, default=1, help="Multiplier of contract price (1, 10, 100, 1000, ...)")

  generate_purchases_parser = generate_subparsers.add_parser('purchases', help='Generate a collection of purchases')
  generate_purchases_parser.add_argument("--total_agents", type=int, required=True, help="Number of agents associated with purchases")
  generate_purchases_parser.add_argument("--total_contracts", type=int, required=True, help="Number of contracts associated with purchases")
  generate_purchases_parser.add_argument("--contract_price", type=int, required=True, help="Average price of purchases will be generated")
  generate_purchases_parser.add_argument("--multiplier", type=int, default=1, help="Multiplier of contract price (1, 10, 100, 1000, ...)")

  args = parser.parse_args(args=argv[1:])

  if args.sub_command == 'generate':
    if args.generated_target == 'agents':
      display(AgentsFaker(**dict(
        total_agents=args.total,
        level_mappings=json.loads(args.mappings),
        language=args.language,
      )))
      return 0
    if args.generated_target == 'candidates':
      display(CandidatesFaker(args.total))
      return 0
    if args.generated_target in ['promocodes', 'promotion-codes', 'promotion_codes']:
      display(PromotionCodeFaker(args.total))
      return 0
    if args.generated_target == 'contracts':
      display(ContractsFaker(**dict(
        total_contracts=args.total,
        contract_price=args.price,
        multiplier=args.multiplier,
      )))
      return 0
    if args.generated_target == 'purchases':
      pprint(list(generate_purchases(**pick_object_fields(args, ['total_agents', 'total_contracts', 'contract_price', 'multiplier']))))
      return 0

  parser.print_help()
  return -1

def display(_faker):
  _total = _faker.total
  _count = 0
  sys.stdout.write('[' + '\n')
  for item in _faker.records:
    _count += 1
    sys.stdout.write('  ' + json.dumps(item, ensure_ascii=False) + (',\n' if _count<_total else '\n'))
  sys.stdout.write(']' + '\n')

if __name__ == "__main__":
  sys.exit(main(sys.argv))
