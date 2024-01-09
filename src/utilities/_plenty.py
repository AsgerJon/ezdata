"""The 'plenty' function checks if all given positional arguments are
different from 'None'. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


def plenty(*args) -> bool:
  """True if all given positional arguments are different from 'None'."""
  for item in args:
    if item is None:
      return False
  return True
