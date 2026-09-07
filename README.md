<div align="center">

# 🗂️ Gist Manager

**Desktop GitHub Gist creator and manager with a graphical interface**  
**Desktopowy kreator i menedżer GitHub Gist z interfejsem graficznym**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-41CD52?logo=qt&logoColor=white)
![GitHub](https://img.shields.io/badge/API-GitHub-181717?logo=github)
![Author](https://img.shields.io/badge/Author-Swir-ff4fa3)

</div>

---

## 🇬🇧 English

Gist Manager is a Python desktop application that provides a convenient GUI for creating and managing GitHub Gists without working directly in the browser. It supports files and folders, Gist browsing, link copying, deletion and several visual themes.

### ✨ Features
- create Gists from files or folders
- browse existing Gists
- copy generated Gist links
- delete selected Gists
- GitHub token support with local persistence/reset
- multiple UI themes: Dark, Light, Ubuntu and Solarized variants
- PyQt5 desktop interface

### 🛠 Requirements
- Python 3.8+
- PyQt5
- requests
- GitHub token with appropriate Gist permissions

```bash
pip install PyQt5 requests
python GistApp.py
```

### 🔐 Token safety
Treat GitHub access tokens like passwords. Use only the permissions required by the application and never commit a token to a public repository.

---

## 🇵🇱 Polski

Gist Manager to desktopowa aplikacja w Pythonie zapewniająca wygodny interfejs do tworzenia i zarządzania GitHub Gist bez konieczności wykonywania wszystkich operacji ręcznie w przeglądarce. Program obsługuje pliki i foldery, przeglądanie Gistów, kopiowanie linków, usuwanie oraz kilka motywów graficznych.

### ✨ Funkcje
- tworzenie Gistów z plików lub folderów
- przeglądanie istniejących Gistów
- kopiowanie wygenerowanych linków
- usuwanie wybranych Gistów
- obsługa tokenu GitHub z możliwością resetowania
- motywy Dark, Light, Ubuntu oraz Solarized
- interfejs desktopowy PyQt5

### 🛠 Wymagania
- Python 3.8+
- PyQt5
- requests
- token GitHub z odpowiednimi uprawnieniami do Gist

```bash
pip install PyQt5 requests
python GistApp.py
```

### 🔐 Bezpieczeństwo tokenu
Token GitHub traktuj jak hasło. Nadawaj wyłącznie potrzebne uprawnienia i nigdy nie umieszczaj tokenu w publicznym repozytorium.

---

## 📁 Structure / Struktura
```text
Gist_manager/
├── GistApp.py
└── README.md
```

## 👤 Author / Autor
Developed by **Swir**.
