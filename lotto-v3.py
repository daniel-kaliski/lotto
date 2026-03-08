import random
import csv
import urllib.request
from collections import Counter

# URL do bazy wyników Lotto
URL = "https://www.wynikilotto.net.pl/download/lotto.csv"

print("Pobieranie najnowszych wyników z sieci...")

# Pobieranie i dekodowanie danych
req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    lines = [line.decode('utf-8') for line in response.readlines()]

nums = []

# Parsowanie pliku CSV
reader = csv.reader(lines, delimiter=',')
for row in reader:
    # Plik ma format: Nr_losowania, Data, L1, L2, L3, L4, L5, L6
    if len(row) >= 8:
        try:
            # Pobieramy 6 ostatnich elementów z każdego wiersza i zamieniamy na int
            draw_nums = [int(x) for x in row[-6:]]
            nums.extend(draw_nums)
        except ValueError:
            # Pomijamy wiersze nagłówkowe (gdzie nie da się zrzutować na int)
            continue

freq = Counter(nums)

print("\n=== Najczęściej występujące liczby (Top 10) ===")
for num, cnt in freq.most_common(10):
    print(f"Liczba {num:2d} – {cnt} wystąpień")

# Symulacja 14 milionów losowań
N_SIM = 14_000_000
print(f"\nTrwa symulacja {N_SIM:,} losowań, to potrwa kilka sekund...")
counts = Counter()

for _ in range(N_SIM):
    combo = tuple(sorted(random.sample(range(1, 50), 6)))  # 6 liczb z 1..49
    counts[combo] += 1

top6 = [num for num, _ in freq.most_common(6)]

top5 = [num for num, _ in freq.most_common(5)]
# Poprawka: losujemy 1 liczbę (zamiast 3), aby zestaw miał 6 liczb
rand1 = random.sample([i for i in range(1, 50) if i not in top5], 1)
combo2 = sorted(top5 + rand1)

top3 = [num for num, _ in freq.most_common(3)]
rand3_2 = random.sample([i for i in range(1, 50) if i not in top3], 3)
combo3 = sorted(top3 + rand3_2)

combo4 = sorted(random.sample(range(1, 50), 6))

print("\n=== Zalecane zestawy (po 6 liczb) ===")
print(f"1) Najczęstsze 6 liczb: {top6}")
print(f"2) Top5 + 1 losowa:   {combo2}")
print(f"3) Top3 + 3 losowe:   {combo3}")
print(f"4) Całkowicie losowy: {combo4}")

print("\n=== Najczęstsze kombinacje w symulacji (Top 5) ===")
for combo, cnt in counts.most_common(5):
    print(f"{combo} – {cnt} wystąpień ({cnt/N_SIM*100:.6f}%)")