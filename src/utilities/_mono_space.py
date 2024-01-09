"""The monoSpace function replaces all whitespace in a string with one
space. The text can be given line breaks by including <br> in the string.
This default value may be set to any string as the second positional
argument or at keyword argument 'newLine'."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import string
from typing import TYPE_CHECKING

from utilities import maybe


def _isWhiteSpace(char: str) -> bool:
  """Examines if the given argument contains only whitespace."""
  if len(char) > 1:
    e = """Expected only single character strings, but received: %s!"""
    raise ValueError(e % char)
  charSets = [string.ascii_letters, string.digits, string.punctuation]
  for charSet in charSets:
    if char in charSet:
      return False
  return True


def monoSpace(text: str, *args, **kwargs) -> str:
  """The monoSpace function replaces all whitespace in a string with one
  space. """
  newLineDefault = '<br>'
  newLineKwarg = kwargs.get('newLine', None)
  newLineArg = [*[arg for arg in args if isinstance(arg, str)], None][0]
  newLine = maybe(newLineKwarg, newLineArg, newLineDefault)
  if TYPE_CHECKING:
    newLine = str(newLine)
  whiteSpaces = []
  for char in text:
    if _isWhiteSpace(char) and char not in whiteSpaces:
      whiteSpaces.append(char)
  for char in whiteSpaces:
    text = text.replace(char, ' ')
  _c = 0
  while '  ' in text and _c < len(text):
    text = text.replace('  ', ' ')
    _c += 1
    if _c > len(text):
      raise RecursionError
  if newLine not in text:
    return text
  lines = text.split(newLine)
  return '\n'.join([line.strip() for line in lines])
