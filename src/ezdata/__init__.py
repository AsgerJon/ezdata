"""This module provides an abstract baseclass for primitive dataclasses"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

#  Orphan imports
from ._effort_error import EffortError
from ._entry import Entry
from ._ez_field import EZField

#  Dependant imports
from ._entry_log import EntryLog
from ._ez_namespace import EZNamespace
from ._ez_meta import EZMeta, EZData
