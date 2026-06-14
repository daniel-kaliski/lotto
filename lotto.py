#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ==============================================================================
# Nazwa pliku: lotto.py
# 
# Copyright (c) 2026 Daniel Kaliski
# Ten kod jest objęty licencją GNU GENERAL PUBLIC LICENSE GPL-3.0.
# Pełny tekst licencji znajduje się w pliku LICENSE lub na stronie:
# https://opensource.org/license/gpl-3.0
# ==============================================================================

import random
import csv
import urllib.request
from collections import Counter
import tkinter as tk
from tkinter import ttk
import threading

URL = "https://www.wynikilotto.net.pl/download/lotto.csv"

class RoundedButton(tk.Canvas):
    """Niestandardowy przycisk z zaokrąglonymi rogami oparty na tk.Canvas"""
    def __init__(self, parent, text, command, radius=20, bg="#003366", fg="white", 
                 hover_bg="#004080", disabled_bg="#a0a0a0", font=("Segoe UI", 10, "bold"), *args, **kwargs):
        parent_bg = parent.cget("bg")
        super().__init__(parent, highlightthickness=0, bg=parent_bg, *args, **kwargs)
        
        self.command = command
        self.radius = radius
        self.bg_color = bg
        self.fg_color = fg
        self.hover_bg = hover_bg
        self.disabled_bg = disabled_bg
        self.text = text
        self.font = font
        self.is_disabled = False

        self.bind("<Configure>", self._draw)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _draw(self, event=None):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        if width < self.radius * 2 or height < self.radius * 2:
            return
            
        current_color = self.disabled_bg if self.is_disabled else self.bg_color
        self._create_rounded_rect(0, 0, width, height, self.radius, fill=current_color, tags="bg")
        self.create_text(width/2, height/2, text=self.text, fill=self.fg_color, font=self.font, tags="text")

    def _create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        """Rysuje zaokrąglony prostokąt"""
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, 
                  x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        return self.create_polygon(points, **kwargs, smooth=True)

    def _on_enter(self, event):
        if not self.is_disabled:
            self.itemconfig("bg", fill=self.hover_bg)
            self.config(cursor="hand2")

    def _on_leave(self, event):
        if not self.is_disabled:
            self.itemconfig("bg", fill=self.bg_color)
            self.config(cursor="")

    def _on_press(self, event):
        if not self.is_disabled:
            self.itemconfig("bg", fill=self.hover_bg) 

    def _on_release(self, event):
        if not self.is_disabled:
            self.itemconfig("bg", fill=self.hover_bg)
            if self.command:
                self.command()

    def set_state(self, state):
        """Zmienia stan przycisku (aktywny/zablokowany)"""
        if state == tk.DISABLED:
            self.is_disabled = True
            self.itemconfig("bg", fill=self.disabled_bg)
            self.config(cursor="X_cursor")
        else:
            self.is_disabled = False
            self.itemconfig("bg", fill=self.bg_color)
            self.config(cursor="hand2")


class LottoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizator i Symulator Lotto")
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        
        bg_color = "#f0f0f0"
        self.root.configure(bg=bg_color)

        main_frame = tk.Frame(root, padx=15, pady=15, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)

        btn_container = tk.Frame(main_frame, height=50, bg=bg_color)
        btn_container.pack(fill=tk.X, pady=(0, 15))
        btn_container.pack_propagate(False)

        self.start_btn = RoundedButton(
            btn_container, 
            text="Pobierz wyniki i uruchom symulację (14M)", 
            command=self.start_processing,
            radius=20,          
            bg="#003366",       
            hover_bg="#004080", 
            fg="white"
        )
        self.start_btn.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.9, anchor=tk.CENTER)

        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 15))

        self.text_area = tk.Text(
            main_frame, 
            wrap=tk.WORD, 
            state=tk.DISABLED, 
            font=("Consolas", 10),
            bg="#ffffff",
            relief=tk.FLAT,
            bd=1,
            highlightbackground="#cccccc",
            highlightcolor="#cccccc",
            highlightthickness=1
        )
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(main_frame, command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=scrollbar.set)

    def log(self, message):
        self.root.after(0, self._append_text, message)

    def _append_text(self, message):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def start_processing(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)

        self.start_btn.set_state(tk.DISABLED)
        self.progress.start(15)

        thread = threading.Thread(target=self.process_data, daemon=True)
        thread.start()

    def process_data(self):
        try:
            self.log("Pobieranie najnowszych wyników z sieci...")

            req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                lines = [line.decode('utf-8') for line in response.readlines()]

            nums = []
            reader = csv.reader(lines, delimiter=',')
            for row in reader:
                if len(row) >= 8:
                    try:
                        draw_nums = [int(x) for x in row[-6:]]
                        nums.extend(draw_nums)
                    except ValueError:
                        continue

            freq = Counter(nums)

            self.log("\n=== Najczęściej występujące liczby (Top 10) ===")
            for num, cnt in freq.most_common(10):
                self.log(f"Liczba {num:2d} – {cnt} wystąpień")

            N_SIM = 14_000_000
            self.log(f"\nTrwa symulacja {N_SIM:,} losowań, to potrwa kilka sekund...")
            counts = Counter()

            for _ in range(N_SIM):
                combo = tuple(sorted(random.sample(range(1, 50), 6)))
                counts[combo] += 1

            top6 = [num for num, _ in freq.most_common(6)]
            top5 = [num for num, _ in freq.most_common(5)]
            
            rand1 = random.sample([i for i in range(1, 50) if i not in top5], 1)
            combo2 = sorted(top5 + rand1)

            top3 = [num for num, _ in freq.most_common(3)]
            rand3_2 = random.sample([i for i in range(1, 50) if i not in top3], 3)
            combo3 = sorted(top3 + rand3_2)

            combo4 = sorted(random.sample(range(1, 50), 6))

            self.log("\n=== Zalecane zestawy (po 6 liczb) ===")
            self.log(f"1) Najczęstsze 6 liczb: {top6}")
            self.log(f"2) Top5 + 1 losowa:   {combo2}")
            self.log(f"3) Top3 + 3 losowe:   {combo3}")
            self.log(f"4) Całkowicie losowy: {combo4}")

            self.log("\n=== Najczęstsze kombinacje w symulacji (Top 5) ===")
            for combo, cnt in counts.most_common(5):
                self.log(f"{combo} – {cnt} wystąpień ({cnt/N_SIM*100:.6f}%)")
                
            self.log("\nZakończono pomyślnie.")

        except Exception as e:
            self.log(f"\nWystąpił błąd podczas działania programu:\n{e}")

        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.start_btn.set_state(tk.NORMAL))

if __name__ == "__main__":
    root = tk.Tk()
    app = LottoGUI(root)
    root.mainloop()