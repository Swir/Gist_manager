<div align="center">

# Gist Manager 2.0

### Modern desktop GitHub Gist Creator & Manager built with PyQt5

**Python • PyQt5 • GitHub API • Windows EXE • File/Folder Upload • Search • Themes**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-41CD52?logo=qt&logoColor=white)
![GitHub](https://img.shields.io/badge/API-GitHub-181717?logo=github&logoColor=white)
![Release](https://img.shields.io/badge/Release-v2.0.0-1f8fff)

</div>

---

## About

**Gist Manager** is a lightweight desktop application for creating and managing GitHub Gists without repeatedly switching to the browser. Version 2.0 refreshes the original utility with a cleaner Windows-friendly interface, faster navigation and safer GitHub API handling while preserving the simple file/folder workflow.

## Windows release

The recommended Windows build is the standalone **GistManager.exe** from the GitHub **v2.0.0 Release**. It is built on GitHub Actions with PyInstaller, receives the project icon, includes the required UI asset and must pass a packaged startup smoke test before publication.

The Release also provides a portable ZIP and `SHA256SUMS.txt` for integrity verification. No local Python installation is required to run the packaged EXE.

## What is new in 2.0

- redesigned card-based **Midnight Blue** interface
- cleaner **Create** and **Manage** workspaces
- drag-and-drop file/folder selection
- live Gist search by description, URL, file or ID
- improved sortable Gist table with file count and update time
- copy/open actions from the table context menu
- clearer progress/status feedback for create and delete operations
- three polished themes: **Midnight Blue**, **Graphite** and **Light**
- high-DPI support and remembered window size/position
- hidden token input and modern GitHub API headers
- request timeouts and clearer API/network error messages
- original Gist Manager application icon
- visible **by Swir** footer with GitHub link
- compatibility with the token/theme saved by the previous version
- verified one-file Windows EXE release pipeline

## Features

| Feature | Description |
|---|---|
| File → Gist | Create a Gist from a selected UTF-8 text file |
| Folder mode | Create one Gist per file from a selected folder tree |
| Drag & drop | Drop a file or folder directly onto the Create page |
| Gist browser | Load and inspect your Gists in a modern table |
| Search | Filter Gists instantly from the manager toolbar |
| Copy / open | Copy normal/raw URLs or open a Gist in the browser |
| Delete | Safely delete selected Gists with confirmation and progress |
| Token storage | Reuse the locally saved GitHub token between launches |
| Themes | Midnight Blue, Graphite and Light |
| Windows EXE | Portable one-file build published in GitHub Releases |

## Installation from source

```bash
git clone https://github.com/Swir/Gist_manager.git
cd Gist_manager
pip install -r requirements.txt
python GistApp.py
```

Or install dependencies manually:

```bash
pip install PyQt5 requests
```

## GitHub token

The app needs a GitHub token with permission to work with Gists. The token prompt uses password-style input and the value is stored locally through `QSettings` for reuse on the same machine.

Treat access tokens like passwords. Grant only the permissions you need and revoke a token immediately if it is exposed.

## UI notes

The default **Midnight Blue** theme is designed for a modern Windows 11 desktop while keeping the interface lightweight and native to PyQt5. Theme selection is available under `Settings → Theme`.

## Project structure

```text
Gist_manager/
├─ GistApp.py
├─ requirements.txt
├─ assets/
│  └─ gist-manager.svg
├─ gist_manager/
│  ├─ api.py
│  ├─ config.py
│  ├─ creator.py
│  ├─ manager.py
│  ├─ style.py
│  └─ window.py
├─ tools/
│  └─ build_icon.py
└─ README.md
```

## Discoverability

`github gist manager` • `gist gui python` • `github gist desktop app` • `python github api gui` • `gist creator python` • `manage github gists` • `pyqt5 github tool`

## Author

Developed by **Swir** — [@Swir](https://github.com/Swir)

<div align="center">

**Create • Search • Copy • Manage**

⭐ Star the repository if Gist Manager improves your workflow.

</div>
