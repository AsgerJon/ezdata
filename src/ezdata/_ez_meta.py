"""EZMetaclass provides the metaclass from which the EZData class is
derived."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from icecream import ic
from vistutils.metas import AbstractMetaclass
from vistutils.metas import Bases as BS

from ezdata import EZNamespace as EZNS

ic.configureOutput(includeContext=True)


class EZMeta(AbstractMetaclass):
  """EZMetaclass provides the metaclass from which the EZData class is
  derived."""

  @classmethod
  def __prepare__(mcls, name: str, bases: BS, **kwargs) -> EZNS:
    """Reimplementation bringing the replacement of the namespace object
    class."""
    if kwargs.get('_root', None) is not None:
      setattr(EZNS, '__illegal_attribute_names__', [])
    return EZNS(name, bases, **kwargs)

  def __call__(cls, *args, **kwargs) -> Any:
    """Reimplementation that completely changes the instance creation
    process. """


class EZData(metaclass=EZMeta, _root=True):
  """EZData exposes the metaclass by allowing subclasses to be created. """

  def __init__(self, *args, **kwargs) -> None:
    """This init function prevents fallback to object.__init__ which takes
    exactly one argument, the instance being created. Further, it informs
    static type checkers that EZData and subclasses may be instantiated
    with positional and keyword arguments."""
    pass
