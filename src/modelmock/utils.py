#!/usr/bin/env python

import numpy as np
import random
import shortuuid

def array_random_split(arr, n, empty_accepted=False):
  ret = []
  arr_len = len(arr)
  first = 0 if empty_accepted else 1
  for i in range(n):
    if i == n-1:
      ret.append(arr)
    else:
      subarr_len = random.randint(first, arr_len - (n - i - 1))
      ret.append(arr[:subarr_len])
      arr = arr[subarr_len:]
      arr_len = len(arr)
  return ret


def number_to_id(number, prefix='A', padding=4):
  return prefix + '_' + str(number).zfill(padding)


def generate_ids(max, prefix='A', padding=4, shuffle=False):
  _ids = range(max)
  if shuffle:
    _ids = list(_ids)
    random.shuffle(_ids)
  return map(lambda x: number_to_id(x, prefix=prefix, padding=padding), _ids)


def generate_uuids(max):
  for i in range(max):
    yield shortuuid.uuid()

def dictify(data=None, nested_field_name='nested_data'):
  if isinstance(data, dict):
    return data
  if data is None:
    return dict()
  return { nested_field_name: data }


def wrap_nodes(nodes, field_name=None):
  if not isiterable(nodes) or not isinstance(field_name, str):
    return nodes
  for node in nodes:
    yield { field_name: node }


def set_deep_child(node, root=None, path=[]):
  if path is None or not isinstance(path, list):
    return node

  if root is not None and not isinstance(root, dict):
    return node

  _tmp = node
  for i in range(len(path)):
    _tmp = { str(path[-i-1]): _tmp }

  if not isinstance(_tmp, dict):
    return node

  if root is None:
    root = _tmp
  else:
    root.update(_tmp)

  return root


def shuffle_nodes(nodes):
  new_nodes = np.array(list(nodes))
  np.random.shuffle(new_nodes)
  return new_nodes


def list_to_dict(nodes, key_name='index'):
  _map = dict()
  for node in nodes:
    _map[node[key_name]] = node
  return _map


def random_fixed_sum_array(_sum, n):
  mean = _sum // n
  variance = int(0.5 * mean)

  min_v = mean - variance
  max_v = mean + variance
  array = [min_v] * n

  diff = _sum - min_v * n
  while diff > 0:
    a = random.randint(0, n - 1)
    if array[a] >= max_v:
      continue
    array[a] += 1
    diff -= 1

  return array


def flatten_sub_dict(nodes, subdict_name='refs', prefix='REFS'):
  if not isiterable(nodes):
    return nodes
  for node in nodes:
    if isinstance(node, dict) and subdict_name in node and isinstance(node[subdict_name], dict):
      for _ref_label in node[subdict_name].keys():
        node[prefix + '_' + _ref_label] = node[subdict_name][_ref_label]
      del node[subdict_name]
    yield node


def flatten_sub_list(contract, list_name='extras', prefix='extra'):
  if not isinstance(contract, dict):
    return contract
  if list_name not in contract or not isinstance(contract[list_name], list):
    return contract
  _extras = contract[list_name]
  for _i in range(len(_extras)):
    _extra = _extras[_i]
    for _f in _extra.keys():
      contract['_'.join([prefix, str(_i), str(_f)])] = _extra[_f]
  del contract[list_name]
  return contract


def chunkify(array, size):
  """
  Yield successive fixed n-length chunks from an array.
  """
  for i in range(0, len(array), size):
    yield array[i:i + size]


def isiterable(obj):
  try:
    iter(obj)
  except Exception:
    return False
  else:
    return True


def generatorify(nodes, cloned=True):
  for node in nodes:
    if cloned and isinstance(node, dict):
      yield node.copy()
    else:
      yield node


def pick_object_fields(obj, field_names=[]):
  if len(field_names) == 0:
    return obj
  if isinstance(obj, dict):
    return {k: v for k, v in obj.items() if k in field_names}
  if isinstance(obj, object):
    output = dict()
    for field_name in field_names:
      if hasattr(obj, field_name):
        output[field_name] = getattr(obj, field_name)
    return output


