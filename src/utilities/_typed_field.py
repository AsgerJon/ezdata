"""TypedField is a strongly typed descriptor class."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen

from __future__ import annotations

from typing import Any
from warnings import warn

from utilities import monoSpace, maybe, empty, plenty


class TypedField:
  """TypedField is a strongly typed descriptor class."""

  @staticmethod
  def _cast(obj: object, *cls: type, **kwargs) -> bool:
    """This method returns the given object as a member the given type. If
    it is possible to new version of the object is returned. If it is not
    possible, the default behaviour is to raise a TypeError. This can be
    suppressed by setting the keyword argument 'fallback' to a value that
    will be returned instead of raising a TypeError.

    At least one type should be given as a positional argument, but more
    may be provided in which case the object will be attempted to be cast
    to each type given in the order received."""
    types = [arg for arg in cls if isinstance(arg, type)]
    if not types:
      e = """Found no type in the given positional arguments!"""
      raise TypeError(e)
    exceptions = []
    casted = None
    for type_ in types:
      try:
        casted = type_(obj)
        break
      except TypeError as typeError:
        exceptions.append(typeError)
    if casted is None:
      typeNames = [cls.__qualname__ for cls in types]
      errMsg = [str(e) for e in exceptions]
      msgList = ['%s: %s' % (c, e) for (c, e) in zip(typeNames, errMsg)]
      msg = '<br>'.join(msgList)
      e = """Attempted to cast object: '%s' to all given types, resulting 
      in: %s!""" % (obj, msg)
      raise TypeError(monoSpace(e))
    return casted

  @staticmethod
  def _parseArgs(*args, **kwargs) -> dict:
    typeKwarg = kwargs.get('type', None)
    defaultKwarg = kwargs.get('default', None)
    typeArg, defaultArg = None, None
    for arg in args:
      if isinstance(arg, type) and typeArg is None:
        typeArg = arg
      if not isinstance(arg, type) and defaultArg is None:
        defaultArg = arg
    defVal = maybe(defaultKwarg, defaultArg, )
    type_ = maybe(typeKwarg, typeArg)
    if type_ is None and defVal is None:
      return dict()
    if type_ is None:
      type_ = type(defVal)
    return dict(type=type_, default=defVal)

  def __init__(self, *args, **kwargs) -> None:
    self.__field_name__ = None
    self.__field_owner__ = None
    self.__value_type__ = None
    self.__default_value__ = None
    allowSet = kwargs.get('allowSet', None)
    readOnly = kwargs.get('readOnly', None)
    if empty(allowSet, readOnly):
      self.__read_only__ = False
    if plenty(allowSet, readOnly):
      if allowSet == readOnly:
        e = """Both 'allowSet' and 'readOnly' were given, and they were 
        given contradictory values!"""
        raise ValueError(monoSpace(e))
      w = """Both 'allowSet' and 'readOnly' were given. Since they 
      indicate the same intended functionality it is sufficient to provide 
      just one of them."""
      warn(monoSpace(w), )
    if allowSet is not None:
      self.__read_only__ = not allowSet
    if readOnly is not None:
      self.__read_only__ = readOnly
    parsedArgs = self._parseArgs(*args, **kwargs)
    if not parsedArgs:
      e = """Instances of TypedField must be instantiated with a type or a 
      default value! Received: '%s'!"""
      raise ValueError(monoSpace(e % parsedArgs))
    type_, defVal = parsedArgs.get('type'), parsedArgs.get('default')
    numTypes = [int, float, complex]
    if type_ in numTypes and type(defVal) in numTypes:
      self.__value_type__ = type_
      self.__default_value__ = type_(defVal)
    elif not isinstance(defVal, type_) and defVal is not None:
      e = """Incompatible default value and field type found! Expected 
      given default value: '%s' to be of type '%s', but received: '%s'!"""
      raise TypeError(monoSpace(e % (defVal, type_, type(defVal))))
    else:
      self.__value_type__ = type_
      self.__default_value__ = defVal

  def _getPrivateName(self, ) -> str:
    """Getter-function for the private name"""
    return '__%s_value__' % self.__field_name__

  def __set_name__(self, cls: type, name: str) -> None:
    """Invoked at class creation time"""
    self.__field_name__ = name
    self.__field_owner__ = cls

  def __get__(self, instance: object, cls: type) -> Any:
    """Getter-function implementation"""
    if instance is None:
      return self.__default_value__
    if hasattr(instance, self._getPrivateName()):
      return getattr(instance, self._getPrivateName())
    setattr(instance, self._getPrivateName(), self.__default_value__)
    return getattr(instance, self._getPrivateName())

  def __set__(self, instance: object, value: object) -> None:
    """Setter-function implementation"""
    if self.__read_only__:
      e = """The field '%s' is read-only!"""
      raise AttributeError(monoSpace(e % self.__field_name__))
    numTypes = [int, float, complex]
    if type(value) in numTypes and self.__value_type__ in numTypes:
      value = self.__value_type__(value)
    if not isinstance(value, self.__value_type__):
      e = """Incompatible value and field type found! Expected given
      value: '%s' to be of type '%s', but received: '%s'!"""
      expType = self.__value_type__
      actType = type(value)
      raise TypeError(monoSpace(e % (value, expType, actType)))
    else:
      setattr(instance, self._getPrivateName(), value)

  def __delete__(self, instance: object) -> None:
    """Deleter-function implementation"""
    if self.__read_only__:
      e = """The field '%s' is read-only!"""
      raise AttributeError(monoSpace(e % self.__field_name__))
    if hasattr(instance, self._getPrivateName()):
      delattr(instance, self._getPrivateName())

  def __str__(self) -> str:
    """String representation"""
    ownerName = None
    fieldName = self.__field_name__
    fieldOwner = self.__field_owner__.__qualname__
    valueType = self.__value_type__.__qualname__
    if not plenty(fieldName, fieldOwner):
      return 'TypedField instance %s %s' % (fieldName, fieldOwner)
    msg = """%s.%s: %s""" % (fieldOwner, fieldName, valueType)
    return monoSpace(msg)
