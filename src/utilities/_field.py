"""Field provides a simple descriptor class"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


class Field:
  """Field provides a simple descriptor class"""

  def __init__(self, defaultValue: object = None, **kwargs) -> None:
    self.__default_value__ = defaultValue
    
