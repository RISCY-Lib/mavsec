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

from PySide6 import QtWidgets
import sys
from mavsec._gui import MavSecMainWindow

import re

#####################################################################################
# Version Information
#####################################################################################
from mavsec._info import __version__

version_info = [int(x) if x.isdigit() else x for x in re.split(r"\.|-", __version__)]


#####################################################################################
# GUI Entry Point
#####################################################################################
def gui():
    app = QtWidgets.QApplication(sys.argv)

    window = MavSecMainWindow()
    window.show()

    sys.exit(app.exec())
