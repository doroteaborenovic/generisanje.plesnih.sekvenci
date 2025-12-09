import cv2
import mediapipe as mp
import json
import os

ulazni_folder = "data/mp4"
izlazni_folder = "data/mp4ijson"


mp_pose = mp.solutions.pose

def extract_pose_from_video(video_path):
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
    cap = cv2.VideoCapture(video_path)
    pose_data = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
        if results.pose_landmarks:
            landmarks = []
            for lm in results.pose_landmarks.landmark:
                landmarks.append({
                    'x': lm.x,
                    'y': lm.y,
                    'z': lm.z,
                    'visibility': lm.visibility
                })
            pose_data.append(landmarks)
        else:
            pose_data.append(None)

    cap.release()
    pose.close()
    return pose_data

def main():
    os.makedirs(izlazni_folder, exist_ok=True)
    video_fajlovi = [f for f in os.listdir(ulazni_folder) if f.endswith(".mp4")]

    for video_fajl in video_fajlovi:
        naziv = os.path.splitext(video_fajl)[0]
        video_path = os.path.join(ulazni_folder, video_fajl)
        json_path = os.path.join(izlazni_folder, f"{naziv}.json")
        mp4_copy_path = os.path.join(izlazni_folder, video_fajl)

        print(f"🎞️ Obrada: {video_fajl}")
        podaci = extract_pose_from_video(video_path)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(podaci, f, indent=2, ensure_ascii=False)

       
        with open(video_path, "rb") as src, open(mp4_copy_path, "wb") as dst:
            dst.write(src.read())

        print(f" JSON: {json_path}")
        print(f" MP4: {mp4_copy_path}")

if __name__ == "__main__":
    main()
