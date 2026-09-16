import html
import os
from pathlib import Path

from PyQt5 import QtCore, QtWidgets

from .api import ApiError
from .config import APP_NAME


class Card(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")


class CreatorPage(QtWidgets.QWidget):
    status_changed = QtCore.pyqtSignal(str)

    def __init__(self, get_api, parent=None):
        super().__init__(parent)
        self.get_api = get_api
        self.setAcceptDrops(True)
        self._build_ui()

    def _build_ui(self):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        intro = Card()
        box = QtWidgets.QVBoxLayout(intro)
        box.setContentsMargins(18, 16, 18, 16)
        title = QtWidgets.QLabel("Create a new Gist")
        title.setObjectName("sectionTitle")
        subtitle = QtWidgets.QLabel(
            "Drop a file or folder here, or choose it manually. Folder mode creates one Gist per file."
        )
        subtitle.setObjectName("muted")
        subtitle.setWordWrap(True)
        box.addWidget(title)
        box.addWidget(subtitle)
        root.addWidget(intro)

        form_card = Card()
        form = QtWidgets.QGridLayout(form_card)
        form.setContentsMargins(18, 18, 18, 18)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(12)

        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.addItems(["File", "Folder"])
        self.type_combo.currentTextChanged.connect(self._type_changed)
        self.path_edit = QtWidgets.QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setPlaceholderText("Choose a file or folder…")
        self.browse_button = QtWidgets.QPushButton("Choose file")
        self.browse_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton))
        self.browse_button.clicked.connect(self.browse_path)

        path_wrap = QtWidgets.QWidget()
        path_row = QtWidgets.QHBoxLayout(path_wrap)
        path_row.setContentsMargins(0, 0, 0, 0)
        path_row.addWidget(self.path_edit, 1)
        path_row.addWidget(self.browse_button)

        self.description_edit = QtWidgets.QLineEdit()
        self.description_edit.setPlaceholderText("Optional description")
        self.public_checkbox = QtWidgets.QCheckBox("Public Gist")
        self.html_checkbox = QtWidgets.QCheckBox("Show normal URL")
        self.raw_checkbox = QtWidgets.QCheckBox("Show raw URL")
        self.raw_checkbox.setChecked(True)

        options = QtWidgets.QWidget()
        options_row = QtWidgets.QHBoxLayout(options)
        options_row.setContentsMargins(0, 0, 0, 0)
        options_row.setSpacing(18)
        for widget in (self.public_checkbox, self.html_checkbox, self.raw_checkbox):
            options_row.addWidget(widget)
        options_row.addStretch(1)

        for row, (label, widget) in enumerate(
            (("Source type", self.type_combo), ("Path", path_wrap), ("Description", self.description_edit), ("Options", options))
        ):
            caption = QtWidgets.QLabel(label)
            caption.setObjectName("caption")
            caption.setMinimumWidth(95)
            form.addWidget(caption, row, 0)
            form.addWidget(widget, row, 1)
        form.setColumnStretch(1, 1)
        root.addWidget(form_card)

        result_card = Card()
        result = QtWidgets.QVBoxLayout(result_card)
        result.setContentsMargins(18, 18, 18, 18)
        header = QtWidgets.QHBoxLayout()
        result_title = QtWidgets.QLabel("Output")
        result_title.setObjectName("sectionTitle")
        self.result_badge = QtWidgets.QLabel("Ready")
        self.result_badge.setObjectName("badge")
        header.addWidget(result_title)
        header.addStretch(1)
        header.addWidget(self.result_badge)
        result.addLayout(header)

        self.output_area = QtWidgets.QTextBrowser()
        self.output_area.setOpenExternalLinks(True)
        self.output_area.setPlaceholderText("Created Gist links will appear here.")
        self.output_area.setMinimumHeight(160)
        result.addWidget(self.output_area, 1)

        actions = QtWidgets.QHBoxLayout()
        clear_button = QtWidgets.QPushButton("Clear")
        clear_button.clicked.connect(self.output_area.clear)
        self.create_button = QtWidgets.QPushButton("Create Gist")
        self.create_button.setObjectName("primary")
        self.create_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogSaveButton))
        self.create_button.clicked.connect(self.create_gists)
        actions.addWidget(clear_button)
        actions.addStretch(1)
        actions.addWidget(self.create_button)
        result.addLayout(actions)
        root.addWidget(result_card, 1)

    def _type_changed(self, value):
        self.browse_button.setText("Choose folder" if value == "Folder" else "Choose file")
        self.path_edit.clear()

    def browse_path(self):
        if self.type_combo.currentText() == "File":
            path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose file", "", "All files (*)")
        else:
            path = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose folder")
        if path:
            self.path_edit.setText(path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and event.mimeData().urls()[0].toLocalFile():
            event.acceptProposedAction()

    def dropEvent(self, event):
        path = event.mimeData().urls()[0].toLocalFile()
        if path:
            self.type_combo.setCurrentText("Folder" if os.path.isdir(path) else "File")
            self.path_edit.setText(path)
            event.acceptProposedAction()

    def create_gists(self):
        path = Path(self.path_edit.text().strip())
        if not path.exists():
            QtWidgets.QMessageBox.warning(self, APP_NAME, "Choose an existing file or folder first.")
            return
        try:
            api = self.get_api()
        except ApiError as exc:
            QtWidgets.QMessageBox.warning(self, APP_NAME, str(exc))
            return

        files = [path] if path.is_file() else [p for p in path.rglob("*") if p.is_file()]
        if not files:
            QtWidgets.QMessageBox.information(self, APP_NAME, "No files were found in this folder.")
            return

        progress = QtWidgets.QProgressDialog("Creating Gists…", "Cancel", 0, len(files), self)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setMinimumDuration(0)
        self.create_button.setEnabled(False)
        self.result_badge.setText("Working")
        created, errors = 0, []

        for index, file_path in enumerate(files, 1):
            if progress.wasCanceled():
                break
            QtWidgets.QApplication.processEvents()
            try:
                data = api.create_gist(
                    file_path.name,
                    file_path.read_text(encoding="utf-8"),
                    self.description_edit.text().strip(),
                    self.public_checkbox.isChecked(),
                )
                self._append_result(file_path.name, data)
                created += 1
            except UnicodeDecodeError:
                errors.append(f"{file_path.name}: not a UTF-8 text file")
            except (OSError, ApiError) as exc:
                errors.append(f"{file_path.name}: {exc}")
            progress.setValue(index)

        progress.close()
        self.create_button.setEnabled(True)
        self.result_badge.setText(f"{created} created")
        self.status_changed.emit(f"Created {created} Gist(s)")
        if errors:
            QtWidgets.QMessageBox.warning(self, APP_NAME, "Some files failed:\n\n" + "\n".join(errors[:12]))

    def _append_result(self, filename, data):
        gist_url = data.get("html_url", "")
        raw_url = data.get("files", {}).get(filename, {}).get("raw_url", "")
        lines = [f"<b>{html.escape(filename)}</b>"]
        if self.html_checkbox.isChecked() and gist_url:
            lines.append(f"Gist: <a href='{gist_url}'>{gist_url}</a>")
        if self.raw_checkbox.isChecked() and raw_url:
            lines.append(f"Raw: <a href='{raw_url}'>{raw_url}</a>")
        if len(lines) == 1 and gist_url:
            lines.append(f"<a href='{gist_url}'>{gist_url}</a>")
        self.output_area.append("<br>".join(lines) + "<br>")
