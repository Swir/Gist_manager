from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets

from .api import ApiError
from .config import APP_NAME
from .creator import Card


class ManagerPage(QtWidgets.QWidget):
    status_changed = QtCore.pyqtSignal(str)

    def __init__(self, get_api, parent=None):
        super().__init__(parent)
        self.get_api = get_api
        self._gists = []
        self._build_ui()
        QtCore.QTimer.singleShot(150, self.load_gists)

    def _build_ui(self):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        toolbar = Card()
        bar = QtWidgets.QHBoxLayout(toolbar)
        bar.setContentsMargins(14, 12, 14, 12)
        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setPlaceholderText("Search description, URL, file or ID…")
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.textChanged.connect(self.apply_filter)
        self.count_badge = QtWidgets.QLabel("0 Gists")
        self.count_badge.setObjectName("badge")

        self.refresh_button = QtWidgets.QPushButton("Refresh")
        self.refresh_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_BrowserReload))
        self.refresh_button.clicked.connect(self.load_gists)
        select_button = QtWidgets.QPushButton("Select all")
        select_button.clicked.connect(self.select_all)
        self.delete_button = QtWidgets.QPushButton("Delete selected")
        self.delete_button.setObjectName("danger")
        self.delete_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_TrashIcon))
        self.delete_button.clicked.connect(self.delete_selected)

        bar.addWidget(self.search_edit, 1)
        bar.addWidget(self.count_badge)
        bar.addWidget(self.refresh_button)
        bar.addWidget(select_button)
        bar.addWidget(self.delete_button)
        root.addWidget(toolbar)

        self.table = QtWidgets.QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["✓", "Description", "Files", "Updated", "Gist URL", "Raw URL", "ID"])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.table_context_menu)
        self.table.cellDoubleClicked.connect(self.open_current_gist)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setSortingEnabled(True)
        header = self.table.horizontalHeader()
        for col in (0, 2, 3, 6):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeToContents)
        for col in (1, 4, 5):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
        root.addWidget(self.table, 1)

    def load_gists(self):
        self.refresh_button.setEnabled(False)
        self.count_badge.setText("Loading…")
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        try:
            self._gists = self.get_api().list_gists()
            self.populate_table()
            self.status_changed.emit(f"Loaded {len(self._gists)} Gist(s)")
        except ApiError as exc:
            QtWidgets.QMessageBox.critical(self, APP_NAME, str(exc))
            self.count_badge.setText("Load failed")
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()
            self.refresh_button.setEnabled(True)

    def populate_table(self):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        for gist in self._gists:
            row = self.table.rowCount()
            self.table.insertRow(row)
            check = QtWidgets.QTableWidgetItem()
            check.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            check.setCheckState(QtCore.Qt.Unchecked)
            self.table.setItem(row, 0, check)

            files = gist.get("files", {})
            first_file = next(iter(files.values()), {})
            values = [
                gist.get("description") or "(No description)",
                str(len(files)),
                self._format_date(gist.get("updated_at", "")),
                gist.get("html_url", ""),
                first_file.get("raw_url", ""),
                gist.get("id", ""),
            ]
            for col, value in enumerate(values, 1):
                item = QtWidgets.QTableWidgetItem(value)
                item.setToolTip(value)
                self.table.setItem(row, col, item)
        self.table.setSortingEnabled(True)
        self.apply_filter(self.search_edit.text())

    @staticmethod
    def _format_date(value):
        if not value:
            return ""
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone().strftime("%Y-%m-%d %H:%M")
        except ValueError:
            return value

    def apply_filter(self, text):
        needle = text.strip().lower()
        visible = 0
        for row in range(self.table.rowCount()):
            haystack = " ".join(
                self.table.item(row, col).text()
                for col in range(1, self.table.columnCount())
                if self.table.item(row, col)
            ).lower()
            hidden = bool(needle) and needle not in haystack
            self.table.setRowHidden(row, hidden)
            visible += 0 if hidden else 1
        self.count_badge.setText(f"{visible}/{len(self._gists)} Gists" if needle else f"{len(self._gists)} Gists")

    def select_all(self):
        for row in range(self.table.rowCount()):
            if not self.table.isRowHidden(row):
                self.table.item(row, 0).setCheckState(QtCore.Qt.Checked)

    def selected_rows(self):
        return [
            row for row in range(self.table.rowCount())
            if self.table.item(row, 0) and self.table.item(row, 0).checkState() == QtCore.Qt.Checked
        ]

    def delete_selected(self):
        rows = self.selected_rows()
        if not rows:
            QtWidgets.QMessageBox.information(self, APP_NAME, "Select at least one Gist first.")
            return
        answer = QtWidgets.QMessageBox.question(
            self, APP_NAME, f"Delete {len(rows)} selected Gist(s)? This cannot be undone.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No,
        )
        if answer != QtWidgets.QMessageBox.Yes:
            return
        try:
            api = self.get_api()
        except ApiError as exc:
            QtWidgets.QMessageBox.warning(self, APP_NAME, str(exc))
            return

        progress = QtWidgets.QProgressDialog("Deleting Gists…", "Cancel", 0, len(rows), self)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setMinimumDuration(0)
        deleted, errors = 0, []
        for index, row in enumerate(rows, 1):
            if progress.wasCanceled():
                break
            gist_id = self.table.item(row, 6).text()
            try:
                api.delete_gist(gist_id)
                deleted += 1
            except ApiError as exc:
                errors.append(f"{gist_id}: {exc}")
            progress.setValue(index)
            QtWidgets.QApplication.processEvents()
        progress.close()
        self.status_changed.emit(f"Deleted {deleted} Gist(s)")
        self.load_gists()
        if errors:
            QtWidgets.QMessageBox.warning(self, APP_NAME, "Some deletions failed:\n\n" + "\n".join(errors[:10]))

    def table_context_menu(self, pos):
        row = self.table.rowAt(pos.y())
        if row < 0:
            return
        self.table.selectRow(row)
        menu = QtWidgets.QMenu(self)
        open_action = menu.addAction("Open Gist in browser")
        copy_gist = menu.addAction("Copy Gist URL")
        copy_raw = menu.addAction("Copy Raw URL")
        chosen = menu.exec_(self.table.viewport().mapToGlobal(pos))
        if chosen == open_action:
            self.open_current_gist()
        elif chosen == copy_gist:
            self.copy_column(4, "Gist URL copied")
        elif chosen == copy_raw:
            self.copy_column(5, "Raw URL copied")

    def copy_column(self, column, message):
        row = self.table.currentRow()
        item = self.table.item(row, column) if row >= 0 else None
        if item and item.text():
            QtWidgets.QApplication.clipboard().setText(item.text())
            self.status_changed.emit(message)

    def open_current_gist(self, *_):
        row = self.table.currentRow()
        item = self.table.item(row, 4) if row >= 0 else None
        if item and item.text():
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(item.text()))
