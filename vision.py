import cv2
from ultralytics import YOLO
import requests, time, numpy as np, os

SERVER_IP = "https://railsense-ai.onrender.com"
API_URL = "https://railsense-ai.onrender.com"
model = YOLO('yolov8n.pt') 
pose_model = YOLO('yolov8n-pose.pt') 
cap = cv2.VideoCapture(0)

criminal_path = "criminal1.jpg"
criminal_img = cv2.imread(criminal_path, 0) if os.path.exists(criminal_path) else None

criminal_active = False
medical_active = False
door_alert_sent = False
luggage_alert_sent = False
door_block_start = 0
last_sync_time = 0
last_density_alert = 0 
print(f"🚄 RailSense AI: MASTER MONITORING ACTIVE.")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame_small = cv2.resize(frame, (320, 240))
    gray = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)

    if criminal_img is not None:
        res = cv2.matchTemplate(gray, cv2.resize(criminal_img, (80, 80)), cv2.TM_CCOEFF_NORMED)
        is_match = np.any(res >= 0.75)
        if is_match and not criminal_active:
            try:
                requests.post(f"{API_URL}/add_alert", json={"type": "CRIMINAL DETECTED"})
                criminal_active = True
                print("🚨 CRIMINAL ALERT SENT")
            except: pass
        elif not is_match:
            criminal_active = False

    pose_results = pose_model(frame_small, verbose=False, imgsz=160)
    is_sos = False
    for r in pose_results:
        if r.keypoints and len(r.keypoints.data[0]) > 10:
            k = r.keypoints.data[0]
            if k[9][1] < k[0][1] and k[10][1] < k[0][1]: is_sos = True
    
    if is_sos and not medical_active:
        try:
            requests.post(f"{API_URL}/add_alert", json={"type": "MEDICAL EMERGENCY"})
            medical_active = True
            print("🆘 MEDICAL SOS SENT")
        except: pass
    elif not is_sos:
        medical_active = False

    results = model.predict(frame_small, imgsz=160, conf=0.4, classes=[0, 24, 26, 28], verbose=False)
    persons, bags = [], []
    for box in results[0].boxes:
        cls, coords = int(box.cls[0]), box.xyxy[0].tolist()
        if cls == 0: persons.append(coords)
        else: bags.append(coords)

    count = len(persons)
    if time.time() - last_sync_time > 2:
        try:
            requests.post(f"{API_URL}/update_live_count?count={int(count)}")
            last_sync_time = time.time()
        except: pass

    for bag in bags:
        is_attended = any(np.linalg.norm(np.array(bag[:2]) - np.array(p[:2])) < 120 for p in persons)
        if not is_attended and not luggage_alert_sent:
            try:
                requests.post(f"{API_URL}/add_alert", json={"type": "UNATTENDED LUGGAGE"})
                luggage_alert_sent = True
                print("⚠️ LUGGAGE ALERT SENT")
            except: pass
        elif is_attended:
            luggage_alert_sent = False

    
    if count > 0:
        if door_block_start == 0: door_block_start = time.time()
        if time.time() - door_block_start > 2 and not door_alert_sent:
            try:
                requests.post(f"{API_URL}/add_alert", json={"type": "DOOR BLOCKED"})
                door_alert_sent = True
                print("⚠️ DOOR BLOCKED ALERT SENT")
            except: pass
    else:
        door_block_start = 0
        door_alert_sent = False

    if count >= 3: 
        if time.time() - last_density_alert > 10: 
            try:
                requests.post(f"{API_URL}/add_alert", json={"type": "HIGH CROWD DENSITY"})
                last_density_alert = time.time()
                print("⚠️ HIGH CROWD DENSITY ALERT SENT")
            except: pass
    elif count < 3:
        last_density_alert = 0 

    cv2.imshow("RailSense AI Security Monitor", results[0].plot())
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cap.release()
cv2.destroyAllWindows()