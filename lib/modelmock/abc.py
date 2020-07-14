#!/usr/bin/env python3

import abc

class AbstractSeqFaker(metaclass=abc.ABCMeta):

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
