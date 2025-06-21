# Przepisownik

**Przepisownik** to desktopowa aplikacja napisana w Pythonie z użyciem PyQt5, umożliwiająca zarządzanie przepisami kulinarnymi, planowanie ich w kalendarzu oraz analizowanie statystyk gotowania.

---

## Funkcje

- Lista przepisów z filtrowaniem po tagach i składnikach
- Kalendarz z planowaniem dań na konkretne dni
- Statystyki gotowania (np. najczęściej gotowane przepisy)
- Wyszukiwanie przepisów
- Obsługa obrazów dla przepisów
- Trwałe przechowywanie danych w JSON (opcjonalnie SQLite)
- Estetyczny interfejs oparty o StyleSheet (QSS)
- Ikony i grafika z Figma

---

## 🚀 Uruchamianie

1. **Zainstaluj zależności**:

```bash
pip install -r requirements.txt
```

2. **Uruchom aplikację**:

```bash
python main.py
```

---

## Budowanie aplikacji

Możesz zbudować plik wykonywalny za pomocą [PyInstaller](https://www.pyinstaller.org/):

```bash
pyinstaller --onefile --windowed main.py
```

Plik `.exe` znajdziesz w folderze `dist/`.

---

## Struktura katalogów
```
projekt_przepisownik/
├── main.py
├── model/
│   ├── database.py
│   ├── singleton_class.py
│   └── ...
├── controller/
│   ├── recipe_controller.py
│   └── calendar_controller.py
├── view/
│   ├── main_window.py
│   ├── recipe_list_view.py
│   ├── calendar_list_view.py
│   └── ...
├── assets/
│   ├── icons/
│   ├── images/
│   └── style.qss
├── data/
│   └── recipes.json
└── README.md
```

---

## Style
Style aplikacji definiowane są w pliku `assets/style.qss`. Przykład:

---

## Dane
Domyślnie dane zapisywane są w `recipes.json`.

---

## Autorzy
- Filip Andrasz
- Dominik Gabiś

---

Języki skryptowe 2025