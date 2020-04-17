#!/usr/bin/env python

import numpy as np
import random

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

def number_to_id(number, prefix='A', pad_size=4):
  return prefix + '_' + str(number).zfill(pad_size)


def generate_ids(max, prefix='A'):
  return map(lambda x: number_to_id(x, prefix), range(max))

def shuffle_nodes(nodes):
  new_nodes = np.array(list(nodes))
  np.random.shuffle(new_nodes)
  return new_nodes

def list_to_dict(nodes):
  _map = dict()
  for node in nodes:
    _map[node['index']] = node
  return _map
