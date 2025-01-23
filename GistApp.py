import sys
import os
import time
import requests
from PyQt5 import QtWidgets, QtGui, QtCore

ORGANIZATION = "MyCompany"
APPLICATION = "GistApp"

# Definicje różnych motywów (styleSheet) jako słownik
THEMES = {
    "Dark": """
        QWidget {
            background-color: #2b2b2b;
            color: #f0f0f0;
            font-family: 'Consolas';
            font-size: 14px;
        }
        QLabel {
            background-color: transparent;
            font-weight: bold;
        }
        QGroupBox {
            background-color: transparent;
            border: 1px solid #555;
            border-radius: 4px;
            margin-top: 5px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 2px 5px;
            font-weight: bold;
            color: #f0f0f0;
            background-color: transparent;
        }
        QLineEdit, QTextEdit, QComboBox {
            background-color: #3c3f41;
            border: 1px solid #555;
            padding: 4px;
            color: #fff;
        }
        QPushButton {
            background-color: #007ACC;
            border: none;
            padding: 6px 14px;
            color: #fff;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #005F9E;
        }
        QCheckBox {
            background-color: transparent;
            padding: 4px;
        }
        QTableWidget {
            background-color: #3c3f41;
            gridline-color: #555;
        }
        QHeaderView::section {
            background-color: #3c3f41;
            color: #fff;
            padding: 4px;
            border: 1px solid #555;
        }
        QTabWidget::pane {
            border: 1px solid #555;
            background-color: #2b2b2b;
        }
        QTabBar::tab {
            background: #3c3f41;
            color: #f0f0f0;
            padding: 6px;
            border: 1px solid #555;
            border-bottom: none;
        }
        QTabBar::tab:selected {
            background: #2b2b2b;
        }
        QTabBar::tab:hover {
            background: #4c4c4c;
        }
    """,

    "Light": """
        QWidget {
            background-color: #f6f6f6;
            color: #000;
            font-family: 'Segoe UI';
            font-size: 14px;
        }
        QLabel {
            background-color: transparent;
            font-weight: bold;
            color: #333;
        }
        QGroupBox {
            background-color: #efefef;
            border: 1px solid #aaa;
            border-radius: 4px;
            margin-top: 5px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 2px 5px;
            font-weight: bold;
            color: #333;
            background-color: transparent;
        }
        QLineEdit, QTextEdit, QComboBox {
            background-color: #fff;
            border: 1px solid #ccc;
            padding: 4px;
            color: #000;
        }
        QPushButton {
            background-color: #007ACC;
            border: none;
            padding: 6px 14px;
            color: #fff;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #005F9E;
        }
        QCheckBox {
            background-color: transparent;
            padding: 4px;
        }
        QTableWidget {
            background-color: #fff;
            gridline-color: #ccc;
        }
        QHeaderView::section {
            background-color: #eee;
            color: #333;
            padding: 4px;
            border: 1px solid #ccc;
        }
        QTabWidget::pane {
            border: 1px solid #aaa;
            background-color: #f6f6f6;
        }
        QTabBar::tab {
            background: #eee;
            color: #333;
            padding: 6px;
            border: 1px solid #bbb;
            border-bottom: none;
        }
        QTabBar::tab:selected {
            background: #ddd;
        }
        QTabBar::tab:hover {
            background: #ddd;
        }
    """,

    "Ubuntu": """
        QWidget {
            background-color: #300A24;
            color: #f0f0f0;
            font-family: 'Ubuntu';
            font-size: 14px;
        }
        QLabel {
            background-color: transparent;
            font-weight: bold;
        }
        QGroupBox {
            background-color: transparent;
            border: 1px solid #9E0041;
            border-radius: 4px;
            margin-top: 5px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 2px 5px;
            font-weight: bold;
            color: #f0f0f0;
            background-color: transparent;
        }
        QLineEdit, QTextEdit, QComboBox {
            background-color: #4F1033;
            border: 1px solid #9E0041;
            padding: 4px;
            color: #fff;
        }
        QPushButton {
            background-color: #E95420;
            border: none;
            padding: 6px 14px;
            color: #fff;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #C44117;
        }
        QCheckBox {
            background-color: transparent;
            padding: 4px;
        }
        QTableWidget {
            background-color: #4F1033;
            gridline-color: #9E0041;
        }
        QHeaderView::section {
            background-color: #9E0041;
            color: #fff;
            padding: 4px;
            border: 1px solid #9E0041;
        }
        QTabWidget::pane {
            border: 1px solid #9E0041;
            background-color: #300A24;
        }
        QTabBar::tab {
            background: #4F1033;
            color: #f0f0f0;
            padding: 6px;
            border: 1px solid #9E0041;
            border-bottom: none;
        }
        QTabBar::tab:selected {
            background: #9E0041;
        }
        QTabBar::tab:hover {
            background: #C44117;
        }
    """,

    "SolarizedDark": """
        QWidget {
            background-color: #002b36;
            color: #839496;
            font-family: 'Consolas';
            font-size: 14px;
        }
        QLabel {
            background-color: transparent;
            font-weight: bold;
            color: #93a1a1;
        }
        QGroupBox {
            background-color: transparent;
            border: 1px solid #586e75;
            border-radius: 4px;
            margin-top: 5px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 2px 5px;
            font-weight: bold;
            color: #93a1a1;
            background-color: transparent;
        }
        QLineEdit, QTextEdit, QComboBox {
            background-color: #073642;
            border: 1px solid #586e75;
            padding: 4px;
            color: #eee8d5;
        }
        QPushButton {
            background-color: #268bd2;
            border: none;
            padding: 6px 14px;
            color: #eee8d5;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1978b5;
        }
        QCheckBox {
            background-color: transparent;
            padding: 4px;
            color: #839496;
        }
        QTableWidget {
            background-color: #073642;
            gridline-color: #586e75;
        }
        QHeaderView::section {
            background-color: #586e75;
            color: #eee8d5;
            padding: 4px;
            border: 1px solid #586e75;
        }
        QTabWidget::pane {
            border: 1px solid #586e75;
            background-color: #002b36;
        }
        QTabBar::tab {
            background: #073642;
            color: #839496;
            padding: 6px;
            border: 1px solid #586e75;
            border-bottom: none;
        }
        QTabBar::tab:selected {
            background: #586e75;
            color: #eee8d5;
        }
        QTabBar::tab:hover {
            background: #657b83;
        }
    """,

    "SolarizedLight": """
        QWidget {
            background-color: #fdf6e3;
            color: #657b83;
            font-family: 'Consolas';
            font-size: 14px;
        }
        QLabel {
            background-color: transparent;
            font-weight: bold;
            color: #586e75;
        }
        QGroupBox {
            background-color: transparent;
            border: 1px solid #93a1a1;
            border-radius: 4px;
            margin-top: 5px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 2px 5px;
            font-weight: bold;
            color: #586e75;
            background-color: transparent;
        }
        QLineEdit, QTextEdit, QComboBox {
            background-color: #eee8d5;
            border: 1px solid #93a1a1;
            padding: 4px;
            color: #657b83;
        }
        QPushButton {
            background-color: #268bd2;
            border: none;
            padding: 6px 14px;
            color: #fdf6e3;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1978b5;
        }
        QCheckBox {
            background-color: transparent;
            padding: 4px;
            color: #657b83;
        }
        QTableWidget {
            background-color: #eee8d5;
            gridline-color: #93a1a1;
        }
        QHeaderView::section {
            background-color: #93a1a1;
            color: #073642;
            padding: 4px;
            border: 1px solid #93a1a1;
        }
        QTabWidget::pane {
            border: 1px solid #93a1a1;
            background-color: #fdf6e3;
        }
        QTabBar::tab {
            background: #eee8d5;
            color: #657b83;
            padding: 6px;
            border: 1px solid #93a1a1;
            border-bottom: none;
        }
        QTabBar::tab:selected {
            background: #93a1a1;
            color: #073642;
        }
        QTabBar::tab:hover {
            background: #d9d2b7;
        }
    """
}

# -------------------------------
# Klasa do wyświetlania ruchomego tekstu
# -------------------------------
class MarqueeLabel(QtWidgets.QLabel):
    """
    Prosta etykieta z efektem przesuwającego się tekstu (marquee).
    """
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._original_text = text
        self._index = 0
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.scroll_text)
        self._timer.start(200)  # co 200 ms przesuwamy napis
        self.setAlignment(QtCore.Qt.AlignCenter)

    def scroll_text(self):
        if len(self._original_text) < 2:
            return
        self._index = (self._index + 1) % len(self._original_text)
        # "przewijanie" przez dodanie spacji i łączenie kawałków
        current = self._original_text[self._index:] + " " + self._original_text[:self._index]
        super().setText(current)

    def setText(self, text):
        self._original_text = text
        self._index = 0
        super().setText(text)


# ======================================
# Klasa GistCreator
# ======================================
class GistCreator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.headers = self.get_headers()
        self.init_ui()

    def get_headers(self):
        settings = QtCore.QSettings(ORGANIZATION, APPLICATION)
        token = settings.value("github_token", type=str)
        if not token:
            token = os.getenv("GITHUB_TOKEN")
        if not token:
            token_input, ok = QtWidgets.QInputDialog.getText(
                self, "Token GitHub", 
                "Wprowadź swój GitHub Token:",
                QtWidgets.QLineEdit.Normal
            )
            if ok and token_input:
                token = token_input.strip()
                settings.setValue("github_token", token)
            else:
                QtWidgets.QMessageBox.critical(self, "Błąd", "Nie ustawiono tokenu GitHub.")
                sys.exit(1)

        return {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def init_ui(self):
        self.setWindowTitle("Gist Manager")

        # Główny layout i podstawowe ustawienia marginesów
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 5)
        main_layout.setSpacing(12)

        # Baner tytułowy
        banner_label = QtWidgets.QLabel("Gist Creator")
        banner_label.setAlignment(QtCore.Qt.AlignCenter)
        banner_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            padding: 8px 0;
            margin: 0;
        """)
        main_layout.addWidget(banner_label)

        # Gist Options
        options_group = QtWidgets.QGroupBox("Gist Options")
        options_group_layout = QtWidgets.QFormLayout()
        options_group_layout.setContentsMargins(10, 10, 10, 10)
        options_group_layout.setSpacing(8)
        options_group.setLayout(options_group_layout)

        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.addItems(["Plik", "Folder"])
        self.type_combo.currentIndexChanged.connect(self.update_browse_button)

        self.path_edit = QtWidgets.QLineEdit()
        self.path_edit.setReadOnly(True)
        self.browse_button = QtWidgets.QPushButton("Wybierz plik")
        self.browse_button.clicked.connect(self.browse_path)

        path_layout = QtWidgets.QHBoxLayout()
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(self.browse_button)

        self.description_edit = QtWidgets.QLineEdit()
        self.public_checkbox = QtWidgets.QCheckBox()
        public_label = QtWidgets.QLabel("Publiczny")

        # Etykiety i pola w form layout
        options_group_layout.addRow("Typ:", self.type_combo)
        options_group_layout.addRow("Ścieżka:", path_layout)
        options_group_layout.addRow("Opis:", self.description_edit)
        options_group_layout.addRow(public_label, self.public_checkbox)

        # Link Options
        links_group = QtWidgets.QGroupBox("Links Options")
        links_layout = QtWidgets.QVBoxLayout()
        links_layout.setContentsMargins(10, 10, 10, 10)
        links_layout.setSpacing(5)
        links_group.setLayout(links_layout)

        self.show_html_checkbox = QtWidgets.QCheckBox("Pokaż normalne linki")
        self.show_html_checkbox.setChecked(False)
        self.show_raw_checkbox = QtWidgets.QCheckBox("Pokaż linki raw")
        self.show_raw_checkbox.setChecked(True)

        links_layout.addWidget(self.show_html_checkbox)
        links_layout.addWidget(self.show_raw_checkbox)

        # Układ poziomy dla Gist Options i Links Options
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(options_group)
        top_layout.addWidget(links_group)

        main_layout.addLayout(top_layout)

        # Results
        results_group = QtWidgets.QGroupBox("Results")
        results_layout = QtWidgets.QVBoxLayout()
        results_layout.setContentsMargins(10, 10, 10, 10)
        results_layout.setSpacing(5)
        results_group.setLayout(results_layout)

        self.output_area = QtWidgets.QTextEdit()
        self.output_area.setReadOnly(True)

        create_button_layout = QtWidgets.QHBoxLayout()
        self.create_button = QtWidgets.QPushButton("Utwórz Gista/Gisty")
        self.create_button.clicked.connect(self.create_gists)
        create_button_layout.addStretch()
        create_button_layout.addWidget(self.create_button)
        create_button_layout.addStretch()

        label_links = QtWidgets.QLabel("Linki do utworzonych gistów:")
        results_layout.addWidget(label_links)
        results_layout.addWidget(self.output_area)
        results_layout.addLayout(create_button_layout)

        main_layout.addWidget(results_group)

    def update_browse_button(self):
        if self.type_combo.currentText() == "Plik":
            self.browse_button.setText("Wybierz plik")
        else:
            self.browse_button.setText("Wybierz folder")
        self.path_edit.clear()

    def browse_path(self):
        if self.type_combo.currentText() == "Plik":
            file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, "Wybierz plik", "",
                "Wszystkie pliki (*);;Pliki Python (*.py)"
            )
            if file_name:
                self.path_edit.setText(file_name)
        else:
            directory = QtWidgets.QFileDialog.getExistingDirectory(
                self, "Wybierz folder",
                options=QtWidgets.QFileDialog.ShowDirsOnly
            )
            if directory:
                self.path_edit.setText(directory)

    def create_gists(self):
        path = self.path_edit.text()
        if not path or not os.path.exists(path):
            QtWidgets.QMessageBox.warning(self, "Błąd", "Wybierz poprawną ścieżkę.")
            return

        description = self.description_edit.text()
        public = self.public_checkbox.isChecked()
        show_html = self.show_html_checkbox.isChecked()
        show_raw = self.show_raw_checkbox.isChecked()

        self.output_area.clear()

        if os.path.isfile(path):
            self.create_single_gist(path, description, public, show_html, show_raw)
        elif os.path.isdir(path):
            self.create_gists_from_folder(path, description, public, show_html, show_raw)

    def create_single_gist(self, file_path, description, public, show_html, show_raw):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Błąd", f"Błąd podczas odczytu pliku: {e}")
            return

        filename = os.path.basename(file_path)
        payload = {
            "description": description,
            "public": public,
            "files": {
                filename: {
                    "content": content
                }
            }
        }

        response = requests.post("https://api.github.com/gists", headers=self.headers, json=payload)
        if response.status_code == 201:
            data = response.json()
            gist_url = data.get("html_url")
            raw_url = data.get("files", {}).get(filename, {}).get("raw_url")

            link_text = ""
            if show_html and gist_url:
                link_text += f"Gist: <a href='{gist_url}' style='color:#57A64A;'>{gist_url}</a><br>"
            if show_raw and raw_url:
                link_text += f"Raw: <a href='{raw_url}' style='color:#E06C75;'>{raw_url}</a><br>"

            self.output_area.append(link_text)
            self.output_area.append("")
        else:
            error_message = response.json().get('message', 'Nieznany błąd')
            QtWidgets.QMessageBox.critical(self, "Błąd", f"Nie udało się utworzyć gista: {error_message}")

    def create_gists_from_folder(self, folder_path, description, public, show_html, show_raw):
        all_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                all_files.append(os.path.join(root, file))

        total_files = len(all_files)
        if total_files == 0:
            QtWidgets.QMessageBox.information(self, "Informacja", "Nie znaleziono plików w wybranym folderze.")
            return

        progress = QtWidgets.QProgressDialog("Tworzenie gistów...", "Przerwij", 0, total_files, self)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)

        for i, file_path in enumerate(all_files, start=1):
            if progress.wasCanceled():
                break
            self.create_single_gist(file_path, description, public, show_html, show_raw)
            progress.setValue(i)
            QtWidgets.QApplication.processEvents()
            time.sleep(0.5)

        progress.close()


# ======================================
# Klasa GistManager
# ======================================
class GistManager(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.headers = self.get_headers()
        self.init_ui()
        self.load_gists()

    def get_headers(self):
        settings = QtCore.QSettings(ORGANIZATION, APPLICATION)
        token = settings.value("github_token", type=str)
        if not token:
            QtWidgets.QMessageBox.critical(self, "Błąd", "Token GitHub nie jest ustawiony.")
            sys.exit(1)
        return {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def init_ui(self):
        self.setWindowTitle("Gist Manager")
        # Zwiększamy nieco domyślny rozmiar
        self.setGeometry(150, 150, 900, 600)

        main_layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Zaznacz", "Opis", "URL", "Raw URL", "ID"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # Menu kontekstowe do kopiowania linków
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.table_context_menu)

        self.refresh_button = QtWidgets.QPushButton("Odśwież listę")
        self.refresh_button.clicked.connect(self.load_gists)
        self.delete_button = QtWidgets.QPushButton("Usuń zaznaczone")
        self.delete_button.clicked.connect(self.delete_selected)
        self.select_all_button = QtWidgets.QPushButton("Zaznacz wszystko")
        self.select_all_button.clicked.connect(self.select_all)

        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.select_all_button)

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

    def load_gists(self):
        response = requests.get("https://api.github.com/gists", headers=self.headers)
        if response.status_code != 200:
            QtWidgets.QMessageBox.critical(self, "Błąd", "Nie udało się pobrać listy gistów.")
            return

        gists = response.json()
        self.table.setRowCount(0)

        for gist in gists:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            checkbox = QtWidgets.QTableWidgetItem()
            checkbox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            checkbox.setCheckState(QtCore.Qt.Unchecked)
            self.table.setItem(row_position, 0, checkbox)

            description = gist.get("description") or "(Bez opisu)"
            self.table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(description))

            html_url = gist.get("html_url", "")
            self.table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(html_url))

            files = gist.get("files", {})
            raw_url = ""
            if files:
                first_file = next(iter(files.values()))
                raw_url = first_file.get("raw_url", "")
            self.table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(raw_url))

            gist_id = gist.get("id", "")
            self.table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(gist_id))

        self.table.resizeColumnsToContents()

    def select_all(self):
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item is not None:
                item.setCheckState(QtCore.Qt.Checked)

    def delete_selected(self):
        rows_to_delete = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.checkState() == QtCore.Qt.Checked:
                rows_to_delete.append(row)

        if not rows_to_delete:
            QtWidgets.QMessageBox.information(self, "Informacja", "Nie zaznaczono żadnych gistów do usunięcia.")
            return

        confirm = QtWidgets.QMessageBox.question(
            self, "Potwierdzenie",
            "Czy na pewno chcesz usunąć zaznaczone gisty?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if confirm != QtWidgets.QMessageBox.Yes:
            return

        progress = QtWidgets.QProgressDialog("Usuwanie gistów...", "Przerwij", 0, len(rows_to_delete), self)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)

        for count, row in enumerate(rows_to_delete, start=1):
            gist_id = self.table.item(row, 4).text()
            requests.delete(f"https://api.github.com/gists/{gist_id}", headers=self.headers)
            progress.setValue(count)
            QtWidgets.QApplication.processEvents()
            if progress.wasCanceled():
                break

        progress.close()
        self.load_gists()

    def table_context_menu(self, pos):
        menu = QtWidgets.QMenu(self)
        copy_gist_action = QtWidgets.QAction("Copy Gist URL", self)
        copy_raw_action = QtWidgets.QAction("Copy Raw URL", self)

        copy_gist_action.triggered.connect(self.copy_gist_url)
        copy_raw_action.triggered.connect(self.copy_raw_url)

        menu.addAction(copy_gist_action)
        menu.addAction(copy_raw_action)

        menu.exec_(self.table.mapToGlobal(pos))

    def copy_gist_url(self):
        row = self.table.currentRow()
        if row >= 0:
            url_item = self.table.item(row, 2)
            if url_item and url_item.text():
                QtWidgets.QApplication.clipboard().setText(url_item.text())
                QtWidgets.QMessageBox.information(self, "Skopiowano", "Skopiowano Gist URL do schowka.")
            else:
                QtWidgets.QMessageBox.information(self, "Brak linku", "Brak dostępnego Gist URL.")

    def copy_raw_url(self):
        row = self.table.currentRow()
        if row >= 0:
            raw_item = self.table.item(row, 3)
            if raw_item and raw_item.text():
                QtWidgets.QApplication.clipboard().setText(raw_item.text())
                QtWidgets.QMessageBox.information(self, "Skopiowano", "Skopiowano Raw URL do schowka.")
            else:
                QtWidgets.QMessageBox.information(self, "Brak linku", "Brak dostępnego Raw URL.")


# ======================================
# Główne okno - MainWindow z menu "Settings" + menu "Themes" + pasek stanu z "marquee"
# ======================================
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = QtCore.QSettings(ORGANIZATION, APPLICATION)
        # Odczyt zapisanej nazwy motywu lub "Dark" jeśli brak
        self.current_theme = self.settings.value("theme", "Dark")

        self.setWindowTitle("Gist Manager")
        self.setGeometry(50, 50, 900, 700)

        # Pasek stanu - zamiast showMessage, wstawiamy ruchomy napis
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        # MarqueeLabel
        self.marquee = MarqueeLabel("Gist manager by Swir")
        # Dodajemy go jako permanentny widget, dzięki czemu będzie widoczny stale
        self.statusBar.addPermanentWidget(self.marquee, 1)

        # Menu
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Settings")

        # Reset token
        reset_action = QtWidgets.QAction("Reset Token", self)
        reset_action.triggered.connect(self.reset_token)
        settings_menu.addAction(reset_action)

        # Menu Themes
        themes_menu = settings_menu.addMenu("Themes")
        # Dodajemy akcje dla każdego motywu
        for theme_name in THEMES.keys():
            theme_action = QtWidgets.QAction(theme_name, self)
            # Przy kliknięciu - ustawiamy motyw
            theme_action.triggered.connect(lambda checked, tn=theme_name: self.set_theme(tn))
            themes_menu.addAction(theme_action)

        self.tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_tab = GistCreator()
        self.manage_tab = GistManager()

        self.tabs.addTab(self.create_tab, "Creator")
        self.tabs.addTab(self.manage_tab, "Manager")

        # Ustawiamy (lub odświeżamy) motyw na aktualny
        self.set_theme(self.current_theme)

    def set_theme(self, theme_name):
        """Zmienia motyw całej aplikacji i zapisuje w QSettings."""
        if theme_name in THEMES:
            self.current_theme = theme_name
            self.settings.setValue("theme", theme_name)
            q_app = QtWidgets.QApplication.instance()
            q_app.setStyleSheet(THEMES[theme_name])

    def reset_token(self):
        # Usuwamy token z ustawień
        self.settings.remove("github_token")

        # Usuwamy stare zakładki
        self.tabs.removeTab(1)
        self.tabs.removeTab(0)

        # Tworzymy nowe instancje, żeby wymusić ponowne pytanie o token
        self.create_tab = GistCreator()
        self.manage_tab = GistManager()
        self.tabs.addTab(self.create_tab, "Creator")
        self.tabs.addTab(self.manage_tab, "Manager")

        QtWidgets.QMessageBox.information(
            self,
            "Reset Token",
            "Token został zresetowany. Wprowadź nowy token przy ponownym użyciu funkcji wymagających autoryzacji."
        )
        # Przywracamy motyw aktualny
        self.set_theme(self.current_theme)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
