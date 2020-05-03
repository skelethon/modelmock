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
