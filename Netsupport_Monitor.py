import psutil
import tkinter as tk
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading
import time

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
    """Creëert een icoon met de opgegeven kleur."""
    icon_size = (64, 64)
    img = Image.new('RGB', icon_size, color)
    draw = ImageDraw.Draw(img)
    draw.ellipse((10, 10, 54, 54), fill=color)
    return img

def update_status():
    """Updatet de UI en het tray-icoon op basis van de netwerkstatus."""
    global tray_icon
    while True:
        try:
            if check_netsupport_connection():
                status_label.config(text="Status: Verbonden", fg="red")
                tray_icon.icon = create_icon("red")
            else:
                status_label.config(text="Status: Geen verbinding", fg="green")
                tray_icon.icon = create_icon("green")
        except Exception as e:
            status_label.config(text=f"Status: Crash ({str(e)})", fg="black")
            tray_icon.icon = create_icon("black")
        time.sleep(2)

def show_window():
    """Toont het hoofdvenster."""
    root.deiconify()

def hide_window():
    """Verbergt het hoofdvenster."""
    root.withdraw()

def exit_program():
    """Beëindigt het programma correct."""
    tray_icon.stop()
    root.quit()

# UI Instellen
root = tk.Tk()
root.title("NetSupport Monitor")
root.geometry("300x100")
root.resizable(False, False)

status_label = tk.Label(root, text="Status: Controle...", font=("Arial", 12))
status_label.pack(pady=20)

exit_button = tk.Button(root, text="Afsluiten", command=exit_program)
exit_button.pack()

root.protocol("WM_DELETE_WINDOW", hide_window)

# Systeemtray-menu
menu = Menu(MenuItem("Toon Venster", show_window), MenuItem("Afsluiten", exit_program))
tray_icon = Icon("netsupport_monitor", create_icon("black"), menu=menu)

# Start de netwerkcontrole in een aparte thread
monitor_thread = threading.Thread(target=update_status, daemon=True)
monitor_thread.start()

# Start het systeemtray-icoon in een aparte thread
tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
tray_thread.start()

root.mainloop()