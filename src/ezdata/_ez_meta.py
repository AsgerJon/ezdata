"""EZMetaclass provides the metaclass from which the EZData class is
derived."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Callable, Any, Never
from warnings import warn

from icecream import ic
from vistutils import maybe
from vistutils.metas import AbstractMetaclass

from ezdata import EZNamespace as EZNS, EffortError, EZField
from vistutils.metas import Bases as BS
from utilities import TypedField, monoSpace

ic.configureOutput(includeContext=True)


class EZMeta(AbstractMetaclass):
  """EZMetaclass provides the metaclass from which the EZData class is
  derived."""

  @classmethod
  def _pvtNameFormat(mcls, name: str) -> str:
    """Private name format"""
    return '_%s' % name

  def initFactory(cls) -> Callable:
    """Factory creating __init__ methods for the given namespace"""

    def __init__(self, *args, **kwargs) -> None:
      args = [*args, ]
      for (key, field) in cls.__dict__.items():
        if isinstance(field, EZField):
          fieldName = key
          valType = field.getValueType()
          if valType is float:
            valType = (float, int)
          if valType is complex:
            valType = (complex, float, int)
          pvtName = field.getPrivateName()
          valKwarg = kwargs.get(fieldName, None)
          valArg = None if not args else args.pop(0)
          valDefault = field.getDefaultValue()
          val = maybe(valKwarg, valArg, valDefault)
          setattr(self, pvtName, val)

    return __init__

  @classmethod
  def __prepare__(mcls, name: str, bases: BS, **kwargs) -> EZNS:
    """Prepares the namespace object"""
    return EZNS(name, bases, **kwargs)

  def __new__(mcls, name: str, bases: BS, namespace: EZNS, **kwargs) -> type:
    """Creates the new class"""
    namespace.freeze()
    newSpace = namespace.compile()
    cls = AbstractMetaclass.__new__(mcls, name, bases, newSpace, **kwargs)
    setattr(cls, '__namespace_object__', namespace)
    return cls

  def __init__(cls, name: str, bases: BS, namespace: EZNS, **kwargs) -> None:
    """Ensures that the descriptor"""
    AbstractMetaclass.__init__(cls, name, bases, namespace, **kwargs)
    setattr(cls, '__init__', cls.initFactory())


class EZData(metaclass=EZMeta):
  """EZData exposes the metaclass by allowing subclasses to be created. """

  def __init__(self, *args, **kwargs) -> None:
    pass
