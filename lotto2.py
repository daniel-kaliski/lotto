import urllib.request
import random
from collections import Counter
import ssl  # <-- Dodany import do obsługi SSL

def run_lotto():
    print("1. Pobieranie wyników z wynikilotto.net.pl...")
    url = "https://www.wynikilotto.net.pl/download/lotto.csv"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    # Tworzymy kontekst, który ignoruje błędy certyfikatów SSL
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        # Dodajemy nasz kontekst (ctx) do żądania
        with urllib.request.urlopen(req, context=ctx) as response:
            dane = response.read().decode('utf-8').splitlines()
    except Exception as e:
        print(f"Błąd podczas pobierania pliku: {e}")
        return
        
    print("2. Analiza historycznych losowań...")
    historyczne_liczby = Counter()
    
    for linia in dane:
        elementy = linia.strip().split(',')
        if len(elementy) >= 6:
            try:
                liczby = [int(x) for x in elementy[-6:]]
                historyczne_liczby.update(liczby)
            except ValueError:
                continue
                
    print("\n--- TOP 5 najczęściej losowanych liczb w historii Lotto ---")
    for liczba, ile in historyczne_liczby.most_common(5):
        print(f"Liczba {liczba:2d}: wylosowana {ile} razy")

    print("\n3. Rozpoczynam symulację 10 000 000 losowań...")
    print("   (Zajmie to około 30-40 sekund. Czekaj cierpliwie...)")
    
    symulowane_zestawy = Counter()
    pula_liczb = list(range(1, 50)) 
    
    for i in range(10_000_000):
        losowanie = tuple(sorted(random.sample(pula_liczb, 6)))
        symulowane_zestawy[losowanie] += 1
        
        if (i + 1) % 2_500_000 == 0:
            print(f"   -> Wykonano {(i + 1):,} losowań...".replace(',', ' '))

    print("\n=============================================")
    print("  TOP 4 NAJCZĘŚCIEJ LOSOWANE ZESTAWY W SYMULACJI")
    print("=============================================")
    for zestaw, ile_razy in symulowane_zestawy.most_common(4):
        print(f"Zestaw: {zestaw} | Wylosowano: {ile_razy} razy")

if __name__ == '__main__':
    run_lotto()