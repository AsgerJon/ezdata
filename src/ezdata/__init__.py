"""This module provides an abstract baseclass for primitive dataclasses"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

#  Orphan imports
from ._ez_types import getGlobalTypes
from ._ez_types import getCommonDefaults, resolveType, createDefaultInstance

#  Dependant imports
from ._ez_field import EZField
from ._ez_namespace import EZNamespace
from ._ez_meta import EZMeta, EZData
