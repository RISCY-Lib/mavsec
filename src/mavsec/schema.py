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
from typing import TypeVar, Type

import pathlib

import abc


SchemaT = TypeVar("SchemaT", bound="Schema")


class Schema(abc.ABC):
    @classmethod
    def from_dict(cls: Type[SchemaT], data: dict) -> SchemaT:
        """Get a cls object from a dictionary.

        Args:
            data (dict): The dictionary to convert to a cls object.

        Returns:
            cls: The Schema object.
        """
        return cls(**data)

    @abc.abstractmethod
    def to_dict(self) -> dict:
        """Convert the object to a dictionary.

        Returns:
            dict: The dictionary.
        """
        pass

    @classmethod
    def from_file(cls: Type[SchemaT], path: str | pathlib.Path) -> SchemaT:
        """Get a cls object from a file.

        Args:
            path (str): The path to the file.

        Returns:
            cls: The cls object.
        """
        if isinstance(path, str):
            path = pathlib.Path(path)

        if path.suffix in (".yaml", ".yml"):
            return cls.from_yaml(path)
        elif path.suffix == ".json":
            return cls.from_json(path)
        elif path.suffix == ".toml":
            return cls.from_toml(path)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")

    @classmethod
    def from_yaml(cls: Type[SchemaT], path: str | pathlib.Path) -> SchemaT:
        """Get a cls object from a YAML file.

        Args:
            path (str): The path to the YAML file.

        Returns:
            cls: The cls object.
        """
        import yaml

        with open(path, "r") as file:
            data = yaml.safe_load(file)

        return cls.from_dict(data)

    @classmethod
    def from_json(cls: Type[SchemaT], path: str | pathlib.Path) -> SchemaT:
        """Get a cls object from a JSON file.

        Args:
            path (str): The path to the JSON file.

        Returns:
            cls: The cls object.
        """
        import json

        with open(path, "r") as file:
            data = json.load(file)

        return cls.from_dict(data)

    @classmethod
    def from_toml(cls: Type[SchemaT], path: str | pathlib.Path) -> SchemaT:
        """Get a cls object from a TOML file.

        Args:
            path (str): The path to the TOML file.

        Returns:
            cls: The cls object.
        """
        import tomllib

        with open(path, "rb") as file:
            data = tomllib.load(file)

        return cls.from_dict(data)

    def to_yaml(self, path: str | pathlib.Path) -> None:
        """Write the object to a YAML file.

        Args:
            path (str): The path to the YAML file.
        """
        import yaml

        with open(path, "w") as file:
            yaml.dump(self.to_dict(), file)

    def to_json(self, path: str | pathlib.Path) -> None:
        """Write the object to a JSON file.

        Args:
            path (str): The path to the JSON file.
        """
        import json

        with open(path, "w") as file:
            json.dump(self.to_dict(), file)

    def to_toml(self, path: str | pathlib.Path) -> None:
        """Write the object to a TOML file.

        Args:
            path (str): The path to the TOML file.
        """
        import tomli_w

        with open(path, "wb") as file:
            tomli_w.dump(self.to_dict(), file)
