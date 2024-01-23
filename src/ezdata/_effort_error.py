"""EffortError is like, you know..."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


class EffortError(Exception):
  """Indicates that implementing the attempted functionality would require
  more effort to implement than the utility would justify."""

  def __init__(self, msg: str = None, *args, **kwargs) -> None:
    if isinstance(msg, str):
      Exception.__init__(self, msg)
    else:
      Exception.__init__(self)
