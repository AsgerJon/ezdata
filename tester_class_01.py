"""TestClass01 """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self, Any

from ezdata import EZData


class Point(EZData):
  x: float
  y: float
  z: float

  def __str__(self) -> str:
    """String Representation"""
    return '(%d, %d, %d)' % (self.x, self.y, self.z)

  def __repr__(self, ) -> str:
    """Code Representation"""
    return 'Point(%d, %d, %d)' % (self.x, self.y, self.z)

  def __abs__(self) -> float:
    """Length of vector """
    return (self * self) ** 0.5

  def __mul__(self, other: Any) -> Any:
    """Scalar multiplication"""
    if isinstance(other, (int, float)):
      return Point(*[other * arg for arg in [self.x, self.y, self.z]], )
    if isinstance(other, Point):
      return sum([self.x * other.x + self.y * other.y + self.z * other.z])

  def __rmul__(self, other: Any) -> Any:
    """Implementation of scalar * Self"""
    return self * other

  def __matmul__(self, other: Any) -> Point:
    """Cross multiplication"""
    x = self.y * other.z - self.z * other.y
    y = self.z * other.x - self.x * other.z
    z = self.x * other.y - self.y * other.x
    return Point(x, y, z)

  def __iter__(self, ) -> Self:
    """Iteration implementation"""
    setattr(self, '__iter_contents__', [self.x, self.y, self.z])
    return self

  def __next__(self, ) -> float:
    """Iteration implementation"""
    iterContents = getattr(self, '__iter_contents__')
    if iterContents:
      out = iterContents.pop(0)
      setattr(self, '__iter_contents__', iterContents)
      return out
    raise StopIteration
