# Gist Manager
**Interaktywny program desktopowy / Interactive desktop application**  
🇵🇱 Umożliwia łatwe tworzenie i zarządzanie GitHub Gistami za pomocą prostego interfejsu graficznego.  
🇬🇧 Enables easy creation and management of GitHub Gists through a simple graphical interface.  

---

## Opis i Funkcje / Description and Features

🇵🇱 **Funkcje programu**:  
- Tworzenie nowych Gistów z plików lub folderów.  
- Zarządzanie istniejącymi Gistami: przeglądanie, kopiowanie linków, usuwanie.  
- Obsługa tokenów GitHuba – zapamiętywanie i możliwość resetowania.  
- Personalizacja wyglądu dzięki różnym motywom (Dark, Light, Ubuntu, Solarized).  

🇬🇧 **Features of the program**:  
- Create new Gists from files or folders.  
- Manage existing Gists: browse, copy links, delete.  
- Support for GitHub tokens – save and reset options.  
- Customize the appearance with various themes (Dark, Light, Ubuntu, Solarized).  

---

## Wymagania i Instalacja / Requirements and Installation

🇵🇱 **Wymagania**:  
- Python 3.8 lub nowszy.  
- Biblioteki:  
  ```bash
  pip install PyQt5 requests
  ```
- Token GitHuba z uprawnieniami `gist`.  

🇬🇧 **Requirements**:  
- Python 3.8 or newer.  
- Libraries:  
  ```bash
  pip install PyQt5 requests
  ```
- A GitHub Personal Access Token with `gist` permissions.  

🇵🇱 **Instalacja i uruchomienie**:  
1. Pobierz kod źródłowy i zapisz jako `GistApp.py`.  
2. Zainstaluj wymagane biblioteki za pomocą polecenia:  
   ```bash
   pip install PyQt5 requests
   ```
3. Uruchom program:  
   ```bash
   python GistApp.py
   ```  

🇬🇧 **Installation and launch**:  
1. Download the source code and save it as `GistApp.py`.  
2. Install the required libraries using the command:  
   ```bash
   pip install PyQt5 requests
   ```
3. Run the program:  
   ```bash
   python GistApp.py
   ```  

---

## Jak działa? / How does it work?

### Token GitHuba / GitHub Token  
🇵🇱 Przy pierwszym uruchomieniu program poprosi o Personal Access Token, który zostanie zapisany lokalnie. Token można zresetować w menu „Settings”.  
🇬🇧 On the first run, the program will ask for a Personal Access Token, which will be saved locally. The token can be reset via the "Settings" menu.  

### Tworzenie Gistów / Creating Gists  
🇵🇱 W zakładce „Creator” wybierz plik lub folder, podaj opis i wygeneruj linki do Gistów.  
🇬🇧 In the "Creator" tab, select a file or folder, provide a description, and generate Gist links.  

### Zarządzanie Gistami / Managing Gists  
🇵🇱 W zakładce „Manager” możesz przeglądać, kopiować linki i usuwać wybrane Gisty.  
🇬🇧 In the "Manager" tab, you can browse, copy links, and delete selected Gists.  

---

## Motywy / Themes  

🇵🇱 Dostępne motywy:  
🇬🇧 Available themes:  

- **Dark**  
- **Light**  
- **Ubuntu**  
- **SolarizedDark**  
- **SolarizedLight**  

---


