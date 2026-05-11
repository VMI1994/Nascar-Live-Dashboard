from flask import Flask, render_template_string, jsonify
import requests
import time
from datetime import timedelta
from textwrap import dedent
import webbrowser

app = Flask(__name__)

URL = "https://cf.nascar.com/live/feeds/live-feed.json"
latest_data = None
last_fetch_time = 0

def fetch_data():
    global latest_data, last_fetch_time
    try:
        response = requests.get(URL, timeout=6)
        response.raise_for_status()
        latest_data = response.json()
        last_fetch_time = time.time()
        return latest_data
    except Exception:
        return None

HTML_TEMPLATE = dedent("""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RaceDash Live Race Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap');
        :root { --primary: #00ff9d; }
        * { transition-property: color, background-color, border-color, text-decoration-color, fill, stroke; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; }
        .dashboard-bg { background: linear-gradient(180deg, #0a0a0a 0%, #111111 100%); }
        .header-glow { text-shadow: 0 0 20px rgb(0 255 157); }
        .leader-row { background: linear-gradient(90deg, #1a3a1a, #112211) !important; font-weight: 600; }
        .flag-green { background-color: #00ff9d; color: #000; }
        .flag-yellow { background-color: #ffd700; color: #000; }
        .flag-red { background-color: #ff0033; color: white; }
        .flag-checkered { background: repeating-linear-gradient(45deg, #000, #000 10px, #fff 10px, #fff 20px); color: #000; font-weight: bold; }
    </style>
</head>
<body class="dashboard-bg text-white font-sans min-h-screen">
    <div class="max-w-screen-2xl mx-auto p-6">
        <!-- HEADER -->
        <div class="flex items-center justify-between mb-8 border-b border-white/10 pb-6">
            <div class="flex items-center gap-x-4">
                <div class="w-12 h-12 bg-emerald-500 rounded-2xl flex items-center justify-center text-3xl shadow-lg shadow-emerald-500/50">🏁</div>
                <div>
                    <h1 class="text-4xl font-bold tracking-tighter header-glow">RaceDash</h1>
                    <p class="text-emerald-400 text-lg -mt-1 font-medium">LIVE RACE DASHBOARD</p>
                </div>
            </div>

            <div id="race-status" class="flex items-center gap-x-8 bg-black/60 backdrop-blur-xl px-8 py-4 rounded-3xl border border-white/10 shadow-2xl text-xl font-medium">
                <!-- filled by JS -->
            </div>

            <div class="flex items-center gap-x-3">
                <div class="flex items-center gap-x-1.5 bg-black/70 px-4 h-9 rounded-2xl border border-white/10">
                    <div class="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
                    <span class="font-mono text-emerald-400" id="last-updated">Just now</span>
                </div>
                <button onclick="manualRefresh()" class="flex items-center gap-x-2 bg-white/10 hover:bg-white/20 px-5 h-9 rounded-2xl text-sm font-medium">
                    <i class="fa-solid fa-rotate"></i> REFRESH
                </button>
            </div>
        </div>

        <!-- RACE INFO CARDS -->
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8" id="race-info"></div>

        <!-- MAIN TABLE -->
        <div class="bg-[#111111] rounded-3xl shadow-2xl border border-white/10 overflow-hidden">
            <div class="px-8 py-5 border-b border-white/10 flex items-center justify-between bg-[#1a1a1a]">
                <div class="flex items-center gap-x-3">
                    <span class="text-emerald-400 font-medium">LIVE STANDINGS</span>
                    <span id="track-name-badge" class="px-3 py-1 text-xs font-mono bg-white/10 rounded-2xl"></span>
                </div>
                <div class="flex items-center gap-x-6 text-sm font-mono">
                    <div><span class="text-emerald-400">LAP</span> <span id="current-lap" class="font-semibold">200</span><span class="text-white/40">/200</span></div>
                    <div id="flag-pill" class="px-6 py-1 rounded-2xl text-black font-bold text-sm"></div>
                </div>
            </div>

            <div class="overflow-auto max-h-[calc(100vh-340px)]">
                <table class="w-full text-sm font-mono" id="standings-table">
                    <thead class="sticky top-0 bg-[#1f1f1f] text-white/70 text-xs">
                        <tr>
                            <th class="px-6 py-4 text-left">POS</th>
                            <th class="px-6 py-4 text-left">NO.</th>
                            <th class="px-6 py-4 text-left">DRIVER</th>
                            <th class="px-4 py-4">MFR</th>
                            <th class="px-4 py-4">START</th>
                            <th class="px-4 py-4">RUN</th>
                            <th class="px-4 py-4">STATUS</th>
                            <th class="px-6 py-4 text-right">LAPS</th>
                            <th class="px-6 py-4 text-right">DELTA</th>
                            <th class="px-6 py-4 text-right">LAST LAP</th>
                            <th class="px-6 py-4 text-right">SPEED</th>
                            <th class="px-6 py-4 text-right">BEST LAP</th>
                            <th class="px-6 py-4 text-right">SPEED</th>
                            <th class="px-6 py-4 text-right">AVG SPEED</th>
                            <th class="px-6 py-4 text-right">PASSES</th>
                            <th class="px-6 py-4 text-right">PASSED</th>
                            <th class="px-6 py-4 text-right">DIFF</th>
                            <th class="px-6 py-4 text-right">FASTEST</th>
                            <th class="px-6 py-4 text-right">LED</th>
                            <th class="px-6 py-4 text-center">ON TRACK</th>
                        </tr>
                    </thead>
                    <tbody id="table-body" class="divide-y divide-white/10 text-white/90"></tbody>
                </table>
            </div>
        </div>

        <div class="mt-6 text-xs text-white/40 font-mono flex justify-between">
            <div>Powered by NASCAR Live Feed • Auto-updates every 2 seconds</div>
            <div id="stagnation-warning" class="hidden text-amber-400 flex items-center gap-x-1">
                <i class="fa-solid fa-triangle-exclamation"></i>
                <span>DATA STAGNANT — Race may be under caution or finished</span>
            </div>
        </div>
    </div>

    <script>
        let dataCache = null;

        function renderDashboard(data) {
            if (!data) return;

            // Race status banner
            const statusHTML = `
                <div class="flex items-center gap-x-8">
                    <div><span class="text-white/60">Lap</span> <span class="font-bold text-3xl">${data.lap_number || 0}</span></div>
                    <div><span class="text-white/60">Elapsed</span> <span class="font-bold">${data.elapsed_time ? new Date(data.elapsed_time * 1000).toISOString().substr(11,8) : '—'}</span></div>
                    <div><span class="text-white/60">Laps to go</span> <span class="font-bold">${data.laps_to_go || 0}</span></div>
                    <div id="flag-pill-inner" class="px-6 py-2 rounded-3xl text-sm font-bold">FLAG STATE ${data.flag_state || ''}</div>
                </div>`;
            document.getElementById('race-status').innerHTML = statusHTML;

            // Flag styling
            const flagEl = document.getElementById('flag-pill-inner');
            if (data.flag_state === 9) flagEl.className = 'flag-checkered px-6 py-2 rounded-3xl text-sm font-bold';
            else if (data.flag_state === 1) flagEl.className = 'flag-green px-6 py-2 rounded-3xl text-sm font-bold';
            else if (data.flag_state === 2) flagEl.className = 'flag-yellow px-6 py-2 rounded-3xl text-sm font-bold';
            else flagEl.className = 'bg-white/10 px-6 py-2 rounded-3xl text-sm font-bold';

            // Race info cards - special handling for time_of_day_os
            const infoContainer = document.getElementById('race-info');
            infoContainer.innerHTML = '';
            const keysToShow = ['run_name', 'track_name', 'series_id', 'time_of_day_os', 'number_of_lead_changes', 'number_of_leaders'];
            
            keysToShow.forEach(key => {
                if (data[key] !== undefined) {
                    let label = key.replace('_', ' ').toUpperCase();
                    let value = data[key];

                    // Convert time_of_day_os to clean LOCAL time (no date, no UTC)
                    if (key === 'time_of_day_os') {
                        const date = new Date(data[key]);
                        value = date.toLocaleTimeString([], { 
                            hour: '2-digit', 
                            minute: '2-digit', 
                            second: '2-digit',
                            hour12: false 
                        });
                        label = 'LOCAL TIME';
                    }

                    const card = document.createElement('div');
                    card.className = 'stat-card bg-white/5 border border-white/10 rounded-3xl p-4 hover:shadow-emerald-500/30';
                    card.innerHTML = `
                        <div class="text-xs text-white/60 uppercase tracking-widest">${label}</div>
                        <div class="text-2xl font-semibold mt-1 font-mono">${value}</div>`;
                    infoContainer.appendChild(card);
                }
            });

            // Table
            const tbody = document.getElementById('table-body');
            tbody.innerHTML = '';

            const vehicles = data.vehicles || [];
            vehicles.forEach((v, idx) => {
                const driver = v.driver || {};
                const lapsLedCount = (v.laps_led || []).reduce((acc, p) => acc + (p.end_lap - p.start_lap + 1), 0);
                const delta = v.delta !== undefined ? (v.delta === 0 ? '—' : v.delta.toFixed(3)) : '—';

                const row = document.createElement('tr');
                if (idx === 0) row.classList.add('leader-row');
                row.innerHTML = `
                    <td class="px-6 py-4">${idx + 1}</td>
                    <td class="px-6 py-4 font-bold">${v.vehicle_number || '—'}</td>
                    <td class="px-6 py-4">${driver.full_name || '—'}</td>
                    <td class="px-4 py-4 text-center">${v.vehicle_manufacturer || '—'}</td>
                    <td class="px-4 py-4 text-center">${v.starting_position || '—'}</td>
                    <td class="px-4 py-4 text-center">${v.running_position || idx + 1}</td>
                    <td class="px-4 py-4 text-center">${v.status || '—'}</td>
                    <td class="px-6 py-4 text-right">${v.laps_completed || 0}</td>
                    <td class="px-6 py-4 text-right font-medium">${delta}</td>
                    <td class="px-6 py-4 text-right">${(v.last_lap_time || 0).toFixed(3)}</td>
                    <td class="px-6 py-4 text-right">${(v.last_lap_speed || 0).toFixed(3)}</td>
                    <td class="px-6 py-4 text-right">${(v.best_lap_time || 0).toFixed(3)}</td>
                    <td class="px-6 py-4 text-right">${(v.best_lap_speed || 0).toFixed(3)}</td>
                    <td class="px-6 py-4 text-right">${(v.average_speed || 0).toFixed(3)}</td>
                    <td class="px-6 py-4 text-right">${v.passes_made || 0}</td>
                    <td class="px-6 py-4 text-right">${v.times_passed || 0}</td>
                    <td class="px-6 py-4 text-right">${v.passing_differential || 0}</td>
                    <td class="px-6 py-4 text-right">${v.fastest_laps_run || 0}</td>
                    <td class="px-6 py-4 text-right">${lapsLedCount}</td>
                    <td class="px-6 py-4 text-center">${v.is_on_track ? '✅' : '❌'}</td>`;
                tbody.appendChild(row);
            });

            // Update track name and lap info
            document.getElementById('track-name-badge').textContent = data.track_name || '';
            document.getElementById('current-lap').textContent = data.lap_number || 0;

            // Stagnation warning
            const stagnant = document.getElementById('stagnation-warning');
            if (!vehicles.length) {
                stagnant.classList.remove('hidden');
            } else {
                stagnant.classList.add('hidden');
            }
        }

        function manualRefresh() {
            fetch('/api/live')
                .then(r => r.json())
                .then(d => {
                    dataCache = d;
                    renderDashboard(d);
                    document.getElementById('last-updated').textContent = 'Just now';
                });
        }

        // Auto-refresh every 2 seconds
        setInterval(() => {
            fetch('/api/live')
                .then(r => r.json())
                .then(d => {
                    dataCache = d;
                    renderDashboard(d);
                    document.getElementById('last-updated').textContent = 'Just now';
                });
        }, 2000);

        // Initial load
        fetch('/api/live').then(r => r.json()).then(d => renderDashboard(d));
    </script>
</body>
</html>
""")

@app.route("/")
def dashboard():
    global latest_data
    if not latest_data or time.time() - last_fetch_time > 30:
        fetch_data()
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/live")
def api_live():
    fetch_data()
    return jsonify(latest_data if latest_data else {"error": "No data available"})

if __name__ == "__main__":
    print("🚀 RaceDash web dashboard starting...")
    print("   Open this link in your browser → http://127.0.0.1:8448")
    print("   (Now showing clean LOCAL TIME in the info cards)")
    webbrowser.open('http://127.0.0.1:8448')
    app.run(debug=False, port=8448)
    webbrowser.open('http://127.0.0.1:8448')
