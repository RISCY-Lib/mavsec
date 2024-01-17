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

from setuptools import setup

import importlib.util
import pathlib
import sys

_proj_root = pathlib.Path(__file__).parent
_mavsec_spec = importlib.util.spec_from_file_location("mavsec", _proj_root.joinpath("src/mavsec/__init__.py"))
mavsec = importlib.util.module_from_spec(_mavsec_spec)
sys.modules["mavsec"] = mavsec
_mavsec_spec.loader.exec_module(mavsec)

if __name__ == "__main__":
  setup(
    version=mavsec.__version__
  )
