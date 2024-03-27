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
import pathlib

from PySide6.QtWidgets import QMainWindow, QTabWidget, QFileDialog, QToolBar
from PySide6 import QtGui, QtCore

import webbrowser

from mavsec.project import Project

from mavsec._gui.proj_tabs import ProjectTab, PropertyDock, ProjectInfoDock
from mavsec._gui.menus import MenuBar, StatusBar

FILE_FILTERS = [
    "Project (*.yaml *.yml *.toml *.json)",
    "YAML (*.yaml *.yml)",
    "TOML (*.toml)",
    "JSON (*.json)"
]


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
        self._setup_menu_bar()

        self._create_tabs()
        self._setup_tabs()

        self._create_toolbar()
        self._setup_toolbar()

        self._project = ProjectInfoDock(self)

        self._properties = PropertyDock(self)

    # Menu Bar Actions
    ################################################################################################
    def _setup_menu_bar(self) -> None:
        self._menuBar.file.actionNew.triggered.connect(self._new_project)
        self._menuBar.file.actionOpen.triggered.connect(self._open_project)
        self._menuBar.file.actionSave.triggered.connect(self._save_project)
        self._menuBar.file.actionExport.triggered.connect(self._export_project)
        self._menuBar.file.actionClose.triggered.connect(self._close_project)
        self._menuBar.file.actionQuit.triggered.connect(self._quit)
        self._menuBar.help.actionDocumentation.triggered.connect(self._open_documentation)

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

        self.save_tab(tab)

        t_idx = self._tabs.currentIndex()
        self._tabs.setTabText(t_idx, tab._proj.info.name)

    def _save_as_project(self) -> None:
        tab = self._tabs.currentWidget()
        if not isinstance(tab, ProjectTab):
            return

        self.save_tab_as(tab)

    def _save_all_projects(self) -> None:
        for tab_idx in range(self._tabs.count()):
            tab = self._tabs.widget(tab_idx)
            if not isinstance(tab, ProjectTab):
                continue

            self.save_tab(tab)

    def _export_project(self) -> None:
        tab = self._tabs.currentWidget()
        if not isinstance(tab, ProjectTab):
            return

        filename, ok = QFileDialog.getSaveFileName(
            self,
            "Export Project",
            ".",
            "TCL (*.tcl)",
        )

        if not ok:
            return

        tab.get_proj().to_tcl(filename)

    def _close_project(self) -> None:
        self._tabs.removeTab(self._tabs.currentIndex())

    def _quit(self) -> None:
        self._save_all_projects()

        self.close()

    def _open_documentation(self) -> None:
        webbrowser.open("https://mavsec.readthedocs.io/en/latest/")

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
        self._project.set_proj(tab._proj)

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

    def _check_properties_action(self) -> None:
        raise NotImplementedError("Check Properties Action not implemented yet.")

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

        self._check_properties = QtGui.QAction(
                                   QtGui.QIcon(str(
                                       fpath.joinpath('assets', 'yellow-check-hi.png'))
                                   ),
                                   "&Check Properties",
                                   self
                                 )
        self._toolbar.addAction(self._check_properties)

    # Helper Functions
    ################################################################################################
    def save_tab(self, tab: ProjectTab) -> None:
        if tab.get_proj().info.proj_file is None:
            self.save_tab_as(tab)
        else:
            tab._proj.to_file(tab._proj.info.proj_file)

    def save_tab_as(self, tab: ProjectTab) -> None:
        filename, ok = QFileDialog.getSaveFileName(
            self,
            "Save Project As",
            ".",
            ";;".join(FILE_FILTERS),
        )

        if not ok:
            return

        tab._proj.info.proj_file = filename
        tab.get_proj().to_file(filename)
