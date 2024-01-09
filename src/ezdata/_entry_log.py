"""EntryLog provides an iterable class representation of the entries made
to an instance of the EZNamespace class."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezdata import Entry


class EntryLog:
  """EntryLog provides an iterable class representation of the entries made
  to an instance of the EZNamespace class."""

  def __init__(self) -> None:
    self.__entry_list__ = []
    self.__iter_contents__ = None

  def __iter__(self) -> EntryLog:
    self.__iter_contents__ = [entry for entry in self.__entry_list__]
    return self

  def __next__(self) -> object:
    if not self.__iter_contents__:
      raise StopIteration
    return self.__iter_contents__.pop(0)

  def append(self, *args, **kwargs) -> Entry:
    """Appends an entry to the inner contents list"""
    entry = Entry(*args, **kwargs)
    self.__entry_list__.append(entry)
    return entry
