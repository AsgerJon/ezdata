"""EZNamespace is a subclass of 'dict' which provides the namespace
class used by the ezmeta metaclass to create the ezdata class."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import builtins
import sys
from typing import Any, Callable

from icecream import ic
from vistutils import monoSpace, stringList
from vistutils.metas import AbstractNamespace

from ezdata import Entry, EZField

ic.configureOutput(includeContext=True)


class EZNamespace(AbstractNamespace):
  """EZNamespace is a subclass of 'dict' which provides the namespace
  class used by the EZMeta metaclass to create the EZData class."""

  @staticmethod
  def _getCommonDefaults() -> dict[type, Any]:
    """Getter-function for default values of common types"""
    return {int : 0, float: 0, complex: 0j, str: '', list: [], set: set(),
            dict: dict(), type: object}

  @classmethod
  def _createDefaultInstance(cls, type_: type) -> Any:
    """Creates a default instance of the given type"""
    if isinstance(type_, str):
      cls._createDefaultInstance(cls.resolveType(type_))
    if hasattr(type_, '__default_instance__'):
      defVal = getattr(type_, '__default_instance__')
      if isinstance(defVal, type_):
        return defVal
      defVal = defVal()
      if isinstance(defVal, type_):
        return defVal
      raise TypeError
    defaults = cls._getCommonDefaults()
    if type_ in defaults:
      return defaults.get(type_)
    instance = type_()
    if isinstance(instance, type_):
      return instance

  @staticmethod
  def _getGlobalTypes() -> dict[str, type]:
    """Getter-function for the types in the global scope"""
    globalScope = globals() | builtins.__dict__
    out = {}
    for (key, val) in globalScope.items():
      if isinstance(val, type):
        out |= {key: val}
    return out

  @classmethod
  def resolveType(cls, namedType: str) -> type:
    """Resolves the name of the type and returns the actual type."""
    for (key, val) in cls._getGlobalTypes().items():
      if namedType in [val.__name__, val.__qualname__, key]:
        return val
    e = """Unable to resolve the name: '%s' as the name of a type defined 
    in the global scope! """
    raise NameError(monoSpace(e % namedType))

  def __init__(self, name, bases, *args, **kwargs) -> None:
    self.__class_name__ = name
    self.__class_bases__ = bases
    self.__callable_space__ = []
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

  def __explicit_get_item__(self, key: str, ) -> Any:
    """Implementation of item retrieval. """
    return dict.__getitem__(self, key)

  def __explicit_set_item__(self, key: str, val: Any, old: Any) -> None:
    """Implementation of item setting"""
    if callable(val):
      self.__callable_space__.append((key, val))
    return dict.__setitem__(self, key, val)

  def __explicit_del_item__(self, key: str, oldVal: Any, ) -> Any:
    """Implementation of item deletion"""
    return dict.__delitem__(self, key)

  def getAnnotations(self) -> dict:
    """Getter-function for the annotations"""
    __annotations__ = []
    for log in self.__access_log__:
      if log.get('key') == '__annotations__':
        val = log.get('val')
        if val not in __annotations__:
          __annotations__.append(val)
    return [{}, *__annotations__][-1]

  def getDescriptorFields(self) -> list[EZField]:
    """Getter-function for data fields"""
    out = []
    for (key, val) in self.getAnnotations().items():
      name = key
      type_ = self.resolveType(val)
      defVal = self._createDefaultInstance(type_)
      ezField = EZField(defVal, type_)
      ezField.setFieldName(name)
      out.append(ezField)
    return out

  def compile(self) -> dict:
    """This method creates the simplified namespace. This is what the
    metaclass should pass on to the type.__new__ call"""
    namespace = {}
    for (key, callMeMaybe) in self.__callable_space__:
      namespace |= {key: callMeMaybe}
    for ezField in self.getDescriptorFields():
      namespace |= {ezField.getFieldName(): ezField}
    return namespace
