"""EZNamespace is a subclass of 'dict' which provides the namespace
class used by the ezmeta metaclass to create the ezdata class."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import builtins
import sys

from ezdata import Entry
from utilities import TypedField, ListField, DictField, monoSpace

if sys.version_info >= (3, 8):
  Bases = list[type]
else:
  from typing import List

  Bases = List[type]


class EZNamespace(dict):
  """EZNamespace is a subclass of 'dict' which provides the namespace
  class used by the EZMeta metaclass to create the EZData class."""

  entryLog = ListField(Entry)
  className = TypedField(str)
  baseClasses = ListField(type)
  initGlobals = DictField(tuple)
  initLocals = DictField(tuple)

  def __init__(self, *args, **kwargs) -> None:
    dict.__init__(self, *args, **kwargs)
    self.initGlobals = globals()
    self.initLocals = locals()

  def append(self, *args, ) -> Entry:
    """Appends an entry to the inner contents list"""
    entry = Entry(*args, )
    if isinstance(self.entryLog, list):
      self.entryLog.append(entry)
    return entry

  def __getitem__(self, key: str, ) -> object:
    """Implementation of item retrieval"""
    try:
      value = dict.__getitem__(self, key)
    except KeyError as keyError:
      self.append('__getitem__', 'key-ERROR: %s' % key, keyError)
      raise keyError
    self.append('__getitem__', key, value)
    return value

  def __setitem__(self, key: str, value: object) -> None:
    """Implementation of item assignment"""
    dict.__setitem__(self, key, value)
    self.append('__setitem__', key, value)

  def __delitem__(self, key: str) -> None:
    """Implementation of item deletion"""
    dict.__delitem__(self, key)
    self.append('__delitem__', key, 'NA')

  def _getTypes(self) -> dict:
    """Getter-function for the types found in globals and locals"""
    types = {}
    for data in [self.initGlobals, self.initLocals, builtins.__dict__]:
      for (key, val) in data.items():
        types = {**types, **{key: val}}
    return types

  def _identifyClass(self, className: str) -> type:
    """This method attempts to recognize the class the given name refers
    to."""
    types = self._getTypes()
    return self._getTypes().get(className, object)

  def getFields(self) -> dict:
    """Getter-function for the fields named in the '__annotations__'.
    fields = namespace.getFields()
    #  Is equivalent to:
    fields = {varName: {className: fieldClass, value: instanceValue}}"""
    out = {}
    __annotations__ = {**self.get('__annotations__', {}), }

    if __annotations__ is None:
      raise AttributeError('__annotations__')
    if isinstance(__annotations__, dict):
      for (key, val) in __annotations__.items():
        fieldClass = self._identifyClass(val)
        if fieldClass is object:
          e = """Did not recognize '%s' as the name of a class!"""
          raise NameError(monoSpace(e % val))
        entry = dict(fieldName=key,
                     fieldClassName=val,
                     fieldClassType=fieldClass,
                     defaultValue=self.get(key, None))
        out = {**out, **{key: entry}}
      return out
    e = """Expected annotations to be of type 'dict', but received '%s' of 
    type '%s'!"""
    raise TypeError(monoSpace(e % (__annotations__, type(__annotations__))))

  def _getFuncs(self, ) -> list:
    """Getter-function for the entries whose values are functions"""
    return [entry for entry in self.entryLog if entry.isFunction()]

  def getFuncNamespace(self) -> dict:
    """Getter-function for the functions in the namespace"""
    namespace = {}
    for entry in self._getFuncs():
      namespace = {**namespace, **{entry.key: entry.value}}
    return namespace
