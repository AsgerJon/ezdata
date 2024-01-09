"""The 'maybe' function is a 'None' aware filter that returns the first
object given as positional argument that is different from 'None'. This is
similar to the null coalescing operator in javascript, for example:

value = 0 ?? 1
The above example would return '0' as '0' although falsy is different from
'None'. The 'maybe' function provides the same functionality:

value = maybe(0, 1)  # value is set to '0' """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


def maybe(*args, ) -> object:
  """The 'maybe' function is a 'None' aware filter that returns the first
  object given as positional argument that is different from 'None'. This is
  similar to the null coalescing operator in javascript, for example:

  value = 0 ?? 1
  The above example would return '0' as '0' although falsy is different from
  'None'. The 'maybe' function provides the same functionality:

  value = maybe(0, 1)  # value is set to '0' """
  for item in args:
    if item is not None:
      return item
