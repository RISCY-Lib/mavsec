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
from PySide6 import QtGui
from PySide6 import QtCore
from mavsec._gui.mavsec_ui import Ui_MainWindow

class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)
        self.setObjectName("MavSecCentralWidget")

        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 781, 541))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText(u"TextLabel")
        self.verticalLayout.addWidget(self.label)

        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setText(u"PushButton")
        self.verticalLayout.addWidget(self.pushButton)


class StatusBar(QtWidgets.QStatusBar):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)
        self.setObjectName(u"statusBar")


class MenuFile(QtWidgets.QMenu):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)
        self.setObjectName(u"menuFile")
        self.setTitle("File")

        self.actionNew = QtGui.QAction(parent)
        self.actionNew.setObjectName(u"actionNew")
        self.actionNew.setText(u"New")
        self.addAction(self.actionNew)
        self.actionLoad = QtGui.QAction(parent)
        self.actionLoad.setObjectName(u"actionLoad")
        self.actionNew.setText(u"Load")
        self.addAction(self.actionLoad)
        self.actionSave = QtGui.QAction(parent)
        self.actionSave.setObjectName(u"actionSave")
        self.actionNew.setText(u"Save")
        self.addAction(self.actionSave)
        self.addSeparator()

        self.actionExport = QtGui.QAction(parent)
        self.actionExport.setObjectName(u"actionExport")
        self.actionNew.setText(u"Export")
        self.addAction(self.actionExport)
        self.addSeparator()

        self.actionClose = QtGui.QAction(parent)
        self.actionClose.setObjectName(u"actionClose")
        self.actionNew.setText(u"Close")
        self.addAction(self.actionClose)
        self.actionQuite = QtGui.QAction(parent)
        self.actionQuite.setObjectName(u"actionQuite")
        self.actionNew.setText(u"Quite")
        self.addAction(self.actionQuite)


class MenuEdit(QtWidgets.QMenu):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)
        self.setObjectName(u"menuEdit")
        self.setTitle("Edit")


class MenuHelp(QtWidgets.QMenu):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)
        self.setObjectName(u"menuHelp")
        self.setTitle("Help")


class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)
        self.setObjectName(u"menuBar")
        self.setGeometry(0, 0, 800, 22)

        self.file = MenuFile(self)
        self.addAction(self.file.menuAction())

        self.edit = MenuEdit(self)
        self.addAction(self.edit.menuAction())

        self.help = MenuHelp(self)
        self.addAction(self.help.menuAction())


class MavSecMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName(u"MavSecMainWindow")
        self.setWindowTitle("MavSec")

        self.resize(1920, 1080)

        self._statusBar = StatusBar(self)
        self.setStatusBar(self._statusBar)

        self._menuBar = MenuBar(self)
        self.setMenuBar(self._menuBar)

        self._centralWidget = CentralWidget(self)
        self.setCentralWidget(self._centralWidget)
