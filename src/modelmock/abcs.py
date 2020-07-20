#!/usr/bin/env python3

import abc
from modelmock.utils import generate_ids, generate_uuids

class AbstractSeqFaker():
  __metaclass__ = abc.ABCMeta

  def __init__(self, **kwargs):
    pass

  @abc.abstractproperty
  def total(self):
    pass

  @abc.abstractproperty
  def records(self):
    pass

  @classmethod
  def __subclasshook__(cls, C):
    if cls is AbstractSeqFaker:
      attrs = set(dir(C))
      if set(cls.__abstractmethods__) <= attrs:
        return True
    return NotImplemented


class IdentifiableSeqFaker(AbstractSeqFaker):

  def __init__(self, total, id_method=None, id_prefix='A', id_padding=4, id_shuffle=True, **kwargs):
    assert isinstance(total, int) and total > 0, '[total] must be a positive integer'
    self.__total = total

    assert id_method is None or isinstance(id_method, str), '[id_method] must be a string (incr, uuid)'
    self.__id_method = 'incr' if id_method is None else id_method

    assert isinstance(id_prefix, str) and len(id_prefix) > 0, '[id_prefix] must be a non-empty string'
    self.__id_prefix = id_prefix

    assert isinstance(id_padding, int) and id_padding > 0, '[id_padding] must be a positive integer'
    self.__id_padding = id_padding

    if isinstance(id_shuffle, str):
      self.__id_shuffle = id_shuffle.lower() in ['yes', 'true', '1']
    else:
      self.__id_shuffle = bool(id_shuffle)

    self.__ids = None

  @property
  def total(self):
    return self.__total

  @property
  def ids(self):
    if self.__ids is None:
      if self.__id_method == 'uuid':
        self.__ids = generate_uuids(self.total)
      else:
        self.__ids = generate_ids(self.total, prefix=self.__id_prefix, padding=self.__id_padding, shuffle=self.__id_shuffle)
    return self.__ids


class AbstractInjector():
  __metaclass__ = abc.ABCMeta

  def __init__(self, **kwargs):
    pass

  @abc.abstractmethod
  def inject(self, data):
    pass

  @classmethod
  def __subclasshook__(cls, C):
    if cls is AbstractInjector:
      attrs = set(dir(C))
      if set(cls.__abstractmethods__) <= attrs:
        return True
    return NotImplemented
