import cv2
import mediapipe as mp
import json
import os

mp_pose = mp.solutions.pose

input_folder = "data/sekvence"
output_folder = "data/sekvence"  

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
    video_files = [f for f in os.listdir(input_folder) if f.endswith('.mp4')]

    for video_file in video_files:
        print(f"Procesiram {video_file} ...")
        video_path = os.path.join(input_folder, video_file)
        pose_sequence = extract_pose_from_video(video_path)

        json_filename = os.path.splitext(video_file)[0] + '.json'
        json_path = os.path.join(output_folder, json_filename)

        with open(json_path, 'w') as f:
            json.dump(pose_sequence, f)

        print(f"Snimljen JSON: {json_path}")

if __name__ == "__main__":
    main()

