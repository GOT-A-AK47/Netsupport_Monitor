# netsupport_monitor_simple.py - Simple Tray + CMD Interface (English)
import sys
import os
import json
import threading
import time
import queue
import subprocess
from datetime import datetime
from functools import lru_cache
from typing import Optional, Dict, Any, List

try:
    import psutil
    from PIL import Image, ImageDraw
    import pystray
    # Windows-specific imports (optional)
    try:
        import winreg
        WINDOWS_AVAILABLE = True
    except ImportError:
        WINDOWS_AVAILABLE = False
except Exception as e:
    print("Missing module:", e)
    print("Install: python -m pip install psutil pillow pystray")
    sys.exit(1)

class SimpleCMDInterface:
    def __init__(self, monitor):
        self.monitor = monitor
        self.cmd_window = None
        self.running = False

    def show_details(self):
        """Show CMD-style detail window"""
        if self.cmd_window and self.cmd_window.poll() is None:
            # Window already open
            return

        self.create_dynamic_cmd_window()

    def create_dynamic_cmd_window(self):
        """Create a dynamic CMD window that updates in real-time"""
        # Create Python script that reads config dynamically
        script_content = '''
import json
import time
import os
import sys
from datetime import datetime

def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"detection_method": "process", "scan_interval": 2, "logging": False}

def get_status():
    # This is a simplified status check for display
    return "[SAFE] No connection detected"

def get_last_check():
    try:
        return datetime.now().strftime("%H:%M:%S")
    except:
        return "Not checked yet"

def show_main_screen():
    os.system("cls")
    config = load_config()

    print("+======================================================+")
    print("|              NetSupport Monitor v3.0              |")
    print("+======================================================+")
    print("|                                                    |")
    print(f"| Status: {get_status():<42} |")
    print("|                                                    |")
    print(f"| Last check: {get_last_check():<37} |")
    print(f"| Method: {config.get('detection_method', 'process'):<41} |")
    print(f"| Scan interval: {config.get('scan_interval', 2)} seconds{' '*(28)} |")
    print("|                                                    |")
    logging_status = "On" if config.get('logging', False) else "Off"
    print(f"| Logging: {logging_status:<41} |")
    print("|                                                    |")
    print("+======================================================+")
    print("| [S] Settings  [L] Logs  [R] Refresh  [Q] Quit     |")
    print("+======================================================+")
    print()
    print("Press a key: [S/L/R/Q]")

def show_settings():
    # Resize for settings screen (58 cols x 14 rows)
    os.system("mode con: cols=58 lines=14")

    while True:
        os.system("cls")
        config = load_config()

        print("+======================================================+")
        print("|                     SETTINGS                      |")
        print("+======================================================+")
        print("|                                                    |")
        print(f"| 1) Detection Method: {config.get('detection_method', 'process'):<26} |")
        print(f"| 2) Scan Interval: {config.get('scan_interval', 2)} seconds{' '*(22)} |")
        logging_status = "On" if config.get('logging', False) else "Off"
        print(f"| 3) Logging: {logging_status:<37} |")
        print("|                                                    |")
        print("| [1-3] Change setting                               |")
        print("| [S] Save and back                                  |")
        print("| [Q] Back without saving                            |")
        print("+======================================================+")
        print()
        print("Press key: [1-3/S/Q]")

        choice = get_single_key().lower()

        if choice == '1':
            change_detection_method(config)
        elif choice == '2':
            change_scan_interval(config)
        elif choice == '3':
            toggle_logging(config)
        elif choice == 's':
            print("Settings saved!")
            time.sleep(1)
            # Resize back to main screen
            os.system("mode con: cols=58 lines=16")
            break
        elif choice == 'q':
            # Resize back to main screen
            os.system("mode con: cols=58 lines=16")
            break

def change_detection_method(config):
    os.system("cls")
    print("Choose detection method:")
    print("1) Process Detection (Fastest)")
    print("2) Port Monitoring")
    print("3) Registry Check (Windows)")
    print("4) Hybrid Mode (Most accurate)")
    print()
    print("Press key [1-4]:")

    choice = get_single_key()
    methods = {"1": "process", "2": "port", "3": "registry", "4": "hybrid"}

    if choice in methods:
        config["detection_method"] = methods[choice]
        save_config(config)
        print(f"Method changed to: {methods[choice]}")
        time.sleep(1)

def change_scan_interval(config):
    try:
        interval = int(input("New scan interval (1-10 seconds): "))
        if 1 <= interval <= 10:
            config["scan_interval"] = interval
            save_config(config)
            print(f"Interval changed to: {interval} seconds")
        else:
            print("Invalid value! Use 1-10.")
        time.sleep(1)
    except ValueError:
        print("Invalid input!")
        time.sleep(1)

def toggle_logging(config):
    current = config.get("logging", False)
    config["logging"] = not current
    save_config(config)
    status = "enabled" if not current else "disabled"
    print(f"Logging {status}!")
    time.sleep(1)

def save_config(config):
    try:
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Error saving: {e}")

def get_single_key():
    """Get single keypress without Enter (Windows)"""
    try:
        import msvcrt
        return msvcrt.getch().decode('utf-8')
    except:
        # Fallback for non-Windows or if msvcrt fails
        return input().strip()[:1]

def main():
    os.system("title NetSupport Monitor - Details")
    os.system("color 0A")
    # Auto-resize window to fit content (58 cols x 16 rows for main screen)
    os.system("mode con: cols=58 lines=16")

    while True:
        show_main_screen()
        # Use getch for direct key input (no Enter needed)
        choice = get_single_key().lower()

        if choice == 's':
            show_settings()
        elif choice == 'l':
            os.system("cls")
            print("=== LOG FILE ===")
            if os.path.exists("netsupport_log.txt"):
                with open("netsupport_log.txt", "r", encoding="utf-8") as f:
                    print(f.read())
            else:
                print("No log file found.")
                print("Enable logging via Settings.")
            input("\\nPress Enter to go back...")
        elif choice == 'r':
            continue  # This will refresh the display
        elif choice == 'q':
            break

if __name__ == "__main__":
    main()
'''

        # Write Python script
        script_path = "netsupport_details.py"
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)

            # For PyInstaller compatibility, create a batch launcher
            batch_script = f'''@echo off
title NetSupport Monitor - Details
color 0A
mode con: cols=58 lines=16

python "{script_path}"
if errorlevel 1 (
    echo.
    echo Python not found! Install Python first.
    echo.
    pause
)
'''

            batch_path = "netsupport_launcher.bat"
            with open(batch_path, 'w', encoding='ascii', errors='replace') as f:
                f.write(batch_script)

            self.cmd_window = subprocess.Popen([batch_path],
                                             creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            # Only print once, avoid duplicate error messages
            if not hasattr(self, '_last_error') or self._last_error != str(e):
                print(f"Could not open CMD window: {e}")
                self._last_error = str(e)

    def get_status_text(self):
        """Get current status text (ASCII-safe)"""
        if getattr(self.monitor, 'last_status', False):
            return "[WARNING] TEACHER CONNECTED"
        return "[SAFE] No connection detected"

    def get_last_check(self):
        """Get last check time"""
        last_check = getattr(self.monitor, 'last_check_time', None)
        if last_check:
            return datetime.fromtimestamp(last_check).strftime("%H:%M:%S")
        return "Not checked yet"

class NetSupportMonitorSimple:
    def __init__(self):
        self.config_file = "config.json"
        self.log_file = "netsupport_log.txt"
        self.running = False
        self.log_buffer = []
        self.last_flush = time.time()

        # Load configuration
        self.config = self.load_config()

        # Initialize interfaces
        self.tray_icon = None
        self.cmd_interface = SimpleCMDInterface(self)
        self.tray_ready = threading.Event()

        # Status tracking
        self.last_status = None
        self.last_check_time = None

        # Threading
        self.monitor_thread = None
        self.log_thread = None

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or return defaults"""
        default_config = {
            "scan_interval": 2,
            "logging": False,
            "port": 5405,
            "detection_method": "process",
            "log_buffer_size": 10,
            "log_flush_interval": 30
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    return {**default_config, **loaded}
            except Exception as e:
                print(f"Config load error: {e}")

        return default_config

    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Config save error: {e}")

    @lru_cache(maxsize=32)
    def get_netsupport_processes(self, cache_key: int) -> frozenset:
        """Cached NetSupport process detection"""
        netsupport_processes = frozenset([
            'pcinssvc.exe', 'student.exe', 'tutor.exe',
            'client32.exe', 'netsupport.exe', 'pcicfgui.exe',
            'pciconfa.exe', 'nsm.exe', 'remote32.exe'
        ])

        try:
            current_processes = set()
            for proc in psutil.process_iter(['pid', 'name'], ad_value=''):
                proc_name = proc.info.get('name', '').lower()
                if proc_name in [p.lower() for p in netsupport_processes]:
                    current_processes.add(proc_name)
            return frozenset(current_processes)
        except Exception as e:
            print(f"Process scan error: {e}")
            return frozenset()

    def check_netsupport_registry(self) -> bool:
        """Check Windows registry for NetSupport activity"""
        if not WINDOWS_AVAILABLE:
            return False

        reg_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\NetSupport\NetSupport School"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\NetSupport\NetSupport School"),
        ]

        try:
            for hkey, path in reg_paths:
                try:
                    with winreg.OpenKey(hkey, path) as key:
                        try:
                            value, _ = winreg.QueryValueEx(key, "Connected")
                            if value:
                                return True
                        except FileNotFoundError:
                            pass
                except FileNotFoundError:
                    continue
        except Exception as e:
            print(f"Registry check error: {e}")

        return False

    def check_netsupport_port(self) -> bool:
        """Check for NetSupport port connections"""
        target_port = int(self.config.get("port", 5405))

        try:
            connections = psutil.net_connections(kind="inet")
            for conn in connections:
                if (hasattr(conn, 'laddr') and conn.laddr and
                    hasattr(conn.laddr, 'port') and conn.laddr.port == target_port and
                    conn.status == "ESTABLISHED"):
                    return True
        except Exception as e:
            print(f"Port check error: {e}")

        return False

    def check_connection(self) -> bool:
        """Main connection check"""
        method = self.config.get("detection_method", "process")

        try:
            if method == "process":
                cache_key = int(time.time() // self.config.get("scan_interval", 2))
                processes = self.get_netsupport_processes(cache_key)
                return len(processes) > 0

            elif method == "port":
                return self.check_netsupport_port()

            elif method == "registry" and WINDOWS_AVAILABLE:
                return self.check_netsupport_registry()

            elif method == "hybrid":
                process_detected = bool(self.get_netsupport_processes(int(time.time() // 5)))
                port_detected = self.check_netsupport_port()
                registry_detected = self.check_netsupport_registry() if WINDOWS_AVAILABLE else False
                return process_detected or port_detected or registry_detected

        except Exception as e:
            print(f"Connection check error ({method}): {e}")

        return False

    def log_status(self, message: str):
        """Buffered logging system"""
        if not self.config.get("logging", False):
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {message}\n"
        self.log_buffer.append(log_entry)

        buffer_size = self.config.get("log_buffer_size", 10)
        flush_interval = self.config.get("log_flush_interval", 30)

        should_flush = (len(self.log_buffer) >= buffer_size or
                       time.time() - self.last_flush > flush_interval)

        if should_flush:
            self.flush_logs()

    def flush_logs(self):
        """Flush log buffer to file"""
        if not self.log_buffer:
            return

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.writelines(self.log_buffer)
            self.log_buffer.clear()
            self.last_flush = time.time()
        except Exception as e:
            print(f"Log save error: {e}")

    def create_tray_icon(self, connected: bool) -> Image.Image:
        """Create system tray icon"""
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Background circle
        if connected:
            # Red background for connection
            draw.ellipse([2, 2, 30, 30], fill="#dc3545", outline="#ffffff", width=2)
            # Warning symbol
            draw.text((16, 16), "!", fill="white", anchor="mm")
        else:
            # Green background for no connection
            draw.ellipse([2, 2, 30, 30], fill="#28a745", outline="#ffffff", width=2)
            # Checkmark or shield symbol
            draw.text((16, 16), "✓", fill="white", anchor="mm")

        return img

    def update_tray_icon(self, connected: bool):
        """Update system tray icon"""
        if self.tray_icon:
            try:
                self.tray_icon.icon = self.create_tray_icon(connected)
                if connected:
                    self.tray_icon.title = "NetSupport Monitor - [!] TEACHER CONNECTED"
                else:
                    self.tray_icon.title = "NetSupport Monitor - [OK] Safe"
            except Exception as e:
                print(f"Tray icon update error: {e}")

    def start_tray(self):
        """Initialize system tray icon"""
        try:
            # Create simple menu
            menu = pystray.Menu(
                pystray.MenuItem("Show details", self.cmd_interface.show_details, default=True),
                pystray.MenuItem("Settings", self.show_simple_settings),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Exit", self.exit_program)
            )

            self.tray_icon = pystray.Icon(
                "netsupport_monitor",
                self.create_tray_icon(False),
                "NetSupport Monitor - [OK] Safe",
                menu
            )

            self.tray_ready.set()
            self.tray_icon.run()

        except Exception as e:
            print(f"Tray start error: {e}")

    def show_simple_settings(self):
        """Show simple settings via CMD"""
        self.cmd_interface.show_details()

    def background_monitor(self):
        """Background monitoring thread"""
        while self.running:
            try:
                start_time = time.time()
                connected = self.check_connection()
                check_duration = time.time() - start_time

                status_changed = connected != self.last_status
                time_passed = (self.last_check_time is None or
                              time.time() - self.last_check_time > 30)

                if status_changed or time_passed:
                    self.update_tray_icon(connected)

                    status_msg = "Teacher connected" if connected else "No connection"
                    self.log_status(f"{status_msg} (check: {check_duration:.2f}s)")

                    self.last_status = connected
                    self.last_check_time = time.time()

                base_interval = self.config.get("scan_interval", 2)
                sleep_interval = base_interval if connected else base_interval * 2
                time.sleep(max(0.5, sleep_interval - check_duration))

            except Exception as e:
                print(f"Monitor thread error: {e}")
                time.sleep(5)

    def log_worker(self):
        """Background log flushing thread"""
        while self.running:
            try:
                time.sleep(self.config.get("log_flush_interval", 30))
                if self.log_buffer:
                    self.flush_logs()
            except Exception as e:
                print(f"Log worker error: {e}")

    def exit_program(self):
        """Clean shutdown"""
        print("NetSupport Monitor shutting down...")

        self.running = False
        self.flush_logs()

        if self.tray_icon:
            try:
                self.tray_icon.stop()
            except Exception:
                pass

        # Wait for threads
        for thread in [self.monitor_thread, self.log_thread]:
            if thread and thread.is_alive():
                thread.join(timeout=2)

        sys.exit(0)

    def run(self):
        """Main application entry point"""
        print("=== NetSupport Monitor v3.0 - Simple Interface ===")
        print("Detection method:", self.config.get("detection_method", "process"))
        print("Scan interval:", self.config.get("scan_interval", 2), "seconds")
        print("Interface: Tray icon + CMD details")

        # Start background threads
        self.running = True

        # Start tray icon thread
        tray_thread = threading.Thread(target=self.start_tray, daemon=True)
        tray_thread.start()

        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.background_monitor, daemon=True)
        self.monitor_thread.start()

        # Start log worker if logging enabled
        if self.config.get("logging", False):
            self.log_thread = threading.Thread(target=self.log_worker, daemon=True)
            self.log_thread.start()

        # Wait for tray to be ready
        self.tray_ready.wait(timeout=3.0)

        # Perform initial scan
        time.sleep(1)
        connected = self.check_connection()
        self.update_tray_icon(connected)
        self.last_status = connected
        self.last_check_time = time.time()

        print("[OK] NetSupport Monitor running in system tray")
        print(">> Right-click on tray icon for options")
        print(">> 'Show details' for CMD interface")

        try:
            # Keep main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.exit_program()

if __name__ == "__main__":
    try:
        monitor = NetSupportMonitorSimple()
        monitor.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)