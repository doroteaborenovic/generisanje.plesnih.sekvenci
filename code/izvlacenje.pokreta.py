import os
import json
#ovo je bitno jer je lista pokreta i kako su klasifikovani u matricu
folder_sekvenci = os.path.join("data", "sekvence")

sve_sekvence = {}

for ime_fajla in os.listdir(folder_sekvenci):
    if ime_fajla.endswith(".json"):
        putanja = os.path.join(folder_sekvenci, ime_fajla)
        with open(putanja, 'r') as f:
            podaci = json.load(f)

        print(f"\n==> {ime_fajla}")
        for i, frame in enumerate(podaci):
            if frame is not None and isinstance(frame, dict):
                keypoints = frame.get("pose_landmarks", [])
                print(f"Frame {i+1}: {len(keypoints)} ključnih tačaka")
            else:
                print(f"Frame {i+1}: preskočen (prazan ili nevalidan)")

        pokret = input(f"Unesi naziv pokreta za fajl '{ime_fajla}': ").strip().lower()
        sve_sekvence[ime_fajla] = pokret

os.makedirs("data", exist_ok=True)
with open("data/pokreti_klasifikacija.json", "w", encoding="utf-8") as f:
    json.dump(sve_sekvence, f, indent=2, ensure_ascii=False)

print("\nyavrseno i sacuvano u data/pokreti_klasifikacija.json")
