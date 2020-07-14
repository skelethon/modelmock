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
  wrap_nodes,
)
from modelmock.user_info import Generator as UserGenerator


# [BEGIN AgentsFaker]

class AgentsFaker(object):

  def __init__(self, total_agents, level_mappings, subpath='record', id_prefix='A', id_padding=4, language='vi_VN', **kwargs):
    self.__total_agents = total_agents
    assert isinstance(self.__total_agents, int) and self.__total_agents > 0,\
        'total_agents must be a positive integer'

    self.__level_mappings = level_mappings
    assert isinstance(self.__level_mappings, list),\
        'level_mappings must be a list'

    self.__subpath = subpath
    self.__id_prefix = id_prefix
    self.__id_padding = id_padding
    self.__language = language

  @property
  def total(self):
    return self.__total_agents

  def generate(self):
    return self._generate_agents(self.__total_agents, self.__level_mappings,
        subpath=self.__subpath,
        id_prefix=self.__id_prefix,
        id_padding=self.__id_padding,
        language=self.__language)

  @classmethod
  def _generate_agents(cls, total_agents, level_mappings, subpath='record', id_prefix='A', id_padding=4, language='en'):
    _records = UserGenerator(language=language).inject_user_info(
      flatten_sub_dict(
        generatorify(
          cls._expand_tree_path(
            cls._assign_levels(None,
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

  @classmethod
  def _expand_tree_path(cls, nodes, index_name='index', level_name='level', super_name='super', prior_list='refs'):
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

  @classmethod
  def _assign_levels(cls, super_id, indices, levels):
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
          return cls._assign_levels(super_id, indices, levels)
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
          ret = ret + cls._assign_levels(first_index, subchild, levels = levels)
    return ret

# [END AgentsFaker]


class CandidatesFaker(object):

  def __init__(self, total_candidates, **kwargs):
    self.__total_candidates = total_candidates
    assert isinstance(self.__total_candidates, int) and self.__total_candidates > 0,\
        'total_candidates must be a positive integer'

    _language = kwargs['language'] if 'language' in kwargs else None
    self.__user_info_faker = UserGenerator(language=_language)

  def generate(self):
    _ids = generate_ids(self.__total_candidates, prefix='CAN', padding=10)
    return self.__user_info_faker.inject_user_info(wrap_nodes(_ids, field_name='id'))

  @property
  def total(self):
    return self.__total_candidates


class PromotionCodeFaker(object):

  def __init__(self, total_codes, spread_limit=5, **kwargs):
    self.__total_codes = total_codes
    assert isinstance(self.__total_codes, int) and self.__total_codes > 0,\
        'total_codes must be a positive integer'

    self.__spread_limit = spread_limit
    assert isinstance(self.__spread_limit, int) and self.__spread_limit > 0 and self.__spread_limit <= self.__total_codes,\
        'spread_limit must be a positive integer'

    self.__referral_targets = dict()

  def __pick_a_referral_code(self):
    _referral_code = None
    _avail_codes = list(filter(lambda _key: (len(self.__referral_targets[_key]) < self.__spread_limit), self.__referral_targets.keys()))
    if len(_avail_codes) > 2:
      _referral_code = _avail_codes[random.randint(0, len(_avail_codes) - 1)]
    return _referral_code

  def generate(self):
    _procodes = generate_ids(self.__total_codes, prefix='PC', padding=10)
    for _procode in _procodes:
      _referral_code = self.__pick_a_referral_code()
      if _referral_code is not None:
        self.__referral_targets[_referral_code].append(_procode)
      self.__referral_targets[_procode] = []
      yield dict(promotion_code=_procode, referral_code=_referral_code)

  @property
  def total(self):
    return self.__total_codes


# [BEGIN ContractsFaker]

class ContractsFaker(object):

  def __init__(self, total_contracts, contract_price, unit=1, id_prefix='CONTR', id_padding=6, flatten=True, **kwargs):
    self.__total_contracts = total_contracts
    assert isinstance(self.__total_contracts, int) and self.__total_contracts > 0,\
        'total_contracts must be a positive integer'

    self.__contract_price = contract_price
    assert isinstance(self.__contract_price, int) and self.__contract_price > 0,\
        'contract_price must be a positive integer'

    self.__unit = unit
    self.__id_prefix = id_prefix
    self.__id_padding = id_padding
    self.__flatten = flatten

  @property
  def total(self):
    return self.__total_contracts

  def generate(self):
    return self.__generate_contracts(self.__total_contracts, self.__contract_price,
        unit=self.__unit,
        id_prefix=self.__id_prefix,
        id_padding=self.__id_padding,
        flatten=self.__flatten)

  def __generate_contracts(self, total_contracts, contract_price, unit, id_prefix='CONTR', id_padding=6, flatten=True):
    # estimate the revenue ~ price * total
    _revenue = contract_price * total_contracts

    # randomize the prices (length: total_contracts)
    _prices = random_fixed_sum_array(_revenue, total_contracts)

    # common kwargs
    _args_tail = dict(unit=unit, id_prefix=id_prefix, id_padding=id_padding, flatten=flatten)

    # generate each contracts
    return map(lambda idx, price: self.__generate_contract(idx, price, **_args_tail), range(total_contracts), _prices)


  def __generate_contract(self, idx, price, unit, id_prefix='C', id_padding=6, max_extras=5, flatten=True, extra_generator=None):
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

# [END ContractsFaker]


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


def generate_agents(total_agents, level_mappings, subpath='record', id_prefix='A', id_padding=4, language='en'):
  faker = AgentsFaker(total_agents, level_mappings,
      subpath=subpath,
      id_prefix=id_prefix,
      id_padding=id_padding,
      language=language)
  return faker.generate()


def generate_contracts(total_contracts, contract_price, unit, **kwargs):
  myargs = dict(total_contracts=total_contracts, contract_price=contract_price, unit=unit)
  myargs.update(kwargs)
  return ContractsFaker(**myargs).generate()
