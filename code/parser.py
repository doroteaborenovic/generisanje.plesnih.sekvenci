import os
import json

folder = "../data/sekvence"

def ucitaj_pokrete_iz_jsona(putanja_do_fajla):
    with open(putanja_do_fajla, 'r') as f:
        podaci = json.load(f)
    

 
    return podaci

if __name__ == "__main__":
    fajlovi = [f for f in os.listdir(folder) if f.endswith('.json')]
    for fajl in fajlovi:
        putanja = os.path.join(folder, fajl)
        pokreti = ucitaj_pokrete_iz_jsona(putanja)
        print(f"Pokreti iz {fajl}: {pokreti[:5]}")  # prikaz prvih 5 za primer
