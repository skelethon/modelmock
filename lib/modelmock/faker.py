#!/usr/bin/env python

import random
from modelmock.utils import (
  array_random_split,
  chunkify,
  number_to_id,
  generate_ids,
  generatorify,
  shuffle_nodes,
  list_to_dict,
  flatten_sub_dict,
  flatten_sub_list,
  random_fixed_sum_array,
)
from modelmock.user_info import Generator as UserGenerator

# [BEGIN generate_agents()]

def generate_agents(total_agents, level_mappings, subpath='record', id_prefix='A', id_padding=4):
  _records = UserGenerator().inject_user_info(
    flatten_sub_dict(
      generatorify(
        expand_tree_path(
          assign_levels(None,
            indices=list(shuffle_nodes(generate_ids(total_agents, prefix=id_prefix, padding=id_padding))),
            levels=level_mappings)
        )
      )
    )
  )

  if isinstance(subpath, str):
    return map(lambda item: { subpath: item }, _records)
  else:
    return _records

def assign_levels(super_id, indices, levels):
  if not isinstance(indices, list):
    raise TypeError('indices is invalid')

  ret = []

  if not isinstance(indices, list) or len(indices) == 0:
    return ret
  if isinstance(levels, list) and len(levels) > 0:
    current = levels[0]
    levels = levels[1:]
    if len(levels) == 0:
      for i in indices:
        item = dict(
          level=current['level'],
          index=i,
          super=super_id
        )
        ret.append(item)
    else:
      # determines the number of branches
      if 'count' in current:
        _count = current['count']
      else:
        _min = current['min'] if 'min' in current else 0
        _max = current['max'] if 'max' in current else len(indices)
        _count = random.randint(_min, _max)
      # no any branch of this level
      if _count == 0:
        return assign_levels(super_id, indices, levels)
      # split the children
      group_len = _count if _count < len(indices) else len(indices)
      child_group = array_random_split(indices, group_len)
      for child in child_group:
        first_index = child[0]
        subchild = child[1:]
        ret.append(dict(
          level=current['level'],
          index=first_index,
          super=super_id
        ))
        ret = ret + assign_levels(first_index, subchild, levels = levels)
  return ret


def expand_tree_path(nodes, index_name='index', level_name='level', super_name='super', prior_list='refs'):
  _lkup = list_to_dict(nodes)
  for node in nodes:
    node[prior_list] = dict()
    node[prior_list][node[level_name]] = node[index_name]

    _super_id = node[super_name]
    if _super_id is None:
      continue

    _super = _lkup[_super_id]
    _super_refs = _super[prior_list]

    for ref_label in _super_refs.keys():
      node[prior_list][ref_label] = _super_refs[ref_label]

  return nodes

# [END generate_agents()]


# [BEGIN generate_contracts()]

def generate_contracts(total_contracts, contract_price, unit, id_prefix='CONTR', id_padding=6, flatten=True):
  # estimate the revenue ~ price * total
  _revenue = contract_price * total_contracts

  # randomize the prices (length: total_contracts)
  _prices = random_fixed_sum_array(_revenue, total_contracts)

  # common kwargs
  _args_tail = dict(unit=unit, id_prefix=id_prefix, id_padding=id_padding, flatten=flatten)

  # generate each contracts
  return map(lambda idx, price: generate_contract(idx, price, **_args_tail), range(total_contracts), _prices)


def generate_contract(idx, price, unit, id_prefix='C', id_padding=6, max_extras=5, flatten=True, extra_generator=None):
    num_extras = random.randint(1, max_extras)
    if extra_generator is None:
      extras = []
      for idx_extras in range(num_extras):
        extras.append(dict(
          fare = random.randint(1,5) * unit,
          type = random.randint(1,3),
          duration = random.randint(1, 12),
        ))
    else:
      extras = map(extra_generator, range(num_extras))
    _contract = dict(id=number_to_id(idx, id_prefix, id_padding), fyp=price * unit, extras=extras)
    if flatten:
      return flatten_sub_list(_contract)
    return _contract


def generate_purchases(contract_price, total_contracts, total_agents, unit, id_prefix='CONTR', id_padding=6, flatten=True, chunky=None):
  # generate the contracts
  _contracts = generate_contracts(total_contracts, contract_price, unit,
      id_prefix=id_prefix,
      id_padding=id_padding,
      flatten=flatten)

  def assign_contract_to_agent(contract, agent_id):
    contract['agent_id'] = agent_id
    return contract

  def select_agent_for_contract(total_contracts, total_agents):
    # assign the contracts to agents
    num_contracts_per_agents = random_fixed_sum_array(total_contracts, total_agents)

    for i in range(len(num_contracts_per_agents)):
      for j in range(num_contracts_per_agents[i]):
        yield number_to_id(i)

  return map(assign_contract_to_agent, _contracts, select_agent_for_contract(total_contracts, total_agents))

# [END generate_contracts()]
