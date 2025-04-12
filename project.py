import cv2
import dlib
import numpy as np
import time
import requests
import pygetwindow as gw
import pygame

print("🔒 NOTICE: This application monitors your eye activity and whether Zoom/Meet is your active window. No data is saved or shared beyond alerting the host.")

# ====== Telegram Bot Setup ======
BOT_TOKEN = "7428822866:AAELMUqUFhZeuBSlSkGSfAh5VDd3BxIV9-8"
CHAT_ID = "1904686292"  # Replace this with your actual chat ID

last_alert_time = 0
COOLDOWN_SECONDS = 5

def should_alert():
    global last_alert_time
    now = time.time()
    if now - last_alert_time >= COOLDOWN_SECONDS:
        last_alert_time = now
        return True
    return False

def play_notification_sound():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("ding.mp3")  # Ensure this file exists
        pygame.mixer.music.play()
        time.sleep(2)
    except Exception as e:
        print(f"🔇 Failed to play sound: {e}")

def is_zoom_or_meet_focused():
    try:
        active = gw.getActiveWindow()
        if active is None:
            return False
        title = active.title
        return any(app in title for app in ["Zoom", "Meet", "Google Meet"])
    except Exception as e:
        print(f"⚠️ Error checking active window: {e}")
        return False

def notify_host(student_name, reason="Student is distracted or inattentive."):
    text = f"🚨 ALERT: Student '{student_name}' is inattentive!\nReason: {reason}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Alert sent successfully!")
        else:
            print(f"❌ Failed to send alert. Error: {response.text}")
    except Exception as e:
        print(f"❌ Telegram API error: {e}")

# ====== Eye Detection Setup ======
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def calibrate_ear(cap, detector, predictor, calibration_time=5):
    print("🔧 Calibrating eye detection... please look directly at the camera.")
    start_time = time.time()
    ear_values = []

    while time.time() - start_time < calibration_time:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        if len(faces) == 0:
            continue

        largest_face = max(faces, key=lambda rect: rect.width() * rect.height())
        landmarks = predictor(gray, largest_face)

        left_eye = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(36, 42)])
        right_eye = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(42, 48)])

        avg_ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0
        ear_values.append(avg_ear)

    if not ear_values:
        print("⚠️ Calibration failed. Using default EAR threshold.")
        return 0.25

    personalized_threshold = np.mean(ear_values) * 0.75
    print(f"✅ EAR calibrated. Threshold set to {personalized_threshold:.3f}")
    return personalized_threshold

# ====== Student Login ======
import argparse
import os

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--email', required=True)
args = parser.parse_args()
email = args.email

# Read datasheet.txt and find the name
student_name = "Unknown"
if os.path.exists("datasheet.txt"):
    with open("datasheet.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        for i in range(0, len(lines), 5):
            try:
                e = lines[i+2].split("Email: ")[1]
                if e == email:
                    student_name = lines[i].split("Full Name: ")[1]
                    break
            except IndexError:
                continue

cap = cv2.VideoCapture(0)
EYE_AR_THRESHOLD = calibrate_ear(cap, detector, predictor)

# ====== Runtime Vars ======
EYE_CLOSED_FRAMES = 10
NO_FACE_THRESHOLD = 10
WINDOW_UNFOCUSED_THRESHOLD = 45

closed_frames = 0
no_face_frames = 0
no_focus_frames = 0

eye_alert_sent = False
face_alert_sent = False
focus_alert_sent = False

print("👀 Eye-tracking started... press 'Q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if not faces:
        no_face_frames += 1
        closed_frames = 0
        print(f"Face not detected for {no_face_frames} frames")
        if no_face_frames >= NO_FACE_THRESHOLD and not face_alert_sent and should_alert():
            notify_host(student_name, reason="No face detected for a long time.")
            play_notification_sound()
            face_alert_sent = True
    else:
        no_face_frames = 0
        face_alert_sent = False

        largest_face = max(faces, key=lambda rect: rect.width() * rect.height())
        landmarks = predictor(gray, largest_face)

        left_eye = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(36, 42)])
        right_eye = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(42, 48)])

        avg_ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0

        if avg_ear < EYE_AR_THRESHOLD:
            closed_frames += 1
            print(f"Eyes closed for {closed_frames} frames")
            if closed_frames >= EYE_CLOSED_FRAMES and not eye_alert_sent and should_alert():
                notify_host(student_name, reason="Eyes closed / sleeping / not attentive.")
                play_notification_sound()
                eye_alert_sent = True
        else:
            closed_frames = 0
            eye_alert_sent = False

    if not is_zoom_or_meet_focused():
        no_focus_frames += 1
        print(f"Zoom/Meet not active for {no_focus_frames} frames")
        if no_focus_frames >= WINDOW_UNFOCUSED_THRESHOLD and not focus_alert_sent and should_alert():
            notify_host(student_name, reason="Zoom/Meet window not in focus")
            play_notification_sound()
            focus_alert_sent = True
    else:
        no_focus_frames = 0
        focus_alert_sent = False

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


