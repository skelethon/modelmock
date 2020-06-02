import random
from pprint import pprint

f = lambda x: 2*x

print('X:' + str(f(10)))

def generate_data(arr, generate_item=None):
  if generate_item is None:
    return arr
  return map(generate_item, arr)

arr = [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]

def gen(item):
  newitem = dict(c=random.randint(1, 10))
  newitem.update(item)
  return newitem

pprint(list(generate_data(arr, gen)))
