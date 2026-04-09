# 🚄 RailSense AI: Real-time Coach Monitoring System (Cloud Edition)

**RailSense AI** is a professional-grade integrated solution that uses **Computer Vision (YOLOv8)** and **Cloud Computing** to monitor Indian Railways coaches in real time. Deploying a full-stack architecture, it connects an AI Vision edge device (Laptop) to a Cloud Backend (Render), serving real-time data to a Web Dashboard and Mobile App globally.

---

## 🚀 Key Features

### 🤖 AI Vision & Security

- **Live Passenger Counting:** Real-time occupancy tracking using **YOLOv8**.
- **Criminal Detection:** Template matching for identifying blacklisted individuals.
- **Medical SOS:** Pose detection to identify passengers needing emergency help.
- **Unattended Luggage:** Automated alerts for suspicious/forgotten bags.

### 💰 Revenue & Operations

- **Ticketless Detection:** Automatic revenue loss calculation by comparing live count vs booked data.
- **Operational Alerts:** Real-time triggers for **Door Blocking** and **High Crowd Density**.
- **Pantry Optimizer:** Dynamic calculation of food and water demand based on live coach occupancy.

### 🌐 Cloud & Sync

- **Global Accessibility:** Hosted on **Render**, accessible from any network.
- **Multi-Platform:** Synchronized **Web Dashboard** and **Mobile App (React Native)**.

---

## 🛠️ System Architecture

1. **Edge Layer (Laptop):** Processes YOLOv8 locally for high speed.
2. **Cloud Layer (Render):** FastAPI backend handles logic and SQLite database.
3. **Display Layer:** HTML5/JS Dashboard and Expo Go Mobile App fetch data via REST APIs.

---

## ⚙️ Installation & Setup

### 1️⃣ Prerequisites

- Python 3.10+
- `pip install -r requirements.txt`
- Node.js (for Expo Mobile App)

### 2️⃣ Running the Edge AI (Local)

Ensure you have updated the `API_URL` in `vision.py` to your Render URL.

```bash
python vision.py

### 3️⃣ Accessing the Dashboards (Cloud)
Since the project is live on Render, you can access it directly:

Master Dashboard: https://railsense-ai.onrender.com

Pantry Hub: https://railsense-ai.onrender.com/pantry

### 4️⃣ Mobile App Setup
Go to the tte-app directory.

Update the API_URL in index.tsx.

Start the app:

Bash
npx expo start
Scan the QR code with Expo Go on your mobile (Works on Mobile Data too!).

🧠 Tech Stack
1. AI/ML: YOLOv8, OpenCV, Ultralytics

2. Backend: FastAPI (Python), Uvicorn

3. Frontend: HTML5, CSS3, JavaScript (Chart.js)

4. Mobile: React Native (Expo)

5. Deployment: Render (Cloud Hosting), GitHub (CI/CD)

6. Database: SQLite3


📌 Use Cases

1. Safety: Real-time crime and medical emergency monitoring.

2. Revenue: Detecting ticketless travelers without manual checking.

3. Efficiency: Optimizing pantry supply to reduce food wastage.
```
