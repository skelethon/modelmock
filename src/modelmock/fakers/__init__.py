#!/usr/bin/env python3

import random
from modelmock.abcs import AbstractSeqFaker, IdentifiableSeqFaker, AbstractInjector
from modelmock.utils import (
  array_random_split,
  generatorify,
  list_to_dict,
  flatten_sub_dict,
  flatten_sub_list,
  random_fixed_sum_array,
  wrap_nodes,
  get_dict_item,
  propagate_patterns,
)
from modelmock.user_info import Generator as UserGenerator


# [BEGIN EntitiesFaker]

class EntitiesFaker(IdentifiableSeqFaker):

  def __init__(self, total, id_method=None, id_prefix='A', id_padding=4, id_shuffle=True, id_field_name='id', injectors=[], **kwargs):

    IdentifiableSeqFaker.__init__(self, total, id_method, id_prefix, id_padding, id_shuffle)

    assert isinstance(id_field_name, str) and len(id_field_name) > 0, '[id_field_name] must be a non-empty string'
    self.__id_field_name = id_field_name

    self.__injectors = []
    for injector in injectors:
      assert isinstance(injector, AbstractInjector)
      self.__injectors.append(injector)

  @property
  def records(self):
    entities = wrap_nodes(self.ids, field_name=self.__id_field_name)
    for i, entity in enumerate(entities):
      for injector in self.__injectors:
        entity = injector.inject(entity)
      yield entity

# [END EntitiesFaker]


# [BEGIN AgentsFaker]

class AgentsFaker(IdentifiableSeqFaker):

  def __init__(self, total_agents, level_mappings, \
      id_method=None, id_prefix='A', id_padding=4, id_shuffle=True, \
      subpath='record', locale='en_US', **kwargs):

    assert level_mappings is None or isinstance(level_mappings, list), '[level_mappings] must be a list or None'
    self.__level_mappings = level_mappings if level_mappings is not None else []

    assert subpath is None or isinstance(subpath, str) and len(subpath) > 0, '[subpath] must be a non-empty string or None'
    self.__subpath = subpath

    self.__user_info_faker = UserGenerator(locale=locale)

    IdentifiableSeqFaker.__init__(self, total_agents, id_method, id_prefix, id_padding, id_shuffle)

  @property
  def records(self):
    return self._generate_agents(self.ids, self.__level_mappings, self.__user_info_faker, subpath=self.__subpath)

  @classmethod
  def _generate_agents(cls, agent_ids, level_mappings, user_info_faker, subpath='record'):
    _records = user_info_faker.inject_user_info(
      flatten_sub_dict(
        generatorify(
          cls._expand_tree_path(
            cls._assign_levels(None,
              indices=list(agent_ids),
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
    ret = []

    if not isinstance(indices, list) or len(indices) == 0:
      return ret
    if isinstance(levels, list) and len(levels) > 0:
      current = levels[0]
      levels = levels[1:]
      if len(levels) == 0:
        for i in indices:
          ret.append(dict(level=current['level'], index=i, super=super_id))
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
          ret.append(dict(level=current['level'], index=first_index, super=super_id))
          ret = ret + cls._assign_levels(first_index, subchild, levels = levels)
    return ret

# [END AgentsFaker]


# [BEGIN CandidatesFaker]

class CandidatesFaker(IdentifiableSeqFaker):

  def __init__(self, total_candidates, id_method=None, id_prefix='CAN', id_padding=10, id_shuffle=False, locale='en', **kwargs):
    IdentifiableSeqFaker.__init__(self, total_candidates, id_method, id_prefix, id_padding, id_shuffle)
    self.__user_info_faker = UserGenerator(locale=locale)

  @property
  def records(self):
    return self.__user_info_faker.inject_user_info(wrap_nodes(self.ids, field_name='id'))

# [END CandidatesFaker]


# [BEGIN PromocodesFaker]

class PromocodesFaker(IdentifiableSeqFaker):

  def __init__(self, total_codes, id_method=None, id_prefix='PC', id_padding=10, id_shuffle=False, spread_limit=5, **kwargs):
    IdentifiableSeqFaker.__init__(self, total_codes, id_method, id_prefix, id_padding, id_shuffle)

    assert isinstance(spread_limit, int) and spread_limit > 0 and spread_limit <= total_codes, '[spread_limit] must be a positive integer'
    self.__spread_limit = spread_limit

    self.__referral_targets = dict()

  @property
  def records(self):
    for _procode in self.ids:
      _referral_code = self.__pick_a_referral_code()
      if _referral_code is not None:
        self.__referral_targets[_referral_code].append(_procode)
      self.__referral_targets[_procode] = []
      yield dict(promotion_code=_procode, referral_code=_referral_code)

  def __pick_a_referral_code(self):
    _referral_code = None
    _avail_codes = list(filter(lambda _key: (len(self.__referral_targets[_key]) < self.__spread_limit), self.__referral_targets.keys()))
    if len(_avail_codes) > 2:
      _referral_code = _avail_codes[random.randint(0, len(_avail_codes) - 1)]
    return _referral_code

# [END PromocodesFaker]


# [BEGIN ContractsFaker]

class ContractsFaker(IdentifiableSeqFaker):

  def __init__(self, total_contracts, contract_price, multiplier=1, \
      id_method=None, id_prefix='CONTR', id_padding=6, id_shuffle=False, \
      extra_descriptors=[], extra_generator=None, \
      flatten=True, **kwargs):

    assert isinstance(contract_price, int) and contract_price > 0, '[contract_price] must be a positive integer'
    self.__contract_price = contract_price

    assert isinstance(multiplier, int) and multiplier > 0, '[multiplier] must be a positive integer'
    self.__multiplier = multiplier

    self.__extra_descriptors = extra_descriptors
    self.__extra_generator = extra_generator

    self.__flatten = flatten

    IdentifiableSeqFaker.__init__(self, total_contracts, id_method, id_prefix, id_padding, id_shuffle)

  @property
  def records(self):
    return self.__generate_contracts(self.total, self.__contract_price, self.__multiplier, \
      extra_descriptors=self.__extra_descriptors, extra_generator=self.__extra_generator, flatten=self.__flatten)

  def __generate_contracts(self, total_contracts, contract_price, multiplier, extra_descriptors=[], extra_generator=None, flatten=True):
    # estimate the revenue ~ price * total
    _revenue = contract_price * total_contracts

    # randomize the prices (length: total_contracts)
    _prices = random_fixed_sum_array(_revenue, total_contracts)

    # get the extra_descriptors
    _extra_descriptors = self.__class__.select_descriptor(total_contracts, extra_descriptors)

    # common kwargs
    _args_tail = dict(extra_generator=extra_generator, flatten=flatten)

    # generate each contracts
    return map(lambda id, price, extra_descriptor: self.__class__.generate_contract(id, price, multiplier, extra_descriptor, **_args_tail),
        self.ids, _prices, _extra_descriptors)

  @classmethod
  def generate_contract(cls, id, price, multiplier, extra_descriptor=dict(), extra_generator=None, flatten=True):
    total_min = get_dict_item(extra_descriptor, 'total_min', 1)
    total_max = get_dict_item(extra_descriptor, 'total_max', 10)
    price_choices = get_dict_item(extra_descriptor, 'price_choices', range(2, 6))
    type_choices = get_dict_item(extra_descriptor, 'type_choices', [1, 2, 3])
    period_choices = get_dict_item(extra_descriptor, 'period_choices', [12, 24, 36])

    num_extras = random.randint(total_min, total_max)
    if extra_generator is None:
      extras = []
      for id_extras in range(num_extras):
        extras.append(dict(
          fare = random.choice(price_choices) * multiplier,
          type = random.choice(type_choices),
          duration = random.choice(period_choices),
        ))
    else:
      extras = map(extra_generator, range(num_extras))

    _contract = dict(id=id, fyp=price * multiplier, extras=extras)

    if flatten:
      return flatten_sub_list(_contract, list_name='extras', prefix='extra')

    return _contract

  @classmethod
  def select_descriptor(cls, total, descriptors=None):
    descriptors = [] if descriptors is None else descriptors
    amounts = list(map(lambda d: d['total'] if 'total' in d else 1, descriptors))
    for i in propagate_patterns(total, amounts):
      if i >= 0:
        d = descriptors[i]
        if isinstance(d, dict) and 'options' in d:
          yield d['options']
          continue
      yield cls.DEFAULT_EXTRA_DESCRIPTOR


  DEFAULT_EXTRA_DESCRIPTOR = dict(
      total_min=1,
      total_max=10,
      price_choices=[1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 5, 6],
      type_choices=[1, 2, 3],
      period_choices=[12, 24, 36, 48, 60, 72, 72, 72, 84, 96],
  )

# [END ContractsFaker]


# [BEGIN PurchasesFaker]

class PurchasesFaker(AbstractSeqFaker):

  def __init__(self, agents_faker, contracts_faker, **kwargs):
    assert isinstance(agents_faker, AgentsFaker), '[agents_faker] must be an instance of AgentsFaker type'
    self.__agents_faker = agents_faker

    assert isinstance(contracts_faker, ContractsFaker), '[contracts_faker] must be an instance of ContractsFaker type'
    self.__contracts_faker = contracts_faker

  @property
  def total(self):
    return self.__contracts_faker.total

  @property
  def records(self):
    total_agents = self.__agents_faker.total
    total_contracts = self.__contracts_faker.total

    def assign_contract_to_agent(contract, agent_id):
      contract['agent_id'] = agent_id
      return contract

    def select_agent_for_contract(total_contracts, total_agents):
      # assign the contracts to agents
      num_contracts_per_agents = random_fixed_sum_array(total_contracts, total_agents)

      for i, agent_id in enumerate(self.__agents_faker.ids):
        for j in range(num_contracts_per_agents[i]):
          yield agent_id

    return map(assign_contract_to_agent, self.__contracts_faker.records, select_agent_for_contract(total_contracts, total_agents))

# [END PurchasesFaker]


def generate_agents(total, level_mappings, subpath='record', id_prefix='A', id_padding=4, locale='en'):
  faker = AgentsFaker(total, level_mappings,
      subpath=subpath,
      id_prefix=id_prefix,
      id_padding=id_padding,
      locale=locale)
  return faker.records


def generate_contracts(total_contracts, contract_price, multiplier, **kwargs):
  myargs = dict(total_contracts=total_contracts, contract_price=contract_price, multiplier=multiplier)
  myargs.update(kwargs)
  return ContractsFaker(**myargs).records


def generate_purchases(total_agents, total_contracts, contract_price, multiplier, flatten=True,
    agent_id_method=None, agent_id_prefix='AGENT', agent_id_padding=6, agent_id_shuffle=True,
    contract_id_method=None, contract_id_prefix='CONTR', contract_id_padding=6, contract_id_shuffle=True):

  agents_faker = AgentsFaker(total_agents, [],
      id_method=agent_id_method,
      id_prefix=agent_id_prefix,
      id_padding=agent_id_padding,
      id_shuffle=agent_id_shuffle)

  contracts_faker = ContractsFaker(total_contracts, contract_price, multiplier,
      id_method=contract_id_method,
      id_prefix=contract_id_prefix,
      id_padding=contract_id_padding,
      id_shuffle=contract_id_shuffle,
      flatten=flatten)

  return PurchasesFaker(agents_faker, contracts_faker).records
