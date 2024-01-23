"""EZField provides the descriptors used by the EZData class"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Never


class EZField:
  """Descriptor"""

  def __init__(self, defaultValue: Any, valueType: type = None) -> None:
    self.__default_value__ = defaultValue
    valueType = type(defaultValue) if valueType is None else valueType
    if not isinstance(valueType, type):
      raise TypeError
    self.__value_type__ = valueType
    self.__field_name__ = None
    self.__field_owner__ = None

  def getFieldName(self) -> str:
    """Getter-function for the field name"""
    return self.__field_name__

  def setFieldName(self, name: str) -> None:
    """Setter-function for the field name"""
    self.__field_name__ = name

  def getPrivateName(self) -> str:
    """Getter-function for private name"""
    return '_%s' % self.__field_name__

  def getDefaultValue(self) -> Any:
    """Getter-function for default value"""
    return self.__default_value__

  def getValueType(self) -> type:
    """Getter-function for value type"""
    return self.__value_type__

  def __set_name__(self, owner: type, name: str) -> None:
    """Automatically invoked when owning class is created. """
    print(owner, name)
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: Any, owner: type) -> Any:
    """Getter-function"""
    pvtName = self.getPrivateName()
    if instance is None:
      return getattr(owner, pvtName, self.getDefaultValue())
    return getattr(instance, pvtName)

  def __set__(self, instance: Any, value: Any) -> None:
    """Setter-function"""
    pvtName = self.getPrivateName()
    if isinstance(value, self.getValueType()):
      return setattr(instance, pvtName, value)
    raise TypeError

  def __delete__(self, _) -> Never:
    """Illegal deleter function"""
    raise TypeError
