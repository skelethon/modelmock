#!/usr/bin/env python

from jsonfaker.utils import (
  array_random_split,
  number_to_id,
  generate_ids,
  shuffle_nodes,
)

def generate_agents(total_agents, level_mappings, subpath='record'):
  _records = shuffle_nodes(flatten_refs(expand_treemap(assign_levels(None,
      indices=list(shuffle_nodes(generate_ids(total_agents, 'A'))),
      levels=level_mappings))))
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


def list_to_dict(nodes):
  _map = dict()
  for node in nodes:
    _map[node['index']] = node
  return _map


def expand_treemap(nodes):
  _lkup = list_to_dict(nodes)
  for node in nodes:
    node['refs'] = dict()
    node['refs'][node['level']] = node['index']

    _super_id = node['super']
    if _super_id is None:
      continue

    _super = _lkup[_super_id]
    _super_refs = _super['refs']

    for ref_label in _super_refs.keys():
      node['refs'][ref_label] = _super_refs[ref_label]

  return nodes


def flatten_refs(nodes):
  for node in nodes:
    for _ref_label in node['refs'].keys():
      node['REFS_' + _ref_label] = node['refs'][_ref_label]
    del node['refs']
  return nodes
