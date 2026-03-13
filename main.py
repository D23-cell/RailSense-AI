import data

def find_station_details(station_name):
    for station in data.station_database:
        if station["name"].lower() == station_name.lower():
            return station
    return None

def calculate_crowd_prediction(station_name, travel_date):
    target_station = find_station_details(station_name)
    
    if not target_station:
        return "Station not found in database"

    base_crowd = target_station["average_daily_footfall"]
    station_category = target_station["category"]
    
    current_multiplier = 1.0
    reason_for_rush = "Normal Day"

    if travel_date in data.global_events:
        event_details = data.global_events[travel_date]
        
        if event_details["impact_type"] == station_category:
            current_multiplier = event_details["multiplier"]
            reason_for_rush = event_details["name"]
        
        elif event_details["impact_type"] == "GLOBAL":
            current_multiplier = event_details["multiplier"]
            reason_for_rush = event_details["name"]

    predicted_crowd = int(base_crowd * current_multiplier)

    display_results(station_name, travel_date, predicted_crowd, reason_for_rush, current_multiplier)

def display_results(name, date, count, reason, risk_level):
    print(f"\n--- REPORT FOR {name.upper()} ---")
    print(f"Date: {date}")
    print(f"Reason: {reason}")
    print(f"Projected Crowd: {count} people")
    
    if risk_level > 5.0:
        print("Status: EXTREMELY OVERCROWDED (Red Alert)")
        print("Seat Chance: 0%")
    elif risk_level > 2.0:
        print("Status: HIGH RUSH (Orange Alert)")
        print("Seat Chance: 20%")
    else:
        print("Status: NORMAL TRAFFIC (Green Signal)")
        print("Seat Chance: 80%")
    print("---------------------------------")


calculate_crowd_prediction("Mathura Junction", "2026-09-04")

calculate_crowd_prediction("Kota Junction", "2026-05-01")

calculate_crowd_prediction("Kyoto Station", "2026-04-15")