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

from PySide6.QtWidgets import QStatusBar, QMenuBar, QMenu, QWidget
from PySide6 import QtGui

from mavsec import _info


####################################################################################################
# Main Windows Support Bars
####################################################################################################
class StatusBar(QStatusBar):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(u"statusBar")


class MenuFile(QMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(u"menuFile")
        self.setTitle("File")

        self.actionNew = QtGui.QAction(parent)
        self.actionNew.setObjectName(u"actionNew")
        self.actionNew.setText(u"New")
        self.actionNew.setShortcut("Ctrl+N")
        self.addAction(self.actionNew)

        self.actionOpen = QtGui.QAction(parent)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionOpen.setText(u"Open")
        self.actionOpen.setShortcut("Ctrl+O")
        self.addAction(self.actionOpen)

        self.actionSave = QtGui.QAction(parent)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave.setText(u"Save")
        self.actionSave.setShortcut("Ctrl+S")
        self.addAction(self.actionSave)

        self.actionSaveAs = QtGui.QAction(parent)
        self.actionSaveAs.setObjectName(u"actionSaveAs")
        self.actionSaveAs.setText(u"Save As")
        self.actionSaveAs.setShortcut("Ctrl+Shift+S")
        self.addAction(self.actionSaveAs)

        self.actionSaveAll = QtGui.QAction(parent)
        self.actionSaveAll.setObjectName(u"actionSaveAll")
        self.actionSaveAll.setText(u"Save All")
        self.actionSaveAll.setShortcut("Ctrl+Alt+S")
        self.addAction(self.actionSaveAll)

        self.addSeparator()

        self.actionExport = QtGui.QAction(parent)
        self.actionExport.setObjectName(u"actionExport")
        self.actionExport.setText(u"Export")
        self.actionExport.setShortcut("Ctrl+E")
        self.addAction(self.actionExport)

        self.addSeparator()

        self.actionClose = QtGui.QAction(parent)
        self.actionClose.setObjectName(u"actionClose")
        self.actionClose.setText(u"Close")
        self.actionClose.setShortcut("Ctrl+W")
        self.addAction(self.actionClose)

        self.actionQuit = QtGui.QAction(parent)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionQuit.setText(u"Quit")
        self.actionQuit.setShortcut("Alt+F4")
        self.addAction(self.actionQuit)


class MenuEdit(QMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(u"menuEdit")
        self.setTitle("Edit")

        self.actionCheckSecurity = QtGui.QAction(parent)
        self.actionCheckSecurity.setObjectName(u"actionCheckSecurity")
        self.actionCheckSecurity.setText(u"Check Security Handoff")
        self.addAction(self.actionCheckSecurity)

        self.actionCheckImplementation = QtGui.QAction(parent)
        self.actionCheckImplementation.setObjectName(u"actionCheckImplementation")
        self.actionCheckImplementation.setText(u"Check Design Handoff")
        self.addAction(self.actionCheckImplementation)


class MenuHelp(QMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(u"menuHelp")
        self.setTitle("Help")

        self.actionVersion = QtGui.QAction(parent)
        self.actionVersion.setObjectName(u"actionVersion")
        self.actionVersion.setText(f"Version: {_info.__version__}")
        self.actionVersion.setEnabled(False)
        self.addAction(self.actionVersion)

        self.actionDocumentation = QtGui.QAction(parent)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionDocumentation.setText(u"Documentation")
        self.addAction(self.actionDocumentation)


class MenuBar(QMenuBar):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(u"menuBar")
        self.setGeometry(0, 0, 800, 22)

        self.file = MenuFile(self)
        self.addAction(self.file.menuAction())

        self.edit = MenuEdit(self)
        self.addAction(self.edit.menuAction())

        self.help = MenuHelp(self)
        self.addAction(self.help.menuAction())
