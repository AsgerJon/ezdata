"""EZFieldSpace provides a namespace object with deferred creation of
EZFields."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any


class EZFieldSpace(dict):
  """Namespace object with deferred creation of EZFields"""

  def __getitem__(self, name: str) -> EZField:
    """Getter-function"""
    try:
      value = dict.__getitem__(self, name)
    except KeyError as keyError:
      raise keyError

  def __contains__(self, name: str) -> bool:
    """Membership test"""
    return name in self.__field_space__

  def __iter__(self):
    """Iterator"""
    return iter(self.__field_space__)

  def __len__(self) -> int:
    """Length"""
    return len(self.__field_space__)
