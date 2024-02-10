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

from PySide6.QtWidgets import (
    QMainWindow, QStatusBar, QMenuBar, QMenu, QTableWidget, QDockWidget, QWidget, QFormLayout,
    QTextEdit, QLineEdit, QTabWidget, QFileDialog
)
from PySide6 import QtGui
from PySide6.QtCore import Qt

from mavsec import _info
from mavsec.project import Project, ProjectInfo


FILE_FILTERS = [
    "Project (*.yaml *.yml *.toml *.json)",
    "YAML (*.yaml *.yml)",
    "TOML (*.toml)",
    "JSON (*.json)"
]


class ProjectTab(QTableWidget):
    def __init__(self, parent: QWidget, proj: Project | None = None):
        super().__init__(parent)
        self.setObjectName(u"properties_table")

        columns = ["ID", "Name", "Type", "Description"]
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)

        if proj is None:
            self._proj = Project(ProjectInfo("", "", ""))
        else:
            self._proj = proj


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

        self._create_project_info_pane()
        self._setup_project_info()

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
        tab_idx = self._tabs.addTab(ProjectTab(self._tabs), "New Project")
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

        proj_tab = ProjectTab(self._tabs, proj)
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
        self._tabs.currentChanged.connect(self._tab_changed)

    def _tab_changed(self, idx: int) -> None:
        tab = self._tabs.widget(idx)
        if not isinstance(tab, ProjectTab):
            self._project_info_clear()
            self._project_info_read_only(True)
            return

        self._project_name.setText(tab._proj.info.name)
        self._project_version.setText(tab._proj.info.version)
        self._project_description.setText(tab._proj.info.description)
        self._project_info_read_only(False)

    # Project Info Actions
    ################################################################################################
    def _setup_project_info(self) -> None:
        self._project_name.textChanged.connect(self._project_name_changed)
        self._project_version.textChanged.connect(self._project_version_changed)
        self._project_description.textChanged.connect(self._project_description_changed)

    def _project_name_changed(self, text: str) -> None:
        tab = self._tabs.currentWidget()
        if not isinstance(tab, ProjectTab):
            return

        tab._proj.info.name = text

    def _project_version_changed(self, text: str) -> None:
        tab = self._tabs.currentWidget()
        if not isinstance(tab, ProjectTab):
            return

        tab._proj.info.version = text

    def _project_description_changed(self) -> None:
        tab = self._tabs.currentWidget()
        if not isinstance(tab, ProjectTab):
            return

        tab._proj.info.description = self._project_description.toPlainText()

    def _project_info_read_only(self, read_only: bool) -> None:
        self._project_name.setReadOnly(read_only)
        self._project_version.setReadOnly(read_only)
        self._project_description.setReadOnly(read_only)

    def _project_info_clear(self) -> None:
        self._project_name.setText("")
        self._project_version.setText("")
        self._project_description.setText("")

    # GUI Creation
    ################################################################################################
    def _create_tabs(self) -> None:
        self._tabs = QTabWidget(self)
        self._tabs.setObjectName(u"tabs")
        self.setCentralWidget(self._tabs)

    def _create_project_info_pane(self) -> None:
        self._left_dock = QDockWidget("Project Info", parent=self)
        self._left_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._left_dock)

        form = QWidget(self._left_dock)
        layout = QFormLayout(form)
        form.setLayout(layout)

        self._project_name = QLineEdit(form)
        self._project_version = QLineEdit(form)
        self._project_description = QTextEdit(form)
        self._project_info_read_only(True)

        layout.addRow("Project Name", self._project_name)
        layout.addRow("Project Version", self._project_version)
        layout.addRow("Project Description", self._project_description)

        self._left_dock.setWidget(form)
