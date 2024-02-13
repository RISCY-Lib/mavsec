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
from typing import Callable

import contextlib
import pathlib

from PySide6.QtWidgets import (
    QMainWindow, QStatusBar, QMenuBar, QMenu, QTableWidget, QDockWidget, QWidget, QFormLayout,
    QTextEdit, QLineEdit, QTabWidget, QFileDialog, QComboBox, QToolBar, QTableWidgetItem
)
from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt

from mavsec import _info, properties
from mavsec.project import Project, ProjectInfo
from mavsec.properties import Property


FILE_FILTERS = [
    "Project (*.yaml *.yml *.toml *.json)",
    "YAML (*.yaml *.yml)",
    "TOML (*.toml)",
    "JSON (*.json)"
]


####################################################################################################
# Project Tab
####################################################################################################
class ProjectTab(QTableWidget):
    """The project information pane"""
    def __init__(
                    self,
                    parent: QWidget,
                    proj: Project | None = None,
                    pdock: PropertyDock | None = None
                ):
        super().__init__(parent)
        self.setObjectName(u"properties_table")

        self._pdock = pdock

        columns = ["Name", "Type", "Description"]
        self.setColumnCount(len(columns))
        self.setColumnWidth(0, 250)
        self.setColumnWidth(1, 250)
        self.setColumnWidth(2, 500)
        self.setHorizontalHeaderLabels(columns)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        if proj is None:
            self._proj = Project(ProjectInfo("", "", ""))
        else:
            self._proj = proj

    def activate(self) -> None:
        self.cellPressed.connect(self._cell_pressed)

    def _cell_pressed(self, row: int, col: int) -> None:
        if self._pdock is not None:
            self._pdock.activate(self._proj.properties, row, self.updateCurrentRow)

    def deactivate(self) -> None:
        with contextlib.suppress(RuntimeError):
            self.cellPressed.disconnect()

    def insertRow(self, row: int) -> None:
        self._proj.properties.insert(row, Property("", "", ptype=properties.SecureKeyProperty))
        super().insertRow(row)
        self.setRow(row)

    def setRow(self, row: int) -> None:
        self.setItem(row, 0, QTableWidgetItem(self._proj.properties[row].name))
        self.setItem(row, 1, QTableWidgetItem(self._proj.properties[row].type_name()))
        self.setItem(row, 2, QTableWidgetItem(self._proj.properties[row].description))

    def updateCurrentRow(self) -> None:
        row = self.currentRow()
        self.setRow(row)


####################################################################################################
# Property Information Pane
####################################################################################################
class PropertyDock(QDockWidget):
    """The property information pane"""
    def __init__(self, parent: QMainWindow):
        super().__init__("Property Info", parent=parent)
        self.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        parent.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self)

        form = QWidget(self)
        layout = QFormLayout(form)
        form.setLayout(layout)

        self._name = QLineEdit(form)
        self._type = QComboBox(form)
        self._description = QTextEdit(form)

        self._type.addItems([t.name for t in Property.available_types()])

        layout.addRow("Name", self._name)
        layout.addRow("Type", self._type)
        layout.addRow("Description", self._description)

        self.setDisabled(True)

        self.setWidget(form)

    def activate(self, props: list[Property], row: int, update: Callable) -> None:
        self._props = props
        self._prow = row
        prop = props[row]
        self._name.setText(prop.name)
        self._type.setCurrentText(prop.__class__.__name__)
        self._description.setText(prop.description)

        self._name.textChanged.connect(lambda text: setattr(prop, "name", text))
        self._name.textChanged.connect(update)
        self._type.currentTextChanged.connect(self.setType)
        self._type.currentTextChanged.connect(update)
        self._description.textChanged.connect(
            lambda: setattr(prop, "description", self._description.toPlainText())
        )
        self._description.textChanged.connect(update)

        self.setDisabled(False)

    def setType(self, text: str) -> None:
        ptype = properties.Property.ptype_from_str(text)
        self._props[self._prow].ptype = ptype

    def deactivate(self) -> None:
        with contextlib.suppress(RuntimeError):
            self._name.textChanged.disconnect()
            self._description.textChanged.disconnect()

        self._name.setText("")
        self._description.setText("")

        self.setDisabled(True)


####################################################################################################
# Project Information Pane
####################################################################################################
def _project_setter(proj: Project, proj_attr: str) -> Callable[[str], None]:
    def _setter(text: str) -> None:
        setattr(proj.info, proj_attr, text)
    return _setter


class ProjectInfoDock(QDockWidget):

    _proj_ptr: Project | None

    """The project information pane"""
    def __init__(self, parent: QMainWindow):
        super().__init__("Project Info", parent=parent)
        self.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        parent.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self)

        form = QWidget(self)
        layout = QFormLayout(form)
        form.setLayout(layout)

        self._name = QLineEdit(form)
        self._version = QLineEdit(form)
        self._description = QTextEdit(form)

        layout.addRow("Project Name", self._name)
        layout.addRow("Project Version", self._version)
        layout.addRow("Project Description", self._description)

        self.setDisabled(True)

        self._proj_ptr = None

        self.setWidget(form)

    def clear(self) -> None:
        self._proj_ptr = None

        self._name.setText("")
        self._version.setText("")
        self._description.setText("")

    def setProj(self, proj: Project) -> None:
        self._proj_ptr = proj
        self.setFromProj(proj)

        with contextlib.suppress(RuntimeError):
            self._name.textChanged.disconnect()
            self._version.textChanged.disconnect()
            self._description.textChanged.disconnect()

        self._name.textChanged.connect(_project_setter(self._proj_ptr, "name"))
        self._version.textChanged.connect(_project_setter(self._proj_ptr, "version"))
        self._description.textChanged.connect(
            lambda: setattr(self._proj_ptr, "description", self._description.toPlainText())
        )

    def setFromProj(self, proj: Project) -> None:
        self._name.setText(proj.info.name)
        self._version.setText(proj.info.version)
        self._description.setText(proj.info.description)


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


class MenuHelp(QMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(u"menuHelp")
        self.setTitle("Help")

        self.actionVersion = QtGui.QAction(parent)
        self.actionVersion.setObjectName(u"actionVersion")
        self.actionVersion.setText(f"Version: {_info.__version__}")
        self.addAction(self.actionVersion)

        # TODO Link to Documentation
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


################################################################################################
# Main Window
################################################################################################
class MavSecMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName(u"MavSecMainWindow")
        self.setWindowTitle("MavSec")

        self.resize(1920, 1080)

        self._statusBar = StatusBar(self)
        self.setStatusBar(self._statusBar)

        self._menuBar = MenuBar(self)
        self.setMenuBar(self._menuBar)
        self._setupMenuBar()

        self._create_tabs()
        self._setup_tabs()

        self._create_toolbar()
        self._setup_toolbar()

        self._project = ProjectInfoDock(self)

        self._properties = PropertyDock(self)

    # Menu Bar Actions
    ################################################################################################
    def _setupMenuBar(self) -> None:
        self._menuBar.file.actionNew.triggered.connect(self._new_project)
        self._menuBar.file.actionOpen.triggered.connect(self._open_project)
        self._menuBar.file.actionSave.triggered.connect(self._save_project)
        self._menuBar.file.actionExport.triggered.connect(self._export_project)
        self._menuBar.file.actionClose.triggered.connect(self._close_project)
        self._menuBar.file.actionQuit.triggered.connect(self._quit)

    def _new_project(self) -> None:
        tab_idx = self._tabs.addTab(ProjectTab(self._tabs, None, self._properties), "New Project")
        self._tabs.setCurrentIndex(tab_idx)

    def _open_project(self) -> None:
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            ".",
            ";;".join(FILE_FILTERS),
        )
        if not ok:
            return

        proj = Project.from_file(filename)
        proj.info.proj_file = filename

        proj_tab = ProjectTab(self._tabs, proj, self._properties)
        tab_idx = self._tabs.addTab(proj_tab, proj.info.name)
        self._tabs.setCurrentIndex(tab_idx)

    def _save_project(self) -> None:
        tab = self._tabs.currentWidget()
        if not isinstance(tab, ProjectTab):
            return

        if tab._proj.info.proj_file is None:
            self._save_as_project()
        else:
            tab._proj.to_file(tab._proj.info.proj_file)

        t_idx = self._tabs.currentIndex()
        self._tabs.setTabText(t_idx, tab._proj.info.name)

    def _save_as_project(self) -> None:
        pass

    def _save_all_projects(self) -> None:
        pass

    def _export_project(self) -> None:
        pass

    def _close_project(self) -> None:
        self._tabs.removeTab(self._tabs.currentIndex())

    def _quit(self) -> None:
        pass

    # Tab Actions
    ################################################################################################
    def _setup_tabs(self) -> None:
        self._prev_tab: None | ProjectTab = None
        self._tabs.currentChanged.connect(self._tab_changed)

    def _tab_changed(self, idx: int) -> None:
        if self._prev_tab is not None:
            self._prev_tab.deactivate()
            self._prev_tab = None

        tab = self._tabs.widget(idx)
        if not isinstance(tab, ProjectTab):
            self._project.clear()
            self._project.setDisabled(True)
            return

        tab.activate()
        self._project.setDisabled(False)
        self._project.setProj(tab._proj)

        self._prev_tab = tab

    def _setup_toolbar(self) -> None:
        self._new_property.triggered.connect(self._new_property_action)
        self._remove_property.triggered.connect(self._remove_property_action)

    def _new_property_action(self) -> None:
        tab = self._tabs.currentWidget()
        if not isinstance(tab, ProjectTab):
            return

        tab.insertRow(tab.rowCount())

    def _remove_property_action(self) -> None:
        tab = self._tabs.currentWidget()
        if not isinstance(tab, ProjectTab):
            return

        tab.removeRow(tab.currentRow())

    # GUI Creation
    ################################################################################################
    def _create_tabs(self) -> None:
        self._tabs = QTabWidget(self)
        self._tabs.setObjectName(u"tabs")
        self._tabs.setTabPosition(QTabWidget.TabPosition.South)
        self.setCentralWidget(self._tabs)

    def _create_toolbar(self) -> None:
        self._toolbar = QToolBar("Properties Toolbar", self)
        self.addToolBar(self._toolbar)
        self._toolbar.setIconSize(QtCore.QSize(16, 16))

        fpath = pathlib.Path(__file__).parent

        self._new_property = QtGui.QAction(
                                QtGui.QIcon(str(fpath.joinpath('assets', 'green-plus-hi.png'))),
                                "&New Property",
                                self
                             )
        self._new_property.setShortcut("Ctrl+Shift+N")
        self._toolbar.addAction(self._new_property)

        self._remove_property = QtGui.QAction(
                                QtGui.QIcon(str(fpath.joinpath('assets', 'red-minus-hi.png'))),
                                "&Remove Property",
                                self
                             )
        self._toolbar.addAction(self._remove_property)
