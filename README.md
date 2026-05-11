# RaceDash - Live NASCAR Race Dashboard

A real-time web dashboard that displays live NASCAR race data using the official NASCAR live feed API. Built with Python Flask and a modern Tailwind CSS frontend.

![RaceDash Dashboard Preview](https://img.shields.io/badge/Status-Live-green)
![License](https://img.shields.io/badge/License-MIT-blue)

## 🚀 Features

- **Real-Time Data Updates**: Automatically refreshes NASCAR data every 2 seconds
- **Live Standings Table**: Complete driver standings with positions, times, and speeds
- **Race Status Display**: Shows current lap, elapsed time, laps to go, and flag state
- **Visual Flag Indicators**: Green flag (free racing), Yellow flag (caution), Red flag (stop), Checkered flag (finished)
- **Driver Statistics**: Includes manufacturer, starting position, running position, and passing differential
- **Performance Metrics**: Best lap times, average speeds, and fastest laps
- **Leaderboard Highlighting**: Top position driver highlighted in green
- **On/Track Status**: Visual indicator showing which drivers are on track
- **Stagnation Detection**: Warns when data stops updating (race may be under caution or finished)
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🎯 What It Shows

- **Driver Information**: Full name, vehicle number, and manufacturer
- **Race Position**: Current and starting positions
- **Timing Data**: Last lap time, best lap time, average speed, fastest laps
- **Performance Stats**: Laps completed, delta times (gap to leader)
- **Passing Statistics**: Passes made, times passed, passing differential
- **Track Information**: Current race track name and series

## 📊 Data Source

RaceDash pulls real-time data from the official NASCAR API:
- **Base URL**: https://cf.nascar.com/live/feeds/live-feed.json
- **Data Frequency**: Updates automatically every 2 seconds
- **Content**: Full race telemetry, driver standings, and real-time status

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/RaceDash.git
   cd RaceDash
   ```

2. **Install dependencies**:
   ```bash
   pip install flask requests
   ```

3. **Run the dashboard**:
   ```bash
   python RaceDash.py
   ```

The dashboard will automatically open in your browser at http://127.0.0.1:8448

## 🎨 How to Run

The application has two ways to run:

### Option 1: Python Directly
```bash
python RaceDash.py
```
This will:
- Start the Flask web server on port 8448
- Automatically open the dashboard in your default browser
- Begin auto-refreshing data every 2 seconds

### Option 2: Manual Access
If you want to access the dashboard manually:
```bash
python RaceDash.py &
```
Then open http://127.0.0.1:8448 in your browser

## 📝 API Endpoints

### `/`
Main dashboard page with full UI rendering

### `/api/live`
REST API endpoint returning JSON data in the same format as the live feed

**Example**:
```bash
curl http://127.0.0.1:8448/api/live
```

## 🎯 Usage Examples

### Accessing Race Data via API
```python
import requests

response = requests.get('http://127.00.1:8448/api/live')
race_data = response.json()

# Get top driver
top_driver = race_data['vehicles'][0]
print(f"Leader: {top_driver['driver']['full_name']} ({top_driver['vehicle_number']})")

# Get current lap
print(f"Current Lap: {race_data['lap_number']}")

# Get flag state
print(f"Flag: {race_data['flag_state']}")
```

### Checking Race Status
```python
if race_data['flag_state'] == 9:
    print("🏁 Checkered flag - Race finished!")
elif race_data['flag_state'] == 1:
    print("🟢 Green flag - Free racing")
elif race_data['flag_state'] == 2:
    print("🟡 Yellow flag - Caution in effect")
```

## 🔧 Configuration

The dashboard runs on:
- **Port**: 8448
- **Host**: localhost (127.0.0.1)
- **Refresh Rate**: 2 seconds (auto-refresh)

You can modify these values in the Flask app configuration or the `__main__` section.

## 🌐 Cross-Platform Support

RaceDash has been built and packaged for:
- ✅ **macOS** (Silicon/M1/M2)
- ✅ **Windows 11**
- ✅ **Ubuntu/Linux**

### Building Binaries with PyInstaller

```bash
# macOS
pyinstaller --onefile --windowed --name RaceDash RaceDash.py

# Windows
pyinstaller --onefile --noconsole --name RaceDash RaceDash.py

# Ubuntu
pyinstaller --onefile --windowed --name RaceDash RaceDash.py
```

## 📱 Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Opera

## 🎯 Key Features Explained

### Flag States
| Flag | Value | Description |
|------|-------|-------------|
| 🟢 Green | 1 | Free racing |
| 🟡 Yellow | 2 | Caution |
| 🔴 Red | 3 | Stop |
| ⚫⚪⚫⚪ Checkered | 9 | Race finished |

### Data Fields

**Race Info**:
- `lap_number`: Current lap count
- `elapsed_time`: Time since race start
- `laps_to_go`: Remaining laps
- `flag_state`: Current flag (1-9)
- `run_name`: Race name (e.g., "Tow Road 400")
- `track_name`: Track location
- `series_id`: NASCAR series identifier
- `time_of_day_os`: Local race time (not UTC)
- `number_of_lead_changes`: How many times the leader changed
- `number_of_leaders`: Current leader count

**Driver Stats**:
- `driver.full_name`: Driver's full name
- `vehicle_number`: Car number
- `vehicle_manufacturer`: Team/manufacturer
- `starting_position`: Original grid position
- `running_position`: Current position
- `laps_completed`: Laps finished
- `delta`: Time gap to leader
- `last_lap_time`: Time of most recent lap
- `last_lap_speed`: Speed of most recent lap
- `best_lap_time`: Best lap time
- `best_lap_speed`: Fastest lap speed
- `average_speed`: Overall average speed
- `passes_made`: Total passes made
- `times_passed`: Number of times passed
- `passing_differential`: Gap improvement vs leader
- `fastest_laps_run`: Number of fastest laps
- `laps_led`: Laps led by this driver
- `is_on_track`: ✅ or ❌ on/off track status

## 🐛 Troubleshooting

### Data Not Updating
- Check internet connection
- Verify NASCAR API is accessible
- Check if race is active (API may return empty data during off-season)

### Browser Opens Slowly
- Increase timeout in `fetch_data()` function (currently set to 6 seconds)
- Consider using a different browser

### Stagnation Warning
- This appears when no vehicles are detected
- Common during pit stops, safety cars, or after race completion
- Indicates the API returned empty vehicle list

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 🎉 Credits

- **NASCAR API**: Official NASCAR data provider
- **Tailwind CSS**: Modern UI styling framework
- **Font Awesome**: Icon library
- **Google Fonts**: Inter and Roboto Mono typefaces

---

**Built with ❤️ for NASCAR racing fans**

*Last updated: May 2026*
