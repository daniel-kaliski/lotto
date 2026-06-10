# Analizator i Symulator Lotto 🎲

Zaawansowana aplikacja desktopowa napisana w języku Python, służąca do pobierania, analizy historycznych wyników losowań Lotto oraz przeprowadzania wielkich symulacji statystycznych. Aplikacja symuluje 14 milionów losowań (odpowiadających całkowitej liczbie możliwych kombinacji w polskim Lotto), korzystając z metody Monte Carlo, aby wygenerować rekomendowane zestawy liczb na podstawie faktycznych danych historycznych.

## ✨ Główne funkcje

* **Pobieranie danych na żywo:** Automatyczne pobieranie i parsowanie najnowszej bazy wyników Lotto w formacie CSV z zewnętrznego serwera.
* **Analiza historyczna:** Obliczanie częstotliwości występowania poszczególnych liczb na przestrzeni wszystkich dotychczasowych losowań (Top 10).
* **Symulacja Monte Carlo:** Błyskawiczna symulacja **14 000 000** losowań w celu zbadania rozkładu prawdopodobieństwa.
* **Generowanie rekomendacji:** Proponowanie gotowych zestawów liczb na podstawie różnych strategii statystycznych (m m.in. najczęstsze, hybrydowe z losowymi).
* **Asynchroniczny interfejs GUI:** Główna pętla obliczeniowa działa w osobnym wątku (`threading`), co zapobiega zawieszaniu się interfejsu (tzw. *UI freezing*) podczas pobierania danych i ciężkich operacji obliczeniowych.
* **Niestandardowy UI:** Nowoczesny, estetyczny wygląd z autorskim, zaokrąglonym przyciskiem opartym na komponencie `tk.Canvas` oraz animowanym paskiem postępu.

## 🛠️ Technologie i Wymagania

Projekt jest niezwykle lekki i **nie wymaga instalacji żadnych zewnętrznych bibliotek** (np. przez `pip`). Opiera się wyłącznie na standardowej bibliotece Pythona.

* **Język:** Python 3.8+
* **Interfejs graficzny:** `tkinter`, `ttk`
* **Współbieżność:** `threading`
* **Przetwarzanie danych:** `urllib`, `csv`, `collections.Counter`, `random`

## 🚀 Jak uruchomić?

1. Sklonuj repozytorium na swój dysk:
   ```bash
   git clone [https://github.com/daniel-kaliski/lotto.git](https://github.com/daniel-kaliski/lotto.git)
2. Przejdź do folderu z projektem i uruchom plik:
   ```bash
   python lotto.py

## 📸 Zrzuty ekranu
Ekran główny aplikacji:
<img width="762" height="694" alt="Zrzut ekranu 2026-06-10 o 21 32 33" src="https://github.com/user-attachments/assets/f8aec1df-f179-4667-b5bf-7edb770a2f0c" />

## 💡 Architektura kodu
Aplikacja wykorzystuje klasę `LottoGUI` do zarządzania interfejsem graficznym. Ze względu na ograniczenia standardowych przycisków w bibliotece `Tkinter` (brak właściwości `border-radius`), zaimplementowano własną klasę `RoundedButton` dziedziczącą po `tk.Canvas`. Pozwala to na tworzenie gładkich, wektorowych zaokrągleń rogów i zmianę kolorów (hover states) poprzez bindowanie zdarzeń myszy (`<Enter>`, `<Leave>`, `<ButtonPress-1>`). Bezpieczna komunikacja między wątkiem obliczeniowym a głównym wątkiem GUI odbywa się za pomocą metody `root.after()`.
