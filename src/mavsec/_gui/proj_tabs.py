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
from typing import Callable, override

import contextlib

from PySide6.QtWidgets import (
    QMainWindow, QTableWidget, QDockWidget, QWidget, QFormLayout,
    QTextEdit, QLineEdit, QComboBox, QTableWidgetItem, QCheckBox
)
from PySide6.QtCore import Qt

from mavsec import properties
from mavsec.project import Project, ProjectInfo
from mavsec.properties import Property


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

        for i in range(len(self._proj.properties)):
            super().insertRow(i)
            self.set_row(i)

    def activate(self) -> None:
        self.cellPressed.connect(self._cell_pressed)

    def _cell_pressed(self, row: int, col: int) -> None:
        if self._pdock is not None:
            self._pdock.activate(self._proj.properties, row, self.update_current_row)

    def deactivate(self) -> None:
        with contextlib.suppress(RuntimeError):
            self.cellPressed.disconnect()

        if self._pdock is not None:
            self._pdock.deactivate()

    @override
    def insertRow(self, row: int) -> None:  # noqa: N802 this is a parent class method
        self._proj.properties.insert(row, Property("", "", ptype=properties.SecureKeyProperty))
        super().insertRow(row)
        self.set_row(row)

    def set_row(self, row: int) -> None:
        self.setItem(row, 0, QTableWidgetItem(self._proj.properties[row].name))
        self.setItem(row, 1, QTableWidgetItem(self._proj.properties[row].type_name()))
        self.setItem(row, 2, QTableWidgetItem(self._proj.properties[row].description))

    def update_current_row(self) -> None:
        row = self.currentRow()
        self.set_row(row)

    def get_proj(self) -> Project:
        return self._proj


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

        self._form = QWidget(self)
        self._layout = QFormLayout(self._form)
        self._form.setLayout(self._layout)

        self._name = QLineEdit(self._form)
        self._type = QComboBox(self._form)
        self._description = QTextEdit(self._form)
        self._preconditions = QTextEdit(self._form)

        self._type.addItems([t.name for t in Property.available_types()])

        self._layout.addRow("Name", self._name)
        self._layout.addRow("Type", self._type)
        self._layout.addRow("Description", self._description)
        self._layout.addRow("Preconditions", self._preconditions)

        self.setDisabled(True)

        self.setWidget(self._form)

    def activate(self, props: list[Property], row: int, update: Callable) -> None:
        self.deactivate()

        self._props = props
        self._prow = row
        self._update = update
        prop = props[row]
        self._name.setText(prop.name)
        self._type.setCurrentText(prop.type_name())
        self.set_type(prop.type_name())
        self._description.setText(prop.description)

        self._name.textChanged.connect(lambda text: setattr(prop, "name", text))
        self._name.textChanged.connect(update)
        self._type.currentTextChanged.connect(self.set_type)
        self._type.currentTextChanged.connect(update)
        self._description.textChanged.connect(
            lambda: setattr(prop, "description", self._description.toPlainText())
        )
        self._description.textChanged.connect(update)
        self._preconditions.textChanged.connect(
            lambda: setattr(prop, "preconditions", self._preconditions.toPlainText())
        )

        self.setDisabled(False)

    def set_type(self, text: str) -> None:
        ptype = properties.Property.ptype_from_str(text)
        self._props[self._prow].ptype = ptype

        self.remove_type_fields()
        self.add_type_fields()

    def deactivate(self) -> None:
        with contextlib.suppress(RuntimeError):
            self._name.textChanged.disconnect()
            self._description.textChanged.disconnect()

        self._name.setText("")
        self._description.setText("")

        self.remove_type_fields()

        self.setDisabled(True)

    def remove_type_fields(self) -> None:
        rows = self._layout.rowCount()
        for i in range(rows-1, 3, -1):
            self._layout.removeRow(i)

    def add_type_fields(self) -> None:
        prop = self._props[self._prow]

        if prop.ptype is None:
            return
        elif isinstance(prop.ptype, str):
            prop.ptype = properties.PropertyType.get_type(prop.ptype)

        for meta, mtype in prop.ptype.meta.items():
            if mtype is bool:
                cb = QCheckBox(self._form)
                if meta not in prop.meta:
                    prop.meta[meta] = False
                cb.setChecked(prop.meta[meta])
                self._layout.addRow(meta, cb)
                cb.stateChanged.connect(lambda state, m=meta: setattr(prop.meta, m, bool(state)))
            elif mtype is str:
                le = QLineEdit(self._form)
                if meta not in prop.meta:
                    prop.meta[meta] = ""
                le.setText(prop.meta[meta])
                le.textChanged.connect(lambda text, m=meta: setattr(prop.meta, m, text))
                le.textChanged.connect(self._update)
                self._layout.addRow(meta, le)
            elif mtype is int:
                le = QLineEdit(self._form)
                if meta not in prop.meta:
                    prop.meta[meta] = 0
                le.setText(str(prop.meta[meta]))
                le.textChanged.connect(lambda text, m=meta: setattr(prop.meta, m, int(text)))
                le.textChanged.connect(self._update)
                self._layout.addRow(meta, le)
            elif mtype is properties.AnyRtlPath:
                le = QLineEdit(self._form)
                if meta not in prop.meta:
                    prop.meta[meta] = ""
                le.setText(prop.meta[meta])
                le.textChanged.connect(lambda text, m=meta: setattr(prop.meta, m, text))
                le.textChanged.connect(self._update)
                le.setPlaceholderText("Path to signal in RTL")
                self._layout.addRow(meta, le)


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

    def set_proj(self, proj: Project) -> None:
        self._proj_ptr = proj
        self.set_from_proj(proj)

        with contextlib.suppress(RuntimeError):
            self._name.textChanged.disconnect()
            self._version.textChanged.disconnect()
            self._description.textChanged.disconnect()

        self._name.textChanged.connect(_project_setter(self._proj_ptr, "name"))
        self._version.textChanged.connect(_project_setter(self._proj_ptr, "version"))
        self._description.textChanged.connect(
            lambda: _project_setter(self._proj_ptr, "description")(self._description.toPlainText())
        )

    def set_from_proj(self, proj: Project) -> None:
        self._name.setText(proj.info.name)
        self._version.setText(proj.info.version)
        self._description.setText(proj.info.description)
