"""DictField is a subclass of ListField providing specialised accessor
methods suitable for a dictionary."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from utilities import ListField, monoSpace


class DictField(ListField):
  """DictField is a subclass of ListField providing specialised accessor
  methods suitable for a dictionary."""

  @staticmethod
  def _parseArgs(*args, **kwargs) -> dict:
    base = ListField._parseArgs(*args, **kwargs)
    base['type'] = dict
    base['default'] = {}
    return base

  def __init__(self, *args, **kwargs) -> None:
    self.__inner_type__ = self._parseArgs(*args, **kwargs).get('innerType')
    self.__default_value__ = []
    self.__value_type__ = list
    ListField.__init__(self, *args, readOnly=True, **kwargs)

  def __set__(self, instance: object, value: object) -> None:
    """The setter-function supports only instances of 'dict'. Entries of
    the given 'dict' are combined to the existing 'dict'. Please note that
    the class does not support default values. To reset the instance
    variable, use: 'del instance.data' which resets it.
    Setting equal to a dict instance updates the existing key, value pairs.
    For example:
      instance.data = dict(a=1, b=2)
      instance.data = dict(b=3, c=4)
      #  Will update the dictionary to {'a': 1, 'b': 3, 'c': 4}
      instance.data
      #  {'a': 1, 'b': 3, 'c': 4}"""
    existing = getattr(instance, self._getPrivateName(), {})
    if isinstance(value, dict):
      newValue = dict(existing, **value)
      setattr(instance, self._getPrivateName(), newValue)
    else:
      e = """DictField supports only instances of 'dict', but received 
      '%s' of type: '%s'!"""
      raise TypeError(monoSpace(e % (value, type(value))))
