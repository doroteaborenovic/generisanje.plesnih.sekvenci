
import os
import json
import random
import numpy as np
import pickle
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx 
import pygame

TRANSITION_FRAMES = 120      
BLEND_WINDOW = 10            
TRANSITION_DURATION_S = 2.4  
markov_path = "data/markov_matrica1.json"

with open(markov_path, "r", encoding="utf-8") as f:
    matrica = json.load(f)

duzina = 8
trenutni = random.choice(list(matrica.keys()))
sekvenca = [trenutni]

for _ in range(duzina - 1):
    moguci = matrica.get(trenutni)
    if not moguci: break
    stanja, ver = list(moguci.keys()), list(moguci.values())
    sledeci = random.choices(stanja, weights=ver, k=1)[0]
    sekvenca.append(sledeci)
    trenutni = sledeci

print(f"\n>>> Generisana sekvenca pokreta: {sekvenca}")

folder_json_2d = "data/keypoints2ddoda"
output_combined_folder = "data"
output_base_name_json = "cisti_keypointsovi"
output_base_name_video = "generisana_varijacija_doda"

def get_next_index_for_prefix(directory, prefix):
    i = 1
    while True:
        candidate = os.path.join(directory, f"{prefix}_{i}.json")
        if not os.path.exists(candidate): return i
        i += 1

index_n = get_next_index_for_prefix(output_combined_folder, output_base_name_json)

def generate_spline_transition(p0, p1, p2, p3, num_frames):
    p0, p1, p2, p3 = map(np.array, [p0, p1, p2, p3])
    transition_frames = []
    for i in range(num_frames):
        t = i / (num_frames - 1) if num_frames > 1 else 0
        frame = 0.5 * (
            (2 * p1) +
            (-p0 + p2) * t +
            (2 * p0 - 5 * p1 + 4 * p2 - p3) * t**2 +
            (-p0 + 3 * p1 - 3 * p2 + p3) * t**3
        )
        transition_frames.append(frame.tolist())
    return transition_frames

def polish_transition(frames, window=5):
    """Primenjuje težinski pokretni prosek na frejmove tranzicije za C2 glatkoću."""
    if window < 3 or window % 2 == 0: return frames
    
    frames_np = np.array(frames)
    polished = np.copy(frames_np)
    half_w = window // 2
    
    weights = np.blackman(window)
    weights /= np.sum(weights)

    for i in range(half_w, len(frames_np) - half_w):
        win = frames_np[i - half_w : i + half_w + 1]
        polished[i] = np.einsum('ijk,i->jk', win, weights)
        
    return polished.tolist()

all_keypoints = []
print("\n--- Spajam keypoints sa dugim i 'ispoliranim' tranzicijama ---")

# Učitavanje videa u memoriju
loaded_clips = []
for pokret in sekvenca:
    fpath = os.path.join(folder_json_2d, pokret + ".json")
    if not os.path.exists(fpath):
        print(f"[!] Nema JSON fajla: {fpath}"); continue
    with open(fpath, "r", encoding="utf-8") as f: data = json.load(f)
    
    frames_cam0 = None
    if isinstance(data, dict):
        kd = data.get("keypoints2d")
        if kd and isinstance(kd, list) and kd: frames_cam0 = kd[0]
    elif isinstance(data, list) and data: frames_cam0 = data[0]

    if frames_cam0:
        cleaned = [[[kp[0], kp[1]] for kp in frame] for frame in frames_cam0 if len(frame) == 17]
        if len(cleaned) > BLEND_WINDOW:
            loaded_clips.append(cleaned)
            print(f"Učitan '{pokret}' sa {len(cleaned)} frejmova.")
        else:
            print(f"[!] Pokret '{pokret}' je prekratak i biće preskočen.")

# spajaju se učitani videi. možda ovo ne bude ni potrebno
for i, current_clip in enumerate(loaded_clips):
    if i == 0:
        all_keypoints.extend(current_clip)
        continue

    prev_clip = loaded_clips[i-1]
    
    p1 = np.array(prev_clip[-1])
    p2 = np.array(current_clip[0])

    avg_prev_pose = np.mean(np.array(prev_clip[-BLEND_WINDOW:-1]), axis=0)
    v_in = p1 - avg_prev_pose
    
    avg_next_pose = np.mean(np.array(current_clip[1:BLEND_WINDOW]), axis=0)
    v_out = avg_next_pose - p2
    
    p0 = p1 - v_in 
    p3 = p2 + v_out

    print(f"  -> Generišem {TRANSITION_FRAMES} prelaznih frejmova...")
    transition = generate_spline_transition(p0, p1, p2, p3, TRANSITION_FRAMES)
    
    print(f"  -> Poliram tranziciju za C2 glatkoću...")
    transition = polish_transition(transition, window=5)

    all_keypoints.pop()
    all_keypoints.extend(transition)
    all_keypoints.extend(current_clip[1:])

if all_keypoints:
    combined_json_output_path = os.path.join(output_combined_folder, f"{output_base_name_json}_{index_n}.json")
    with open(combined_json_output_path, "w", encoding="utf-8") as f:
        json.dump([all_keypoints], f, ensure_ascii=False, indent=2)
    print(f"\n>>> KEYPOINTS spojeni sa tranzicijama u: {combined_json_output_path}")
    print(f"    Ukupno frejmova: {len(all_keypoints)}")
else:
    print("\n[!] Nije bilo moguće učitati nijedan klip. Prekidam.")
    exit()


folder_mp4 = "data/mp4"
video_list = []
for pokret in sekvenca:
    vpath = os.path.join(folder_mp4, pokret + ".mp4")
    if os.path.exists(vpath):
        try: video_list.append(VideoFileClip(vpath))
        except Exception as e: print(f"Problem sa video '{vpath}': {e}")
    else: print(f"[!] Nema video za {pokret}")
if len(video_list) > 1:
    clips_with_fadein = [video_list[0]]
    for clip in video_list[1:]: clips_with_fadein.append(clip.fx(vfx.fadein, TRANSITION_DURATION_S))
    final_video = concatenate_videoclips(clips_with_fadein, padding=-TRANSITION_DURATION_S, method="compose")
    video_output_path = os.path.join(output_combined_folder, f"{output_base_name_video}_{index_n}.mp4")
    final_video.write_videofile(video_output_path, codec="libx264", audio=False)
    print(f">>> Video spojen sa glatkim prelazima i sačuvan kao: {video_output_path}")
elif len(video_list) == 1:
    video_output_path = os.path.join(output_combined_folder, f"{output_base_name_video}_{index_n}.mp4")
    video_list[0].write_videofile(video_output_path, codec="libx264", audio=False)
    print(f">>> Pronađen samo jedan video, sačuvan kao: {video_output_path}")
else: print("Nema nijedan video za spajanje.")

SCALE_FACTOR, SMOOTHING_FACTOR, PRE_SMOOTHING_WINDOW = 0.25, 0.2, 8
JSON_PATH = combined_json_output_path
screen_w, screen_h, fps = 1000, 1000, 50
line_width, point_radius = 3, 4
COLOR_LEFT, COLOR_RIGHT, COLOR_NEUTRAL = (255, 0, 150), (0, 255, 255), (255, 255, 255)
TEXT_COLOR, BG_COLOR = (230, 230, 230), (25, 20, 35)
LEFT_SIDE_INDICES, RIGHT_SIDE_INDICES = [1,3,5,7,9,11,13,15], [2,4,6,8,10,12,14,16]
SKELETON_CONNECTIONS = [(5,6),(11,12),(5,11),(5,7),(7,9),(11,13),(13,15),(6,12),(6,8),(8,10),(12,14),(14,16),(0,1),(0,2),(1,3),(2,4)]

def load_dance(path):
    try:
        with open(path, "r", encoding="utf-8") as f: data = json.load(f)
        return data[0] if data and isinstance(data[0], list) else []
    except Exception as e:
        print(f"Greška pri učitavanju JSON {path}: {e}"); return []
def preprocess_and_smooth(frames, w):
    if w < 2: return frames
    frames_np, out = np.array(frames), np.copy(np.array(frames))
    for i in range(len(frames_np)):
        s, e = max(0, i-w//2), min(len(frames_np), i+w//2+1)
        for p in range(frames_np.shape[1]):
            win = frames_np[s:e, p, :]
            mask = np.any(win != 0, axis=1)
            if np.any(mask): out[i,p,:] = np.mean(win[mask], axis=0)
    return out.tolist()
def normalize_and_scale(points, w, h):
    pts = np.array(points)
    vis = pts[np.any(pts!=0, axis=1)]
    if len(vis) < 2: return np.zeros((17,2))
    center = vis.mean(axis=0)
    if np.any(pts[5]!=0) and np.any(pts[6]!=0): center = (pts[5]+pts[6])/2
    centered = pts - center
    maxr = np.max(np.ptp(vis, axis=0))
    if maxr < 1e-6: maxr = 1
    scaled = (centered/maxr) * np.array([1,-1])
    return scaled * min(w,h)*SCALE_FACTOR + np.array([w/2, h/2])
class Smooth:
    def __init__(self,alpha): self.alpha, self.prev = alpha, None
    def apply(self,new):
        if self.prev is None or self.prev.shape!=new.shape: self.prev=np.copy(new)
        else: self.prev = self.alpha*new + (1-self.alpha)*self.prev
        return self.prev

frames = load_dance(JSON_PATH)
if PRE_SMOOTHING_WINDOW > 1: frames = preprocess_and_smooth(frames, PRE_SMOOTHING_WINDOW)

if not frames: print("Nema frejmova za prikaz.")
else:
    pygame.init()
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Auto Ples - Final FULL")
    clock, font = pygame.time.Clock(), pygame.font.SysFont(None, 30)
    smoother = Smooth(SMOOTHING_FACTOR)
    idx, running, paused = 0, True, False
    print(">>> SPACE pauza, ESC izlaz")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: paused = not paused
        screen.fill(BG_COLOR)
        if idx < len(frames):
            raw = np.array(frames[idx])
            scaled = normalize_and_scale(raw, screen_w, screen_h)
            scaled[:,1] = screen_h - scaled[:,1]
            coords = smoother.apply(scaled)
            for (s,e) in SKELETON_CONNECTIONS:
                if np.any(raw[s]!=0) and np.any(raw[e]!=0):
                    c = COLOR_LEFT if s in LEFT_SIDE_INDICES or e in LEFT_SIDE_INDICES else COLOR_RIGHT
                    pygame.draw.line(screen, c, coords[s], coords[e], line_width)
            for ii,pt in enumerate(raw):
                if np.any(pt!=0):
                    cc = COLOR_LEFT if ii in LEFT_SIDE_INDICES else COLOR_RIGHT
                    pygame.draw.circle(screen, cc, coords[ii].astype(int), point_radius)
            if not paused: idx = (idx + 1) % len(frames)
        txt = font.render(f"{idx}/{len(frames)}", True, TEXT_COLOR)
        screen.blit(txt, (10,10))
        if paused:
            pause_txt = font.render("PAUSED", True, (255,255,0))
            screen.blit(pause_txt, (screen_w//2 - 45, 30))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
