import psutil
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw
import threading
import time
import sys
import pystray
from datetime import datetime

NETSUPPORT_PORT = 5405

def check_netsupport_connection():
    """Controleert of er een actieve NetSupport-verbinding is op poort 5405."""
    try:
        connections = psutil.net_connections(kind="inet")
        for conn in connections:
            if conn.laddr.port == NETSUPPORT_PORT and conn.status == "ESTABLISHED":
                return True
    except Exception as e:
        print(f"Fout bij netwerkcontrole: {e}")
    return False

def create_icon(color):
    """Creëert een afbeelding voor het tray-icoon."""
    icon_size = (32, 32)
    img = Image.new('RGB', icon_size, 'white')
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 28, 28], fill=color)
    return img

def update_status():
    """Updatet de UI en tray-icon status op basis van de netwerkstatus."""
    while True:
        try:
            connection_status = check_netsupport_connection()
            last_checked = datetime.now().strftime('%H:%M:%S')
            
            if connection_status:
                root.after(0, lambda: status_label.config(text="Status: Verbonden", fg="red"))
                root.after(0, lambda: last_check_label.config(text=f"Laatste controle: {last_checked}"))
                tray_icon.icon = red_icon
                tray_icon.title = "NetSupport: Verbonden"
            else:
                root.after(0, lambda: status_label.config(text="Status: Geen verbinding", fg="green"))
                root.after(0, lambda: last_check_label.config(text=f"Laatste controle: {last_checked}"))
                tray_icon.icon = green_icon
                tray_icon.title = "NetSupport: Geen verbinding"
        except Exception as e:
            root.after(0, lambda: status_label.config(text=f"Status: Crash ({str(e)})", fg="black"))
            tray_icon.icon = black_icon
            tray_icon.title = "NetSupport: Crash"
        time.sleep(2)

def manual_refresh():
    """Handmatige update van de status."""
    connection_status = check_netsupport_connection()
    last_checked = datetime.now().strftime('%H:%M:%S')
    
    if connection_status:
        status_label.config(text="Status: Verbonden", fg="red")
        tray_icon.icon = red_icon
        tray_icon.title = "NetSupport: Verbonden"
    else:
        status_label.config(text="Status: Geen verbinding", fg="green")
        tray_icon.icon = green_icon
        tray_icon.title = "NetSupport: Geen verbinding"
    
    last_check_label.config(text=f"Laatste controle: {last_checked}")

def open_settings():
    """Placeholder functie voor instellingen menu."""
    settings_window = tk.Toplevel(root)
    settings_window.title("Instellingen")
    settings_window.geometry("250x150")
    tk.Label(settings_window, text="Instellingen komen hier.").pack(pady=20)

def exit_program(icon, item):
    """Beëindigt het programma correct."""
    tray_icon.stop()
    root.quit()
    sys.exit()

def show_window(icon, item):
    """Toont het UI-venster."""
    root.after(0, root.deiconify)

def hide_window():
    """Verbergt het UI-venster."""
    root.withdraw()

# UI Instellen
root = tk.Tk()
root.title("NetSupport Monitor")
root.geometry("350x200")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", hide_window)  # Sluit naar tray

frame = ttk.Frame(root, padding=10)
frame.pack(fill='both', expand=True)

status_label = tk.Label(frame, text="Status: Controle...", font=("Arial", 12))
status_label.pack(pady=5)

last_check_label = tk.Label(frame, text="Laatste controle: -", font=("Arial", 10))
last_check_label.pack(pady=5)

button_frame = ttk.Frame(frame)
button_frame.pack(pady=10)

refresh_button = ttk.Button(button_frame, text="Vernieuwen", command=manual_refresh)
refresh_button.grid(row=0, column=0, padx=5)

settings_button = ttk.Button(button_frame, text="Instellingen", command=open_settings)
settings_button.grid(row=0, column=1, padx=5)

exit_button = ttk.Button(frame, text="Afsluiten", command=lambda: exit_program(None, None))
exit_button.pack(pady=10)

# Icoon afbeeldingen laden
green_icon = create_icon("green")
red_icon = create_icon("red")
black_icon = create_icon("black")

# Systeemtray instellen
menu = pystray.Menu(
    pystray.MenuItem("Toon Venster", show_window),
    pystray.MenuItem("Afsluiten", exit_program)
)
tray_icon = pystray.Icon("NetSupport Monitor", green_icon, "NetSupport Monitor", menu)

# Start de netwerkcontrole in een aparte thread
monitor_thread = threading.Thread(target=update_status, daemon=True)
monitor_thread.start()

# Start tray in een aparte thread
tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
tray_thread.start()

root.mainloop()
