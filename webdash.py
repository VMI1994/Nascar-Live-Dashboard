# Data Analysis Report: See original code comments for JSON structure details.subp

from flask import Flask, render_template, jsonify
import requests
import json
import time
import sys
from datetime import timedelta

# Flask app setup
app = Flask(__name__)

URL = "https://cf.nascar.com/live/feeds/live-feed.json"
UPDATE_INTERVAL = 2000  # 2 seconds (used in frontend JavaScript)
STAGNATION_THRESHOLD = 30  # seconds

class NascarDashboard:
    def __init__(self):
        self.previous_data = None
        self.stagnation_time = 0
        self.last_fetch_time = time.time()

    def fetch_data(self):
        try:
            response = requests.get(URL, timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Error fetching data: {str(e)}"}

    def format_time(self, seconds):
        if seconds is None:
            return "N/A"
        td = timedelta(seconds=seconds)
        return str(td)

    def compute_laps_led_count(self, laps_led):
        count = 0
        for period in laps_led:
            count += period.get('end_lap', 0) - period.get('start_lap', 0) + 1
        return count

    def process_data(self):
        data = self.fetch_data()
        if "error" in data:
            return data

        # Check for stagnation
        current_time = time.time()
        if self.previous_data is not None and json.dumps(data) == json.dumps(self.previous_data):
            self.stagnation_time += (current_time - self.last_fetch_time)
        else:
            self.stagnation_time = 0
        self.last_fetch_time = current_time
        self.previous_data = data

        # Process race info
        race_info = {}
        for key, value in data.items():
            if key not in ['vehicles', 'stage']:
                if key == 'elapsed_time':
                    value = self.format_time(value)
                race_info[key] = value
        if 'stage' in data:
            race_info['stage'] = str(data['stage'])

        # Process vehicles
        vehicles = data.get('vehicles', [])
        leader_elapsed = vehicles[0].get('vehicle_elapsed_time', 0) if vehicles else 0
        vehicles_data = []

        for idx, vehicle in enumerate(vehicles, start=1):
            driver = vehicle.get('driver', {})
            driver_name = driver.get('full_name', 'N/A')
            laps_led = vehicle.get('laps_led', [])
            laps_led_count = self.compute_laps_led_count(laps_led)
            pit_stops_count = len(vehicle.get('pit_stops', []))
            delta = vehicle.get('delta', vehicle.get('vehicle_elapsed_time', 0) - leader_elapsed)
            delta = '-' if delta == 0 else f"{delta:.3f}"

            vehicles_data.append({
                'Position': idx,
                'Number': vehicle.get('vehicle_number', 'N/A'),
                'Driver': driver_name,
                'Starting Pos': vehicle.get('starting_position', 'N/A'),
                'Running Pos': vehicle.get('running_position', idx),
                'Status': vehicle.get('status', 'N/A'),
                'Laps Completed': vehicle.get('laps_completed', 'N/A'),
                'Delta': delta,
                'Last Lap Time': f"{vehicle.get('last_lap_time', 0):.3f}",
                'Last Lap Speed': f"{vehicle.get('last_lap_speed', 0):.3f}",
                'Best Lap Time': f"{vehicle.get('best_lap_time', 0):.3f}",
                'Best Lap Speed': f"{vehicle.get('best_lap_speed', 0):.3f}",
                'Average Speed': f"{vehicle.get('average_speed', 0):.3f}",
                'Fastest Laps': vehicle.get('fastest_laps_run', 'N/A'),
                'Laps Led Count': laps_led_count,
                'Pit Stops': pit_stops_count,
                'On Track': vehicle.get('is_on_track', 'N/A'),
                'Sponsor': vehicle.get('sponsor_name', 'N/A')
            })

        return {
            'race_info': race_info,
            'vehicles': vehicles_data,
            'stagnation': self.stagnation_time > STAGNATION_THRESHOLD
        }

# Initialize dashboard
dashboard = NascarDashboard()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    return jsonify(dashboard.process_data())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8448)
