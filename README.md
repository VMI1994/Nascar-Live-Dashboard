![1](https://github.com/VMI1994/Nascar-Live-Dashboard/blob/main/kali.gif)

![2](https://github.com/VMI1994/Nascar-Live-Dashboard/blob/main/RaceDash.png)

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

- Download the appropriate binary executable file for your system(Windows, Ubuntu or Apple Silicone)
- Double click the executable to start
- The dashboard will automatically open in your browser at http://127.0.0.1:8448
- If you have difficulty running the program make sure you set the permissions as executable

## 🔧 Configuration

The dashboard runs on:
- **Port**: 8448
- **Host**: localhost (127.0.0.1)
- **Refresh Rate**: 2 seconds (auto-refresh)

## 🌐 Cross-Platform Support

RaceDash has been built and packaged for:
- ✅ **macOS** (Silicon/M1/M2)
- ✅ **Windows 10/11**
- ✅ **Ubuntu/Linux**

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
