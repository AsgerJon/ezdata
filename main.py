"""Main Tester Script - This file is for development only"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from icecream import ic

from tester_class_01 import Point

here = os.path.dirname(os.path.abspath(__file__))
there = os.path.join(here, 'src')
sys.path.append(there)

ic.configureOutput(includeContext=True)


def tester00() -> None:
  """Hello World!"""
  for item in [os, sys, 'hello world']:
    print(item)


def tester01() -> None:
  """LMAO"""


def tester02() -> None:
  """Testing globals"""
  X = Point(1, 2, 3)
  Y = Point(3, 4, 0)
  print(X, abs(X))
  print(Y, abs(Y))
  print(X @ Y)


if __name__ == '__main__':
  tester02()
