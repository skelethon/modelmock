#!/usr/bin/env python3

from datetime import datetime, timedelta
from modelmock.utils import dictify, isiterable
import random

class DateTimeInjector(object):

  def __init__(self, total, descriptors, **kwargs):
    self.__total = total
    assert isinstance(self.__total, int) and self.__total > 0,\
        'total must be a positive integer'

    assert isinstance(descriptors, list),\
        'descriptors must be a list'

    self.__randomizers = []
    for i, descriptor in enumerate(descriptors):
      self.__randomizers.append(DateTimeRandomizer(total, **descriptor))

    self.__randomizers = sorted(self.__randomizers, key= lambda r: r.step)

  def inject(self, data):
    if isiterable(data):
      for node in data:
        yield self.__gen_times(node)
    else:
      return self.__gen_times(data)

  def __gen_times(self, data):
    data = dictify(data)
    prev_step = 0
    prev_time = None
    for randomizer in self.__randomizers:
      if randomizer.step > prev_step:
        current = randomizer.next(prev_time)
        prev_time = current
        prev_step = randomizer.step
      else:
        current = randomizer.next()
      if randomizer.format is None:
        data[randomizer.name] = current
      else:
        data[randomizer.name] = current.strftime(randomizer.format)
    return data


class DateTimeRandomizer(object):

  def __init__(self, total, field_name, step=0, offset=0, offset_unit='days', delta_min=0, delta_max=0, delta_unit='days', format=None, **kwargs):
    self.__field_name = field_name
    self.__offset = offset
    self.__offset_unit = offset_unit

    if self.__offset != 0:
      self.__offset_calc = timedelta(**{self.__offset_unit: self.__offset})
    else:
      self.__offset_calc = None

    self.__delta_min = delta_min
    self.__delta_max = delta_max
    self.__delta_unit = delta_unit

    self.__step = step

    self.__format = format

  @property
  def name(self):
    return self.__field_name

  @property
  def format(self):
    return self.__format

  @property
  def step(self):
    return self.__step

  def next(self, current = None):
    current = datetime.now() if current is None else current
    assert isinstance(current, datetime)

    if self.__offset_calc is not None:
      current = current + self.__offset_calc

    if 0 < self.__delta_max:
      _delta = 0

      if self.__delta_min == self.__delta_max:
        _delta = self.__delta_min
      elif self.__delta_min < self.__delta_max:
        _delta = random.randint(self.__delta_min, self.__delta_max)

      if _delta > 0:
        current = current + timedelta(**{ self.__delta_unit: _delta })

    return current
