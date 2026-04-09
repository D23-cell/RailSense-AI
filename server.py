from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse # Dashboard serve karne ke liye
import uvicorn, sqlite3, time, random, os # os zaroori hai port ke liye

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

verified_tickets = 0
current_fine_amount = 0
current_alerts = {"security": "NORMAL", "operational": "NORMAL"}

# --- RENDER SPECIAL: Serve Frontend ---
@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.get("/pantry")
async def read_pantry():
    return FileResponse('pantry.html')
# ---------------------------------------

def init_db():
    conn = sqlite3.connect('railsense.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, count INTEGER, timestamp REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS alerts (id INTEGER PRIMARY KEY, message TEXT, time REAL)''')
    cursor.execute("INSERT OR IGNORE INTO history (count, timestamp) VALUES (0, ?)", (time.time(),))
    conn.commit()
    conn.close()

init_db()

@app.post("/update_live_count")
async def update_count(count: int):
    conn = sqlite3.connect('railsense.db')
    conn.execute("INSERT INTO history (count, timestamp) VALUES (?, ?)", (count, time.time()))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.post("/add_alert")
async def add_alert(request: Request):
    data = await request.json()
    msg = data.get("type", "Unknown").upper()
    if "CRIMINAL" in msg or "MEDICAL" in msg:
        current_alerts["security"] = msg
    else:
        current_alerts["operational"] = msg
    conn = sqlite3.connect('railsense.db')
    conn.execute("INSERT INTO alerts (message, time) VALUES (?, ?)", (msg, time.time()))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.get("/get_status")
async def get_status():
    conn = sqlite3.connect('railsense.db')
    cursor = conn.cursor()
    cursor.execute("SELECT count FROM history ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    count = row[0] if row else 0
    conn.close()
    ticketless = max(0, count - verified_tickets)
    return {
        "count": count,
        "security_alert": current_alerts["security"],
        "op_alert": current_alerts["operational"],
        "verified_count": verified_tickets,
        "ticketless_count": ticketless,
        "total_fine": current_fine_amount,
        "prediction": "High Load" if count > 3 else "Normal"
    }

@app.get("/pantry_demand")
async def pantry_demand():
    conn = sqlite3.connect('railsense.db')
    cursor = conn.cursor()
    cursor.execute("SELECT count FROM history ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    count = row[0] if row else 0
    conn.close()
    return {
        "current_occupancy": count,
        "meals_needed": count * 1,
        "water_bottles": count * 2,
        "pantry_status": "URGENT PREP" if count > 3 else "Normal"
    }

@app.post("/verify_ticket")
async def verify():
    global verified_tickets
    verified_tickets += 1
    return {"verified_count": verified_tickets}

@app.post("/generate_fine")
async def fine():
    global current_fine_amount
    current_fine_amount += 500
    return {"total_fine": current_fine_amount}

@app.post("/reset_all")
async def reset():
    global verified_tickets, current_fine_amount
    verified_tickets = 0
    current_fine_amount = 0
    current_alerts["security"] = "NORMAL"
    current_alerts["operational"] = "NORMAL"
    return {"status": "reset"}

@app.get("/get_station_data")
async def station_data(name: str):
    return {"station": name.capitalize(), "expected_count": random.randint(20, 50)}

if __name__ == "__main__":
    # Render environmental variables se port uthata hai
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)