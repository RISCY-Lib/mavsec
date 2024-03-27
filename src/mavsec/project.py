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

from dataclasses import dataclass, field

from mavsec.schema import Schema
from mavsec.properties import Property

import pathlib


@dataclass
class Project(Schema):
    """A project."""

    info: ProjectInfo
    """Information about the project."""
    properties: list[Property] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> Project:
        """Get a Project object from a dictionary.

        Args:
            data (dict): The dictionary to convert to a Project object.

        Returns:
            Project: The Project object.
        """
        return cls(
            info=ProjectInfo.from_dict(data["project"]),
            properties=[Property.from_dict(prop) for prop in data["properties"]],
        )

    def to_dict(self) -> dict:
        """Convert the object to a dictionary.

        Returns:
            dict: The dictionary.
        """
        return {
            "project": self.info.to_dict(),
            "properties": [prop.to_dict() for prop in self.properties],
        }

    def to_file(self, filename: str | pathlib.Path | None = None) -> None:
        """Write the object to a file."""
        if self.info.proj_file is None and filename is None:
            raise ValueError("Project file not set.")

        if filename is not None:
            self.info.proj_file = filename

        if self.info.proj_file is None:
            raise ValueError("Project file not set.")

        filepath = pathlib.Path(self.info.proj_file)

        if filepath.suffix in (".yaml", ".yml"):
            self.to_yaml(filepath)
        elif filepath.suffix == ".json":
            self.to_json(filepath)
        elif filepath.suffix == ".toml":
            self.to_toml(filepath)
        else:
            raise ValueError(f"Unsupported file type: {filepath.suffix}")

    def to_tcl(self, filename: str | pathlib.Path | None = None) -> None:
        """Write the object to a file."""
        raise NotImplementedError()


@dataclass
class ProjectInfo(Schema):
    """Information about the project."""

    name: str
    """Name of the project."""
    version: str
    """Version of the project."""
    description: str
    """Description of the project."""
    proj_file: str | pathlib.Path | None = None
    """Path to the project file."""

    def to_dict(self) -> dict:
        """Convert the object to a dictionary.
        proj_file is deliberately not included in the dictionary.

        Returns:
            dict: The dictionary.
        """
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
        }
