"""Instances of the Entry class describes access events to instances of
the namespace class."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys

from utilities import TypedField, ListField

if sys.version_info < (3, 11):
  from typing_extensions import Self
else:
  from typing import Self


class Entry:
  """Instances of the Entry class describes access events to instances of
  the namespace class."""

  accessor = TypedField(str)
  key = TypedField(str)
  value = TypedField(object)
  _iterContents = ListField(object)

  @staticmethod
  def _getFunctionTypes() -> list:
    """Getter-function for the types that represent a method"""

    def func() -> None:
      """Any function"""

    return [type(func), staticmethod, classmethod]

  @classmethod
  def _parseArgs(cls, *args, **kwargs) -> Self:
    """Parses the arguments to a key-value pair with the key of string
    type and the value of any type. """
    for (k, v) in kwargs.items():
      if isinstance(v, cls):
        return v

    for arg in args:
      if isinstance(arg, cls):
        return arg

    k, v = [*args, None, None][:2]
    if isinstance(k, str):
      return

  def __init__(self, *args, ) -> None:
    entry = [*[arg for arg in args if isinstance(arg, Entry)], None][0]
    if entry is not None:
      if isinstance(entry, Entry):
        self.accessor = entry.accessor
        self.key = entry.key
        self.value = entry.value
    elif len(args) > 2:
      self.accessor, self.key = args[:2]
      if isinstance(args[2], Exception):
        self.value = str(args[2])
      else:
        self.value = args[2]
    else:
      args = ', '.join([str(arg) for arg in args])
      raise ValueError("""Invalid entry: '(%s)'!""" % args)

  def isFunction(self, ) -> bool:
    """Flag indicating if the entry represents a function, a class method
    or a static method."""
    for type_ in self._getFunctionTypes():
      if isinstance(self.value, type_):
        return True
    return False

  def __repr__(self, ) -> str:
    """Code representation of the entry"""
    acc, key, val = self.accessor, self.key, self.value
    return 'Entry(%s, %s, %s)' % (acc, key, val)

  def __str__(self, ) -> str:
    """String representation of the entry"""
    acc, key, val = self.accessor, self.key, self.value
    return '.%s(%s, %s, %s)' % (acc, key, type(val), val)

  def __iter__(self, ) -> Self:
    """Implementation of iteration"""
    self._iterContents = [self.accessor, self.key, self.value]
    return self

  def __next__(self, ) -> object:
    """Implementation of iteration"""
    if self._iterContents:
      return self._iterContents.pop(0)
    raise StopIteration
