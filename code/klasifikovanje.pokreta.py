import os
import json

folder = "data/mp4"  
klasifikacija = {}

for fajl in os.listdir(folder):
    if fajl.endswith(".mp4"):
        ime_bez_ekstenzije = os.path.splitext(fajl)[0]
        klasifikacija[fajl] = ime_bez_ekstenzije  

output_path = os.path.join("data", "klasifikacija_pokreta.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(klasifikacija, f, ensure_ascii=False, indent=2)

print("Napravljen fajl pokreti_klasifikacija.json")
