"""The 'empty' method returns 'None' if all positional arguments are
'None'. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


def empty(*args, ) -> bool:
  """Returns True the given arguments consists only of 'None'. """
  for arg in args:
    if arg is not None:
      return False
  return True
