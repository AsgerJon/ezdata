"""EZMetaclass provides the metaclass from which the EZData class is
derived."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Callable, Any

from icecream import ic

from ezdata import EZNamespace
from utilities import TypedField

if TYPE_CHECKING:
  if sys.version_info >= (3, 8):
    Bases = list[type]
  else:
    from typing import List

    Bases = List[type]
else:
  Bases = tuple[type, ...]

ic.configureOutput(includeContext=True)


class EZMetaMeta(type):
  """Meta-metaclass used to create the EZMeta metaclass. This allows
  customization of __call__ to intercept the namespace between __prepare__
  and __new__. Further, it allows customization of __str__ and __repr__."""

  def __str__(cls) -> str:
    return cls.__qualname__


class EZMeta(type, metaclass=EZMetaMeta):
  """EZMetaclass provides the metaclass from which the EZData class is
  derived."""

  @staticmethod
  def _initSubFactory() -> Callable:
    """Why must this exist?"""

    def func(cls: object = None, *args, **kwargs) -> None:
      """Fine, I'll take those keyword arguments lmao!"""
      return type.__init_subclass__()

    return func

  def _initFactory(cls) -> Callable:
    """Factory method creating the __init__ method for the derived
    classes."""

    def __init__(self, *args, **kwargs) -> None:
      if not hasattr(cls, '__field_namespace__'):
        e = """No field namespace were found!"""
        raise ValueError(e)
      fields = getattr(cls, '__field_namespace__', )
      for (arg, (name, field)) in zip(args, fields.items()):
        field.__set__(self, arg)

    return __init__

  @staticmethod
  def _strFactory() -> Callable:
    """Factory method creating the __str__ method for the derived classes."""

    def __str__(self) -> str:
      cls = self.__class__
      fields = getattr(cls, '__field_namespace__', )
      clsName = cls.__name__
      lines = ['Instance of %s with fields:' % (clsName), ]
      for (key, val) in fields.items():
        lines.append('  %s: %s' % (val, val.__get__(self, cls)))
      return '\n'.join(lines)

    return __str__

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> EZNamespace:
    """Implementation of namespace preparation"""
    nameSpace = EZNamespace()
    nameSpace.className = name
    nameSpace.baseClasses = bases
    return nameSpace

  def __new__(mcls,
              name: str,
              bases: Bases,
              namespace: EZNamespace,
              **kwargs) -> type:
    """Implementation of class creation"""
    # print(50 * '_')
    # print('Entries for %s' % name)
    # print('Bases: %s' % str(namespace.baseClasses))
    # for entry in namespace.entryLog:
    #   print(entry)
    # print('END of entries for %s' % name)
    # print(50 * '¨')
    fields = namespace.getFields()
    fieldsNamespace = dict()
    for (key, val) in fields.items():
      defaultValue = val.get('defaultValue', None)
      valueType = val.get('fieldClassType', None)
      field = TypedField(defaultValue, valueType)
      fieldsNamespace[key] = field
    simpleNamespace = dict(__field_namespace__=fieldsNamespace, )
    simpleNamespace = {**simpleNamespace, **fieldsNamespace}
    simpleNamespace = {**simpleNamespace, **namespace.getFuncNamespace()}
    varDict = namespace.get('__annotations__', None)
    strFunc = mcls._strFactory()
    simpleNamespace = {**simpleNamespace, **{'__annotations__': varDict}}
    bases = namespace.baseClasses
    for base in bases:
      setattr(base, '__init_subclass__', mcls._initSubFactory())
    cls = type.__new__(mcls, name, (*bases,), simpleNamespace, **kwargs)
    initFunc = mcls._initFactory(cls)
    for (key, field) in fieldsNamespace.items():
      field.__set_name__(cls, key)
    setattr(cls, '__initial_name_space__', namespace)
    setattr(cls, '__str__', strFunc)
    setattr(cls, '__init__', initFunc)
    initSubclassFunc = mcls._initSubFactory()
    setattr(cls, '__init_subclass__', initSubclassFunc)
    return cls

  def __str__(cls) -> str:
    """Simplifies the name of the created class"""
    mcls = cls.__class__
    return '%s.%s' % (mcls.__qualname__, cls.__qualname__)

  def __repr__(cls) -> str:
    """Returns the name of the class itself"""
    return cls.__qualname__

  # def __call__(cls, *args, **kwargs) -> Any:
  #   print(cls.__qualname__)
  #   if len(args) == 1 and not kwargs:
  #     if isinstance(args[0], type):
  #       if cls.__qualname__ == 'EZData':
  #         ic(cls)
  #         ic(cls.__class__)
  #         raise Exception
  #         mcls = cls.__class__
  #         other = args[0]
  #         initSubclassFunc = mcls._initSubFactory()
  #         setattr(other, '__init_subclass__', initSubclassFunc)
  #         ic(other)
  #         name = other.__name__
  #         bases = []
  #         for base in other.__bases__:
  #           if base is not object:
  #             setattr(base, '__init_subclass__', initSubclassFunc)
  #             bases.append(base)
  #         return mcls(name, (*bases,), EZNamespace(), )
  #   return type.__call__(cls, *args, **kwargs)


class EZData(metaclass=EZMeta):
  """In-between class exposing the functionality from the metaclass"""
