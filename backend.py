print("🚀 RAIL-SENSE BACKEND IS WAKING UP...")

import sqlite3
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

live_coach_data = {"count": 0, "current_station": "Mathura Junction"}

def get_db_connection():
    conn = sqlite3.connect('railsense.db')
    conn.row_factory = sqlite3.Row
    return conn

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.get("/")
def home():
    return {"message": "RailSense AI Server is Running!"}

@app.post("/update_live_count")
async def update_count(count: int):
    live_coach_data["count"] = count
    
    try:
        conn = get_db_connection()
        row = conn.execute('SELECT booked_seats FROM stations WHERE name = ?', (live_coach_data["current_station"],)).fetchone()
        conn.close()
        booked = row['booked_seats'] if row else 0
    except:
        booked = 0
        
    ticketless = max(0, count - booked)

    await manager.broadcast({
        "live_count": count,
        "booked_seats": booked,
        "ticketless_detected": ticketless
    })
    
    return {"status": "updated"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/predict/{station_name}/{date}")
def predict_crowd(station_name: str, date: str):
    try:
        conn = get_db_connection()
        station = conn.execute("SELECT * FROM stations WHERE name LIKE ?", (station_name,)).fetchone()
        
        if not station:
            conn.close()
            return {"error": "Station not found"}

        event = conn.execute("SELECT * FROM events WHERE date = ?", (date,)).fetchone()
        conn.close()

        base_crowd = station['avg_footfall']
        multiplier = 1.0
        reason = "Normal Day"
        
        if event:
            if event['impact_type'] == station['category'] or event['impact_type'] == "CAPITAL":
                multiplier = event['multiplier']
                reason = event['name']

        predicted_crowd = int(base_crowd * multiplier)
        status = "Red Alert" if multiplier >= 5 else "High Rush" if multiplier >= 2 else "Normal"

        return {
            "station": station['name'], "date": date,
            "crowd_count": predicted_crowd, "status": status, "reason": reason
        }
    except:
        return {"error": "Database error"}

if __name__ == "__main__":
    print("🟢 Server starting on PORT 8080... Please wait!")
    uvicorn.run(app, host="0.0.0.0", port=8080)