import os
import json
import pickle
import numpy as np
import glob

folder_2d = "data/keypoints2dples"
folder_3d = "data/keypoints3dples"
folder_sekvenci = "data/mp4ijson"
os.makedirs(folder_sekvenci, exist_ok=True)

fajlovi = glob.glob(os.path.join(folder_sekvenci, "generisana_sekvenca_*.json"))
if not fajlovi:
    print("Nema generisanih sekvenci.")
    exit()

putanja_sekvence = max(fajlovi, key=os.path.getctime)
print(f"Učitavam sekvencu iz: {os.path.basename(putanja_sekvence)}")

with open(putanja_sekvence, "r", encoding="utf-8") as f:
    sekvenca = json.load(f)

broj = os.path.splitext(os.path.basename(putanja_sekvence))[0].split("_")[-1]

def ucitaj_keypoints_iz_pkl(putanja):
    with open(putanja, "rb") as f:
        return pickle.load(f)

def konvertuj_u_serializable(data):
    if isinstance(data, np.ndarray):
        return data.tolist()
    if isinstance(data, dict):
        return {k: konvertuj_u_serializable(v) for k, v in data.items()}
    if isinstance(data, list):
        return [konvertuj_u_serializable(x) for x in data]
    return data

svi_keypoints_2d = []
svi_keypoints_3d = []

for pokret in sekvenca:
    putanja_2d = os.path.join(folder_2d, f"{pokret}.pkl")
    putanja_3d = os.path.join(folder_3d, f"{pokret}.pkl")

    if os.path.exists(putanja_2d):
        svi_keypoints_2d.append(ucitaj_keypoints_iz_pkl(putanja_2d))
    else:
        print(f"Ne postoji 2D keypoints za {pokret}")

    if os.path.exists(putanja_3d):
        svi_keypoints_3d.append(ucitaj_keypoints_iz_pkl(putanja_3d))
    else:
        print(f"Ne postoji 3D keypoints za {pokret}")

ime_keypoints_2d = f"keypoints_varijacija_{broj}_2d.json"
ime_keypoints_3d = f"keypoints_varijacija_{broj}_3d.json"

with open(os.path.join(folder_sekvenci, ime_keypoints_2d), "w", encoding="utf-8") as f:
    json.dump(konvertuj_u_serializable(svi_keypoints_2d), f, ensure_ascii=False, indent=2)

with open(os.path.join(folder_sekvenci, ime_keypoints_3d), "w", encoding="utf-8") as f:
    json.dump(konvertuj_u_serializable(svi_keypoints_3d), f, ensure_ascii=False, indent=2)

print(f"Keypoints 2D sačuvani kao {ime_keypoints_2d}")
print(f" Keypoints 3D sačuvani kao {ime_keypoints_3d}")
print("Sekvenca:", sekvenca)
