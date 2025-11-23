<p align="center">

  <!-- Version Badge -->
  <img src="https://img.shields.io/badge/version-1.1-blue?style=for-the-badge" alt="Version">

  <!-- Python Badge -->
  <img src="https://img.shields.io/badge/python-3.10%2B-success?style=for-the-badge" alt="Python">

  <!-- Status Badge -->
  <img src="https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge" alt="Status">

  <!-- Platform Badge -->
  <img src="https://img.shields.io/badge/platform-windows%20%7C%20linux-lightgrey?style=for-the-badge" alt="Platform">

  <!-- License Badge -->
  <img src="https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge" alt="License">

  <!-- Project Type -->
  <img src="https://img.shields.io/badge/type-transport%20display-orange?style=for-the-badge" alt="Type">

</p>


# Bus Stop Display System
A real-time countdown display for bus services, built with Tkinter and structured around JSON timetable data.  
Supports multiple routes, dual-direction displays, simulated time/day, and dynamic JSON loading.

---

## 🚏 Features

### 🟩 Core Functionality
- Dual-direction bus departure board  
- Real-time countdown to next departures  
- Filters out departures >120 minutes away  
- Automatic refresh every minute  
- Two independent panels per route (e.g., *To Portsmouth*, *To Southampton*)

---

### 🟦 JSON Route System (v1.1+)
Each route lives in its own JSON file:

```
routes/
    x4.json
    x5.json
    x7.json
```

Each file defines:
- Route name  
- All directions (e.g. southampton, portsmouth)  
- 7-day timetable (mon–sun)  
- Times + destination names  

---

### 🟥 DEV Mode
Designed for simulation, debugging, and timetable testing.

- `DEV_MODE`: enables simulated clock  
- `DEV_TIME="HH:MM"`: inject a fake current time  
- `DEV_DAY="MON"`: force a specific weekday  
- On-screen red banner showing DEV status  

---

### 🟧 Real-Time Mode
When DEV MODE is disabled:
- Green “CURRENT TIME” banner displayed  
- Uses system time & actual weekday  

---

### 📁 Folder Structure
```
project/
│ main.py
│ README.md
│
└── routes/
    ├── x4.json
    ├── x5.json
    └── …
```

---

## ⚙️ Installation

1. Install Python 3.10+
2. Clone the repository
3. Install any fonts (optional)
4. Run:

```bash
python main.py
```

---

## 📜 JSON Format Example

Example `routes/x4.json`:

```json
{
  "route": "X4",
  "southampton": {
      "mon": { "times": ["06:43", "07:24"], "dests": ["Southampton", "Southampton"] },
      "tue": { "times": ["06:43", "07:24"], "dests": ["Southampton", "Southampton"] },
      "sun": { "times": ["07:37", "08:37"], "dests": ["Southampton", "Southampton"] }
  },
  "portsmouth": {
      "mon": { "times": ["08:14", "08:59"], "dests": ["Portsmouth", "Portsmouth"] },
      "sun": { "times": ["07:46", "08:37"], "dests": ["Portsmouth", "Portsmouth"] }
  }
}
```

---

## 🧭 Upcoming Versions
V1.2 - **Coming soon.**

---

## 🪖 Maintainer
NX.RTEZ, team of 1.
