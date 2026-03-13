# 🚄 RailSense AI: Real-time Coach Monitoring System

**RailSense AI** is an integrated solution that uses **Computer Vision** and **IoT** to monitor Indian Railways coaches in real time.  
It helps manage **passenger occupancy tracking, security alerts, and revenue protection** efficiently.

---

## 🚀 Key Features

### 🤖 AI Vision
- Live passenger counting using **YOLOv8**
- Detection of **unattended luggage**

### 🔐 Security
- **Criminal detection** using template matching
- **Medical SOS detection** using pose detection

### 💰 Revenue Protection
- Detect **ticketless passengers** by comparing:
  - AI passenger count  
  - Booked ticket data

### 🚪 Operational Alerts
- **Door blocking detection**
- **High crowd density alerts**

### 🍱 Pantry Optimizer
- Calculates **food and water demand** based on real-time occupancy.

### 📱 Multi-Platform Support
- **Web Dashboard**
- **Mobile App (Expo Go)** synchronization

---

# 🛠️ System Architecture & Setup

Follow the steps below to set up the project.

---

## 1️⃣ Prerequisites

Make sure the following tools are installed:

- **Python 3.10+**
- **Node.js & npm** (for Expo mobile app)
- **Expo Go App** (install on your mobile device)

---

## 2️⃣ IP Address Configuration (Important Step) 🚨

To sync the project across devices on the same network, you need your **Laptop's IPv4 Address**.

### Steps

1. Open terminal and run:

```bash
ipconfig

2. Copy the IPv4 Address
Example:

10.14.58.199

3. Update the SERVER_IP or API_URL in the following files:
server.py
vision.py
index.html
tte-app/index.tsx

Replace them with your IPv4 address.


# ⚙️ Installation & Running the Project

Step A: Database Setup
python setup_db.py

Step B: Start Backend Server
python server.py

Step C: Start AI Vision Monitor
python vision.py

Step D: Web Dashboard
Open the following file in your browser: index.html

Step E: Mobile App (Expo Go)
Start the mobile application: cd tte-app
npx expo start

A QR Code will appear in the terminal.

Scan it using the Expo Go app on your mobile phone.


##### 📡 Important Note

Your Laptop and Mobile phone must be connected to the same Wi-Fi network or hotspot for the system to work properly.


##🧠 Tech Stack

1. Computer Vision: YOLOv8

2. Backend: Python

3. Database: SQLite

4. Frontend: HTML / JavaScript

5. Mobile App: React Native (Expo)

6. Database: SQLite / Python DB setup

##📌 Use Case

RailSense AI can help Indian Railways improve:

1. Passenger safety

2. Ticket fraud detection

3. Operational efficiency

4. Food supply planning

5. Real-time monitoring of train coaches
