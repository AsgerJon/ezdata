"""EZField provides the descriptors used by the EZData class"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Never

from vistutils import monoSpace
from vistutils.fields import AbstractField
from vistutils.waitaminute import typeMsg

from ezdata import createDefaultInstance, resolveType


class _QField:
  """QuickField is a class for creating fields with a single line of code."""

  def __init__(self, defVal: Any = None, *args, **kwargs) -> None:
    self.__field_name__ = None
    self.__field_owner__ = None
    self.__default_value__ = defVal

  def __set_name__(self, owner: type, name: str) -> None:
    self.__field_name__ = name
    self.__field_owner__ = owner

  def _getPrivateName(self) -> str:
    return '_%s' % self.__field_name__

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    pvtName = self._getPrivateName()
    if hasattr(instance, pvtName):
      return getattr(instance, pvtName)
    if kwargs.get('_recursion', False):
      raise RecursionError
    if self.__default_value__ is None:
      raise AttributeError(self.__field_name__)
    setattr(instance, pvtName, self.__default_value__)
    return self.__get__(instance, owner, _recursion=True, **kwargs)

  def __set__(self, instance: Any, value: Any) -> None:
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, value)

  def __delete__(self, instance: Any) -> None:
    return delattr(instance, self._getPrivateName())

  def __str__(self) -> str:
    """String representation"""
    return '[%s: %s]' % (self.__field_name__, self.__class__.__name__)


class EZParsed:
  """Class responsible for parsing arguments to default value and value
  type."""

  valType = _QField()
  defVal = _QField()

  @staticmethod
  def _parseTypeVal(valueType: type, defaultValue: Any) -> dict:
    """Parses the type and value"""
    if not isinstance(valueType, type):
      try:
        isinstance(valueType, defaultValue)
        return {'valueType': defaultValue, 'defaultValue': valueType}
      except TypeError as typeError:
        raise TypeError from typeError
    if isinstance(defaultValue, valueType):
      out = {'valueType': valueType, 'defaultValue': defaultValue}
      return out
    raise TypeError

  @classmethod
  def _parseVal(cls, valueType: Any) -> dict:
    """Parses the value"""
    if isinstance(valueType, type):
      defaultValue = createDefaultInstance(valueType)
      return {'valueType': valueType, 'defaultValue': defaultValue}
    return {'valueType': type(valueType), 'defaultValue': valueType}

  @classmethod
  def _parseStrings(cls, *args: str) -> dict:
    """Parses the strings"""
    strArgs = [str(arg) for arg in args]
    if not strArgs:
      e = """Received no arguments"""
      raise ValueError(e)
    if len(strArgs) == 1:
      try:
        type_ = resolveType(args[0])
        return cls._parseVal(type_)
      except NameError as nameError:
        return cls._parseTypeVal(str, args[0])
    if 'str' in strArgs:
      strArgs.remove('str')
      return cls._parseTypeVal(str, strArgs[0])
    type_ = None
    errors = []
    for arg in strArgs:
      try:
        type_ = resolveType(arg)
        break
      except NameError as nameError:
        errors.append(nameError)
    else:
      e = """Unable to resolve any of the names: '%s' as the name of a type
      defined in the global scope! If multiple names are given, at least 
      one must be the name of a type defined in the global scope! """
      raise NameError(monoSpace(e % strArgs))
    return cls._parseVal(type_)

  def __init__(self, *args, **kwargs) -> None:
    try:
      _parsed = self._parseTypeVal(*[*args, ][:2])
    except TypeError as typeError:
      try:
        _parsed = self._parseVal(args[0])
      except TypeError as typeError2:
        raise typeError2 from typeError
    self.valType = _parsed['valueType']
    self.defVal = _parsed['defaultValue']


class EZField(AbstractField):
  """Descriptor"""

  def __prepare_owner__(self, owner: type) -> type:
    """Prepares the owner"""
    return owner

  def __init__(self, *args, **kwarg) -> None:
    AbstractField.__init__(self, *args, **kwarg)

  def __set_name__(self, owner: type, name: str) -> None:
    """Automatically invoked when owning class is created. """
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """Getter-function"""
    pvtName = self.getPrivateName()
    if hasattr(instance, pvtName):
      return getattr(instance, pvtName)
    if kwargs.get('_recursion', False):
      raise RecursionError
    setattr(instance, pvtName, self.getDefaultValue())
    return self.__get__(instance, owner, _recursion=True, **kwargs)

  def __set__(self, instance: Any, value: Any) -> None:
    """Setter-function"""
    pvtName = self.getPrivateName()
    if isinstance(value, self.getValueType()):
      return setattr(instance, pvtName, value)
    e = typeMsg('value', value, self.getValueType())
    raise TypeError(e)

  def __delete__(self, _) -> Never:
    """Illegal deleter function"""
    e = """It is illegal to delete a field!"""
    raise TypeError(e)
