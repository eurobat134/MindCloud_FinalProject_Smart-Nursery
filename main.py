import tkinter as tk
from ESP32_COM import ESP32Com

ESP32_COM = ESP32Com()
ESP32_COM.send_telegram_message("Test message from Smart Nursery Guardian!")
ESP32_COM.start()   # runs the socket loop in a background thread

# -------------------- Colors --------------------
BG = "#0b0f19"
CARD_BG = "#111827"
BORDER = "#1f2937"
TEXT = "#f3f4f6"
MUTED = "#9ca3af"

GREEN = "#22c55e"
YELLOW = "#f59e0b"
RED = "#ef4444"
BLUE = "#38bdf8"
PURPLE = "#a78bfa"

# Main Window
window = tk.Tk()

window.title("Smart Nursery")
window.geometry("1100x750")
window.minsize(800, 600)
window.configure(bg=BG)

# Header
header = tk.Frame(
    window,
    bg=BG
)

header.pack(
    fill="x",
    pady=(25, 20)
)

title = tk.Label(
    header,
    text="Smart Nursery",
    font=("Arial", 30, "bold"),
    fg="white",
    bg=BG
)

title.pack()

subtitle = tk.Label(
    header,
    text="Real-Time Baby Monitoring System",
    font=("Arial", 12),
    fg=MUTED,
    bg=BG
)

subtitle.pack(pady=(5, 0))

# Dashboard Container
dashboard = tk.Frame(
    window,
    bg=BG
)

dashboard.pack(
    fill="both",
    expand=True,
    padx=30
)

# Make 3 columns equal width
for column in range(3):
    dashboard.columnconfigure(column, weight=1)

for row in range(5):
    dashboard.rowconfigure(row, weight=1)

# Card Function
def create_card(parent, row, column, title_text, icon,
                columnspan=1):

    card = tk.Frame(
        parent,
        bg=CARD_BG,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    card.grid(
        row=row,
        column=column,
        columnspan=columnspan,
        sticky="nsew",
        padx=8,
        pady=8
    )

    # Internal padding
    content = tk.Frame(
        card,
        bg=CARD_BG
    )

    content.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )

    # Icon
    icon_label = tk.Label(
        content,
        text=icon,
        font=("Arial", 25),
        fg=TEXT,
        bg=CARD_BG
    )

    icon_label.pack(
        anchor="w"
    )

    # Card title
    title_label = tk.Label(
        content,
        text=title_text.upper(),
        font=("Arial", 10),
        fg=MUTED,
        bg=CARD_BG
    )

    title_label.pack(
        anchor="w",
        pady=(5, 5)
    )

    # Value
    value_label = tk.Label(
        content,
        text="Unknown",
        font=("Arial", 21, "bold"),
        fg=TEXT,
        bg=CARD_BG
    )

    value_label.pack(
        anchor="w"
    )

    return value_label

# Cards
# Baby
baby_state = create_card(
    dashboard,
    0,
    0,
    "Baby",
    "👶"
)

# Cry status
cry_state = create_card(
    dashboard,
    0,
    1,
    "Status",
    "🔊"
)

# Room
room_state = create_card(
    dashboard,
    0,
    2,
    "Room",
    "🏠"
)

# Light
light_state = create_card(
    dashboard,
    1,
    0,
    "Room Light",
    "💡"
)

# Temperature
temperature_card = tk.Frame(
    dashboard,
    bg=CARD_BG,
    highlightbackground=BORDER,
    highlightthickness=1
)

temperature_card.grid(
    row=1,
    column=1,
    columnspan=2,
    sticky="nsew",
    padx=8,
    pady=8
)

temperature_content = tk.Frame(
    temperature_card,
    bg=CARD_BG
)

temperature_content.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)

tk.Label(
    temperature_content,
    text="🌡️",
    font=("Arial", 25),
    fg=TEXT,
    bg=CARD_BG
).pack(anchor="w")

tk.Label(
    temperature_content,
    text="TEMPERATURE",
    font=("Arial", 10),
    fg=MUTED,
    bg=CARD_BG
).pack(anchor="w")

temperature = tk.Label(
    temperature_content,
    text="0 °C",
    font=("Arial", 32, "bold"),
    fg=TEXT,
    bg=CARD_BG
)

temperature.pack(anchor="w")


# Fan
fan_state = create_card(
    dashboard,
    2,
    0,
    "Fan",
    "🌀"
)

# Gas
gas_state = create_card(
    dashboard,
    2,
    1,
    "Gas / Smoke",
    "⚠️"
)

# Buzzer
buzzer_state = create_card(
    dashboard,
    2,
    2,
    "Alert",
    "🔔"
)

# Servo
servo_state = create_card(
    dashboard,
    3,
    0,
    "Crib",
    "⚙️"
)

# AI Card
ai_card = tk.Frame(
    dashboard,
    bg="#17132b",
    highlightbackground=BORDER,
    highlightthickness=1
)

ai_card.grid(
    row=3,
    column=1,
    columnspan=2,
    sticky="nsew",
    padx=8,
    pady=8
)

ai_content = tk.Frame(
    ai_card,
    bg="#17132b"
)

ai_content.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)

tk.Label(
    ai_content,
    text="🧠",
    font=("Arial", 25),
    fg=TEXT,
    bg="#17132b"
).pack(anchor="w")

tk.Label(
    ai_content,
    text="AI CRY CLASSIFICATION",
    font=("Arial", 10),
    fg=MUTED,
    bg="#17132b"
).pack(anchor="w")

ai_state = tk.Label(
    ai_content,
    text="None",
    font=("Arial", 25, "bold"),
    fg=PURPLE,
    bg="#17132b"
)

ai_state.pack(
    anchor="w",
    pady=(5, 0)
)

# Update Dashboard
def update_dashboard(data):
    # ---------------- Baby ----------------
    if data["babyAwake"]:
        baby_state.config(
            text="Awake",
            fg=BLUE
        )
    else:
        baby_state.config(
            text="Sleeping",
            fg=GREEN
        )

    # ---------------- Cry ----------------
    if data["cry"]:
        cry_state.config(
            text="Crying",
            fg=RED
        )
    else:
        cry_state.config(
            text="Quiet",
            fg=GREEN
        )

    # ---------------- Room ----------------
    if data["dark"]:
        room_state.config(
            text="Dark",
            fg=YELLOW
        )
    else:
        room_state.config(
            text="Bright",
            fg=BLUE
        )

    # ---------------- Light ----------------
    if data["light"]:
        light_state.config(
            text="ON",
            fg=YELLOW
        )
    else:
        light_state.config(
            text="OFF",
            fg=MUTED
        )

    # ---------------- Temperature ----------------
    temperature.config(
        text=f'{data["temperature"]} °C'
    )

    # ---------------- Fan ----------------
    fan_state.config(
        text=f'{data["fan"]}%'
    )

    # ---------------- Gas ----------------
    if data["gas"]:

        gas_state.config(
            text="DANGER",
            fg=RED
        )

    else:

        gas_state.config(
            text="Safe",
            fg=GREEN
        )

    # ---------------- Buzzer ----------------
    if data["buzzer"]:

        buzzer_state.config(
            text="ON",
            fg=RED
        )

    else:

        buzzer_state.config(
            text="OFF",
            fg=MUTED
        )

    # ---------------- Servo ----------------
    if data["servo"]:

        servo_state.config(
            text="Rocking",
            fg=BLUE
        )

    else:

        servo_state.config(
            text="Stopped",
            fg=MUTED
        )

    # ---------------- AI ----------------
    if data["classification"] == '0':
        ai_state.config(
            text="Hungry",
            fg=RED
        )
    elif data["classification"] == '1':
        ai_state.config(
            text="Tired",
            fg=YELLOW
        )
    elif data["classification"] == '2':
        ai_state.config(
            text="Discomfort",
            fg=BLUE
        )
    else:
        ai_state.config(
            text="None",
            fg=MUTED
    )

# Footer
footer = tk.Frame(
    window,
    bg=BG
)

footer.pack(
    fill="x",
    pady=(10, 20)
)

separator = tk.Frame(
    footer,
    height=1,
    bg=BORDER
)

separator.pack(
    fill="x",
    padx=30
)

tk.Label(
    footer,
    text="Smart Nursery • Team 10",
    font=("Arial", 10),
    fg="#6b7280",
    bg=BG
).pack(
    pady=(10, 0)
)

def refresh_dashboard():
    data = {
        "babyAwake": ESP32_COM.get_classification() != '3',
        "cry": ESP32_COM.get_classification() != '3',
        "dark": ESP32_COM.dark,
        "light": ESP32_COM.light,
        "temperature": ESP32_COM.temperature,
        "fan": ESP32_COM.fan,
        "gas": ESP32_COM.gas_state,
        "buzzer": ESP32_COM.buzzer_state,
        "servo": ESP32_COM.servo_state,
        "classification": ESP32_COM.get_classification()
    }
    update_dashboard(data)
    window.after(500, refresh_dashboard)  # poll every 500ms

# Initial + recurring update
refresh_dashboard()

# Start GUI
window.mainloop()