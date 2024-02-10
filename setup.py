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

_proj_root = pathlib.Path(__file__).parent
_info_spec = importlib.util.spec_from_file_location(
                                   "mavsec._info",
                                   _proj_root.joinpath("src", "mavsec", "_info.py")
                               )
_info = importlib.util.module_from_spec(_info_spec)
_info_spec.loader.exec_module(_info)

if __name__ == "__main__":
  setup(
    version=_info.__version__
  )