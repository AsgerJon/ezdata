"""Old main tester script"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


def tester01() -> None:
  """Testing the EZMeta metaclass"""
  # obj = HelloWorld()
  # print(obj.a)
  # print(obj.b)
  # print(obj.c)
  # obj.a = 2
  # obj.b = '3'
  # obj.c = 4
  # print(obj.a)
  # print(obj.b)
  # print(obj.c)


def tester02() -> None:
  """Testing string.ascii stuff"""
  letters = string.ascii_letters
  digits = string.digits
  symbols = string.punctuation
  chars = [letters, digits, symbols]
  for set_ in chars:
    print(type(set_))


def tester03() -> None:
  """Testing worktoy"""
  for item in dir(worktoy):
    print(item)
  print(worktoy.__file__)


def tester04() -> None:
  """Testing str.strip"""
  base = '    lmao  '
  before = '|%s|' % base
  after = '|%s|' % base.strip()
  print(base)
  print(before)
  print(after)


def tester05() -> None:
  """Testing lorem"""

  test = lorem()
  print(test)
  print(monoSpace(test))


def tester06() -> None:
  """Testing HelloWorld class"""


class SpacePoint(EZData):
  """Representation of a point in space"""
  x: float
  y: float
  z: float

  @staticmethod
  def staticMethod() -> None:
    """LOL"""
    return None

  @classmethod
  def zero(cls) -> SpacePoint:
    """Returns the zero point"""
    return cls(0, 0, 0)

  @classmethod
  def unit(cls, value: float = None) -> SpacePoint:
    """Creates a unit valued point. Use the optional value argument to set
    a different value than 1. """
    value = 1 if value is None else value
    if value:
      return cls(value, value, value)
    return cls.zero()

  def __abs__(self) -> float:
    """Returns the distance from origin to self"""
    x, y, z = self.x, self.y, self.z
    return (x * x + y * y + z * z) ** 0.5

  def __mul__(self, other: SpacePoint) -> float:
    """Returns the dot product of self and other"""
    if isinstance(other, float):
      raise NotImplementedError
    x, y, z = self.x, self.y, self.z
    x2, y2, z2 = other.x, other.y, other.z
    return x * x2 + y * y2 + z * z2


def tester07() -> None:
  """Testing SpacePoint"""
  P = SpacePoint(3, 4, 5)
  Q = SpacePoint(4.5, 5.5, 6.)
  print(P)
  print(Q)
  R = SpacePoint()
  print(R)
