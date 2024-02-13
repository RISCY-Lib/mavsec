#####################################################################################
# A tool for the creation of JasperGold SVP principle tcl files.
# Copyright (C) 2024  RISCY-Lib Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#####################################################################################

from __future__ import annotations
from typing import ClassVar

from dataclasses import dataclass, field
import enum


AnyRtlPath = str


class SignalType(enum.StrEnum):
  """The type of the signal of interest"""

  SYSTEM_INPUT = enum.auto()
  """A system input signal."""
  SYSTEM_OUTPUT = enum.auto()
  """A system output signal."""
  SYSTEM_CLOCK = enum.auto()
  """A system clock signal."""
  SYSTEM_RESET = enum.auto()
  """A system reset signal."""
  INTERNAL = enum.auto()
  """An internal signal."""


@dataclass
class Signal:
  name: str
  """The name of the signal."""
  description: str
  """A brief description of the signal."""
  location: AnyRtlPath
  """The RTL location of the signal. Using SystemVerilog syntax."""


@dataclass
class PropertyType():

  name: str
  """The name of the property type."""
  description: str
  """A brief description of the property type."""
  meta: list[str] = field(default_factory=list)
  """The information needed to generate the property."""


SecureKeyProperty = PropertyType(
  "SecureKey",
  "A property that ensures a given key is stored correctly.",
  ["key_loc", "key_size", "public_bus"]
)

SecureKeyGenProperty = PropertyType(
  "SecureKeyGen",
  "A property that ensures a given generated key is stored correctly.",
  ["public_key_loc", "key_size", "public_bus"]
)

SecureExternalMemoryProperty = PropertyType(
  "SecureExternalMemory",
  "A property that ensures a given external memory is secure."
)

SecureInternalStorageProperty = PropertyType(
  "SecureInternalStorage",
  "A property that ensures a given internal storage is not able to be accessed."
)

FaultTolerantFSMProperty = PropertyType(
  "FaultTolerantFSM",
  "A property that ensures a given FSM is fault tolerant."
)


@dataclass
class Property():
  name: str
  """The name of the property."""
  description: str
  """A brief description of the property."""
  meta: dict[str, str] = field(default_factory=dict)
  """A dictionary of metadata for the property."""
  ptype: PropertyType | str | None = None
  """The type of the property."""

  property_types: ClassVar[list[PropertyType]] = [
    SecureKeyProperty,
    SecureKeyGenProperty,
    SecureExternalMemoryProperty,
    SecureInternalStorageProperty,
    FaultTolerantFSMProperty
  ]
  """Available properties"""

  def __post_init__(self):
    if isinstance(self.ptype, str):
      for ptype in self.property_types:
        if ptype.name == self.ptype:
          self.ptype = ptype
          break
      else:
        raise ValueError(f"Property type {self.ptype} not found.")

  def type_name(self) -> str:
    """Gets the name of the property type."""
    if isinstance(self.ptype, PropertyType):
      return self.ptype.name
    return str(self.ptype)

  def to_svp(self) -> str:
    """Converts the property to an SVP principle."""
    raise NotImplementedError()

  @classmethod
  def ptype_from_str(cls, prop: str) -> PropertyType:
    """Gets a property type from a string."""
    for ptype in cls.property_types:
      if ptype.name == prop:
        return ptype
    raise ValueError(f"Property type {prop} not found.")

  @classmethod
  def from_dict(cls, d: str) -> Property:
    """Converts the SVP principle to a property."""
    raise NotImplementedError()

  @classmethod
  def available_types(cls) -> list[PropertyType]:
    """Returns all the available property types."""
    return cls.property_types

  @classmethod
  def add_type(cls, ptype: PropertyType) -> None:
    """Adds a property type to the available types."""
    cls.property_types.append(ptype)
