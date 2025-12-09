import json
from collections import defaultdict, Counter

with open("data/pokreti_klasifikacija.json", "r", encoding="utf-8") as f:
    klasifikacija = json.load(f)

fajlovi_sort = sorted(klasifikacija.keys())

sekvence_pokreta = [klasifikacija[f] for f in fajlovi_sort]

prelazi = defaultdict(Counter)

for i in range(len(sekvence_pokreta) - 1):
    trenutni = sekvence_pokreta[i]
    sledeci = sekvence_pokreta[i+1]
    prelazi[trenutni][sledeci] += 1

markov_matrica = {}
for pokret, sledeci_pokreti in prelazi.items():
    ukupan_broj = sum(sledeci_pokreti.values())
    markov_matrica[pokret] = {sledeci: broj/ukupan_broj for sledeci, broj in sledeci_pokreti.items()}

with open("data/markov_matrica.json", "w", encoding="utf-8") as f:
    json.dump(markov_matrica, f, indent=2, ensure_ascii=False)

print("matrica sačuvana u data/markov_matrica.json")
