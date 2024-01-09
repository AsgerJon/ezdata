"""ListField is a subclass of TypedField providing specialised accessor
methods. These include support for setting equal to a tuple as well as
another list and a requirement for members of the list to be of a particular
type ('object' by default)."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import collections
from typing import TYPE_CHECKING

from utilities import maybe, TypedField


class ListField(TypedField):
  """ListField is a subclass of TypedField providing specialised accessor
  methods. These include support for setting equal to a tuple as well as
  another list and a requirement for members of the list to be of a
  particular type ('object' by default)."""

  @staticmethod
  def _parseArgs(*args, **kwargs) -> dict:
    out = TypedField._parseArgs(*args, **kwargs)
    typeKwarg = kwargs.get('innerType', object)
    typeArg = [*[arg for arg in args if isinstance(arg, type)], None][0]
    typeDefault = object
    type_ = maybe(typeKwarg, typeArg, typeDefault)
    if isinstance(type_, type):
      return dict(innerType=type_, type=list, default=[])
    raise TypeError

  def __init__(self, *args, **kwargs) -> None:
    self.__inner_type__ = self._parseArgs(*args, **kwargs).get('innerType')
    self.__default_value__ = []
    self.__value_type__ = list
    for arg in args:
      if arg is not self.__inner_type__:
        self.__default_value__.append(arg)
    TypedField.__init__(self, self.__default_value__, self.__value_type__, )

  def __set__(self, instance: object, value: object) -> None:
    """Please note that the setter-function will always replace existing
    content of the list. If the given value is iterable, then the inner
    list will have appended each item of the iterable. Otherwise,
    the inner list will be a single item list containing the given value."""
    newValue = None
    if isinstance(value, dict):
      value = [(k, v) for (k, v) in value.items()]
    if hasattr(value, '__iter__') or hasattr(value, '__getitem__'):
      if TYPE_CHECKING:
        if not isinstance(value, collections.Iterable):
          raise TypeError
      newValue = [i for i in value if isinstance(i, self.__inner_type__)]
    if newValue is None:
      newValue = [value, ]
    setattr(instance, self._getPrivateName(), newValue)
