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
import abc
import enum


AnyRtlPath = str


@dataclass
class Project:
  name: str
  """The name of the project."""
  description: str
  """A brief description of the project."""
  version: str
  """The version of the project file"""
  signals: list[Signal] = field(default_factory=list)
  """The list of signals of interest in the project."""
  properties: list[Property] = field(default_factory=list)
  """The list of properties of interest in the project."""


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
class Property(abc.ABC):
  name: str
  """The name of the property."""
  description: str
  """A brief description of the property."""
  signal: Signal
  """The signal of interest in the property."""

  @abc.abstractmethod
  def to_svp(self) -> str:
    """Converts the property to an SVP principle."""
    pass

  @classmethod
  def from_dict(cls, d: str) -> Property:
    """Converts the SVP principle to a property."""
    raise NotImplementedError()


@dataclass
class KeyProperty(Property):
  """A property that ensures that a given key is stored correctly."""

  loc: Signal
  """The location of the key."""

  def to_svp(self) -> str:
    raise NotImplementedError()

  @classmethod
  def from_dict(cls, d: str) -> KeyProperty:
    raise NotImplementedError()


@dataclass
class KeyGenerationProperty(KeyProperty):
  """A property that ensures that a given generated key is stored correctly."""

  def to_svp(self) -> str:
    raise NotImplementedError()

  @classmethod
  def from_dict(cls, d: str) -> KeyGenerationProperty:
    raise NotImplementedError()


@dataclass
class SecureExternalMemoryProperty(Property):
  """A property that ensures that a given external memory is secure."""

  def to_svp(self) -> str:
    raise NotImplementedError()

  @classmethod
  def from_dict(cls, d: str) -> SecureExternalMemoryProperty:
    raise NotImplementedError()


@dataclass
class SecureInternalStorageProperty(Property):
  """A property that ensures that a given internal storage is secure."""

  def to_svp(self) -> str:
    raise NotImplementedError()

  @classmethod
  def from_dict(cls, d: str) -> SecureInternalStorageProperty:
    raise NotImplementedError()


@dataclass
class FaultTolerantFSMProperty(Property):
  """A property that ensures that a given FSM is fault tolerant."""

  state: Signal
  """The signal which is the state of the FSM"""
  inputs: list[Signal]
  """The list of signals which are the inputs of the FSM and should be tested for fault tolerance."""
  outputs: list[Signal]
  """The list of signals which are the outputs of the FSM and should be tested for fault tolerance."""

  def to_svp(self) -> str:
    raise NotImplementedError()

  @classmethod
  def from_dict(cls, d: str) -> FaultTolerantFSMProperty:
    raise NotImplementedError()
