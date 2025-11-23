import tkinter as tk
from datetime import datetime, timedelta
import json
import os

# ============================================================
# DEV MODE CONFIG
# ============================================================

DEV_MODE = False        # Simulated time/day enabled
DEV_TIME = "15:30"     # Simulated time HH:MM
DEV_DAY = "MON"        # Simulated weekday ("MON"…"SUN")

def get_now():
    """Returns simulated time when DEV_MODE=True, otherwise system time."""
    if DEV_MODE:
        hour, minute = map(int, DEV_TIME.split(":"))
        today = datetime.now().date()
        return datetime.combine(today, datetime.min.time()).replace(
            hour=hour, minute=minute
        )
    return datetime.now()


# ============================================================
# JSON LOADING
# ============================================================

ROUTE_DIR = "routes"

def load_route_file(route_name):
    """Loads route JSON: routes/x4.json"""
    path = os.path.join(ROUTE_DIR, f"{route_name.lower()}.json")
    with open(path, "r") as f:
        return json.load(f)


def get_available_routes():
    """Find all JSON route files in routes folder."""
    files = os.listdir(ROUTE_DIR)
    routes = [f.split(".")[0].upper() for f in files if f.endswith(".json")]
    return sorted(routes)


# ============================================================
# DAY LOGIC
# ============================================================

DAY_MAP = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

def get_day_key():
    """Returns JSON day key like: mon/tue/sat/sun"""
    if DEV_MODE:
        return DEV_DAY.lower()

    dow = datetime.today().weekday()
    return DAY_MAP[dow]


# ============================================================
# EXTRACT DEPARTURES
# ============================================================

MAX_LINES = 3
MAX_WAIT_MIN = 120

def get_upcoming(route_data, direction):
    """Returns list of (dest, mins, time_str) for the direction."""
    day = get_day_key()
    times = route_data[direction][day]["times"]
    dests = route_data[direction][day]["dests"]

    now = get_now()
    today = now.date()

    result = []

    for t_str, dest in zip(times, dests):
        hour, minute = map(int, t_str.split(":"))

        dep_time = datetime.combine(today, datetime.min.time()).replace(
            hour=hour, minute=minute
        )
        if dep_time < now:
            dep_time += timedelta(days=1)

        mins = int((dep_time - now).total_seconds() // 60)

        if mins <= MAX_WAIT_MIN:
            result.append((dest, mins, t_str))

    result.sort(key=lambda x: x[1])
    return result[:MAX_LINES]


# ============================================================
# GUI CLASS
# ============================================================

class MultiRouteDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Stop Display – Multi Route")

        self.canvas = tk.Canvas(root, width=900, height=500, bg="black")
        self.canvas.pack()

        self.colour = "#ffcc00"
        self.header_font = ("Helvetica", 18, "bold")
        self.row_font = ("Helvetica", 16, "bold")

        # Route selector
        self.routes = get_available_routes()
        self.selected_route = tk.StringVar(value=self.routes[0])

        dropdown = tk.OptionMenu(root, self.selected_route, *self.routes, command=self.change_route)
        dropdown.pack()

        self.route_data = load_route_file(self.selected_route.get())

        self.update()

    def change_route(self, _):
        """Reload route when dropdown changes."""
        self.route_data = load_route_file(self.selected_route.get())

    def draw_panel(self, x, y, title, entries):
        self.canvas.create_text(
            x, y, text=title, fill=self.colour, font=self.header_font, anchor="w"
        )
        row_y = y + 40

        for idx, (dest, mins, t_str) in enumerate(entries, start=1):
            line = f"{idx} | {dest} | {mins} mins | {t_str}"
            self.canvas.create_text(
                x, row_y, text=line, fill=self.colour, font=self.row_font, anchor="w"
            )
            row_y += 30

    def update(self):
        self.canvas.delete("all")

        # ============================================================
        # BANNER
        # ============================================================
        if DEV_MODE:
            banner = f"DEV MODE — SIM TIME {DEV_TIME} — DAY {DEV_DAY}"
            colour = "#ff5555"
        else:
            banner = f"CURRENT TIME — {datetime.now().strftime('%H:%M:%S')}"
            colour = "#55ff55"

        self.canvas.create_text(
            450, 25, text=banner,
            fill=colour, font=("Helvetica", 14, "bold"), anchor="center"
        )

        # ============================================================
        # RENDER BOTH DIRECTIONS
        # ============================================================

        rt = self.route_data["route"]

        up_south = get_upcoming(self.route_data, "southampton")
        up_port = get_upcoming(self.route_data, "portsmouth")

        self.draw_panel(50, 80, f"{rt} to Portsmouth:", up_port)
        self.draw_panel(450, 80, f"{rt} to Southampton:", up_south)

        # Refresh every minute
        self.root.after(60_000, self.update)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiRouteDisplay(root)
    root.mainloop()
