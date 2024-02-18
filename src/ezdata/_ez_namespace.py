"""EZNamespace is a subclass of 'dict' which provides the namespace
class used by the ezmeta metaclass to create the ezdata class."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import builtins
from typing import Any, Callable

from icecream import ic
from vistutils import monoSpace
from vistutils.metas import AbstractNamespace
from vistutils.waitaminute import typeMsg

from ezdata import EZField

ic.configureOutput(includeContext=True)


class EZNamespace(AbstractNamespace):
  """EZNamespace is a subclass of 'dict' which provides the namespace
  class used by the EZMeta metaclass to create the EZData class."""

  __illegal_attribute_names__ = [
    '__init__', '__new__'
  ]

  def _validateAttributeName(self, name: str) -> str:
    """This method validates the given name by comparing against the list
    of reserved and banned names that derived classes are not allowed to
    implement. """
    if name in self.__illegal_attribute_names__:
      e = """When creating class: '%s', the namespace object encountered: 
      name: '%s', which EZData classes are not allowed to implement!
      
      EZData classes use a special instance creation process. This 
      process does not use __new__ nor __init__, and for this reason those 
      names are banned. This error can be suppressed by using the keyword 
      argument _root to any value besides None. Please note that even then
      the __new__ and the __init__ are both ignored entirely."""
      raise AttributeError(e % self.__class_name__, name)
    return name

  def __init__(self, name, bases, *args, **kwargs) -> None:
    self.__class_name__ = name
    self.__class_bases__ = bases
    self.__callable_space__ = {}
    self.__field_space__ = {}
    data = kwargs
    for arg in args:
      if isinstance(arg, (tuple, list)):
        if len(arg) == 1:
          data |= {arg[0]: None}
        if len(arg) == 2:
          data |= {arg[0]: arg[1]}
        if len(arg) > 2:
          data |= {arg[0]: (*arg[1:],)}
    AbstractNamespace.__init__(self, **data)

  def getAnnotations(self) -> dict:
    """Getter-function for the annotations"""
    __annotations__ = []
    for log in self.__access_log__:
      if log.get('key') == '__annotations__':
        val = log.get('val')
        if val not in __annotations__:
          __annotations__.append(val)
    return [{}, *__annotations__][-1]

  def __setitem__(self, key: str, value: Any) -> None:
    """Reimplementation collecting names set to non-callables"""
    AbstractNamespace.__setitem__(self, key, value)
    if callable(value):
      return self._setCallable(key, value)
    self._setField(key, value)

  def _setCallable(self, key: str, callMeMaybe: Callable) -> None:
    """Collecting named callable"""
    if not callable(callMeMaybe):
      e = typeMsg('callMeMaybe', callMeMaybe, Callable)
      raise TypeError(e)
    existingValues = self.__callable_space__.get(key, [])
    self.__callable_space__ |= {key: [callMeMaybe, *existingValues]}

  def _setField(self, key: str, value: Any) -> None:
    """Collecting named field"""
    if callable(value):
      e = """Received callable where field was expected!"""
      raise TypeError(e)
    if key in self.__field_space__:
      val = self.__field_space__.get(key)
      e = """Attribute name: '%s' already set to: '%s', but received new 
      value later in class body: '%s'! Only methods support overloading."""
      raise NameError(monoSpace(e % (key, val, value)))
    self.__field_space__ |= {key: value}

  def compile(self) -> dict:
    """Compiles the namespace object into a dictionary"""
    
