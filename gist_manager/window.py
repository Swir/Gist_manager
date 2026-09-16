import sys
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets

from .api import ApiError, GitHubGistApi, TokenStore
from .config import APP_NAME, APP_VERSION, GITHUB_PROFILE, THEMES
from .creator import CreatorPage
from .manager import ManagerPage
from .style import theme_css


def resource_path(relative_path):
    """Return a path that works from source and from a PyInstaller bundle."""
    bundle_root = getattr(sys, "_MEIPASS", None)
    if bundle_root:
        return Path(bundle_root) / relative_path
    return Path(__file__).resolve().parent.parent / relative_path


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = TokenStore.settings()
        self.current_theme = self.settings.value("theme", "Midnight Blue", type=str)
        if self.current_theme not in THEMES:
            self.current_theme = "Midnight Blue"
        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")
        self.setMinimumSize(900, 650)
        self.resize(1120, 780)
        self._apply_icon()
        self._build_menu()
        self._build_ui()
        self.set_theme(self.current_theme)
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

    def _apply_icon(self):
        icon = resource_path("assets/gist-manager.svg")
        if icon.exists():
            self.setWindowIcon(QtGui.QIcon(str(icon)))

    def _build_menu(self):
        settings_menu = self.menuBar().addMenu("Settings")
        settings_menu.addAction("Change GitHub token…", self.change_token)
        settings_menu.addAction("Forget saved token", self.reset_token)
        settings_menu.addSeparator()
        theme_menu = settings_menu.addMenu("Theme")
        self.theme_actions = {}
        group = QtWidgets.QActionGroup(self)
        group.setExclusive(True)
        for name in THEMES:
            action = QtWidgets.QAction(name, self, checkable=True)
            action.setChecked(name == self.current_theme)
            action.triggered.connect(lambda checked, n=name: self.set_theme(n))
            group.addAction(action)
            theme_menu.addAction(action)
            self.theme_actions[name] = action
        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction(
            "Open Swir on GitHub",
            lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl(GITHUB_PROFILE)),
        )

    def _build_ui(self):
        root_widget = QtWidgets.QWidget()
        root_widget.setObjectName("root")
        root = QtWidgets.QVBoxLayout(root_widget)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(14)

        hero = QtWidgets.QFrame()
        hero.setObjectName("hero")
        hero_row = QtWidgets.QHBoxLayout(hero)
        hero_row.setContentsMargins(22, 18, 22, 18)
        titles = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("Gist Manager")
        title.setObjectName("title")
        subtitle = QtWidgets.QLabel("Fast desktop workflow for GitHub Gists")
        subtitle.setObjectName("subtitle")
        titles.addWidget(title)
        titles.addWidget(subtitle)
        badge = QtWidgets.QLabel(f"v{APP_VERSION} • by Swir")
        badge.setObjectName("badge")
        hero_row.addLayout(titles)
        hero_row.addStretch(1)
        hero_row.addWidget(badge)
        root.addWidget(hero)

        self.tabs = QtWidgets.QTabWidget()
        self.creator = CreatorPage(self.get_api)
        self.manager = ManagerPage(self.get_api)
        self.creator.status_changed.connect(self.show_status)
        self.manager.status_changed.connect(self.show_status)
        self.tabs.addTab(self.creator, "Create")
        self.tabs.addTab(self.manager, "Manage")
        root.addWidget(self.tabs, 1)

        footer = QtWidgets.QLabel(
            "<a style='text-decoration:none' href='https://github.com/Swir'>by Swir — github.com/Swir</a>"
        )
        footer.setOpenExternalLinks(True)
        footer.setAlignment(QtCore.Qt.AlignRight)
        root.addWidget(footer)
        self.setCentralWidget(root_widget)
        self.statusBar().showMessage("Ready")

    def prompt_token(self):
        token, ok = QtWidgets.QInputDialog.getText(
            self, "GitHub token", "Enter a GitHub token with Gist access:", QtWidgets.QLineEdit.Password
        )
        if ok and token.strip():
            TokenStore.save(token.strip())
            self.show_status("GitHub token saved")
            return token.strip()
        raise ApiError("GitHub token is required for this action.")

    def get_api(self):
        token = TokenStore.token() or self.prompt_token()
        return GitHubGistApi(token)

    def change_token(self):
        try:
            self.prompt_token()
        except ApiError:
            pass

    def reset_token(self):
        TokenStore.clear()
        self.show_status("Saved GitHub token removed")
        QtWidgets.QMessageBox.information(
            self, APP_NAME,
            "The locally saved token was removed. You will be asked for a token next time GitHub access is needed.",
        )

    def set_theme(self, name):
        if name not in THEMES:
            return
        self.current_theme = name
        self.settings.setValue("theme", name)
        QtWidgets.QApplication.instance().setStyleSheet(theme_css(name))
        for theme_name, action in self.theme_actions.items():
            action.setChecked(theme_name == name)
        self.show_status(f"Theme: {name}")

    def show_status(self, message):
        self.statusBar().showMessage(message, 4500)

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        super().closeEvent(event)
