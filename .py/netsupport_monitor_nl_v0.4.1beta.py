# netsupport_monitor_simple.py - Simpele Tray + CMD Interface (Nederlands)
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
    print("Ontbrekende module:", e)
    print("Installeer: python -m pip install psutil pillow pystray")
    sys.exit(1)

class SimpleCMDInterface:
    def __init__(self, monitor):
        self.monitor = monitor
        self.cmd_window = None
        self.running = False
        self.status_file = "netsupport_status.json"

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
    """Load configuration with improved error handling"""
    default_config = {
        "detection_method": "process",
        "scan_interval": 2,
        "logging": False,
        "auto_start": False,
        "silent_mode": False,
        "show_notifications": True,
        "network_adapter": "all"
    }
    try:
        if not os.path.exists("config.json"):
            return default_config
        with open("config.json", "r", encoding="utf-8") as f:
            loaded = json.load(f)
            # Merge with defaults to ensure all keys exist
            return {**default_config, **loaded}
    except json.JSONDecodeError as e:
        print(f"Config file corrupted: {e}")
        return default_config
    except Exception as e:
        print(f"Error loading config: {e}")
        return default_config

def load_status():
    """Load real-time status from shared status file"""
    default_status = {"connected": False, "last_check": None, "method_used": "unknown"}
    try:
        if not os.path.exists("netsupport_status.json"):
            return default_status
        with open("netsupport_status.json", "r", encoding="utf-8") as f:
            loaded = json.load(f)
            return {**default_status, **loaded}
    except json.JSONDecodeError:
        return default_status
    except Exception:
        return default_status

def get_status():
    """Get real-time status from monitor"""
    status = load_status()
    if status.get("connected", False):
        return "[WAARSCHUWING] LEERKRACHT VERBONDEN"
    return "[VEILIG] Geen verbinding gedetecteerd"

def get_last_check():
    """Get last check time from status file"""
    status = load_status()
    last_check = status.get("last_check")
    if last_check:
        try:
            return datetime.fromtimestamp(last_check).strftime("%H:%M:%S")
        except:
            pass
    return "Nog niet gecontroleerd"

def show_main_screen():
    os.system("cls")
    config = load_config()

    print("+======================================================+")
    print("|              NetSupport Monitor v0.4.1             |")
    print("+======================================================+")
    print("|                                                    |")
    print(f"| Status: {get_status():<42} |")
    print("|                                                    |")
    print(f"| Laatste controle: {get_last_check():<31} |")
    print(f"| Methode: {config.get('detection_method', 'process'):<38} |")
    print(f"| Scan interval: {config.get('scan_interval', 2)} seconden{' '*(29)} |")
    print("|                                                    |")
    logging_status = "Aan" if config.get('logging', False) else "Uit"
    print(f"| Logboek: {logging_status:<39} |")
    print("|                                                    |")
    print("+======================================================+")
    print("| [S] Instellingen [L] Logs [R] Ververs [Q] Afsluiten |")
    print("+======================================================+")
    print()
    print("Druk op een toets: [S/L/R/Q]")

def show_settings():
    # Resize for settings screen (58 cols x 14 rows)
    os.system("mode con: cols=58 lines=14")

    while True:
        os.system("cls")
        config = load_config()

        print("+======================================================+")
        print("|                   INSTELLINGEN                     |")
        print("+======================================================+")
        print("|                                                    |")
        print(f"| 1) Detectiemethode: {config.get('detection_method', 'process'):<27} |")
        print(f"| 2) Scan Interval: {config.get('scan_interval', 2)} seconden{' '*(21)} |")
        logging_status = "Aan" if config.get('logging', False) else "Uit"
        print(f"| 3) Logboek: {logging_status:<36} |")
        print("|                                                    |")
        print("| [1-3] Wijzig instelling                           |")
        print("| [S] Opslaan en terug                              |")
        print("| [Q] Terug zonder opslaan                          |")
        print("+======================================================+")
        print()
        print("Druk op toets: [1-3/S/Q]")

        choice = get_single_key().lower()

        if choice == '1':
            change_detection_method(config)
        elif choice == '2':
            change_scan_interval(config)
        elif choice == '3':
            toggle_logging(config)
        elif choice == 's':
            print("Instellingen opgeslagen!")
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
    print("Kies detectiemethode:")
    print("1) Process Detection (Snelst)")
    print("2) Port Monitoring")
    print("3) Registry Check (Windows)")
    print("4) Hybrid Mode (Meest accuraat)")
    print()
    print("Druk op toets [1-4]:")

    choice = get_single_key()
    methods = {"1": "process", "2": "port", "3": "registry", "4": "hybrid"}

    if choice in methods:
        config["detection_method"] = methods[choice]
        save_config(config)
        print(f"Methode gewijzigd naar: {methods[choice]}")
        time.sleep(1)

def change_scan_interval(config):
    try:
        interval = int(input("Nieuwe scan interval (1-10 seconden): "))
        if 1 <= interval <= 10:
            config["scan_interval"] = interval
            save_config(config)
            print(f"Interval gewijzigd naar: {interval} seconden")
        else:
            print("Ongeldige waarde! Gebruik 1-10.")
        time.sleep(1)
    except ValueError:
        print("Ongeldige invoer!")
        time.sleep(1)

def toggle_logging(config):
    current = config.get("logging", False)
    config["logging"] = not current
    save_config(config)
    status = "ingeschakeld" if not current else "uitgeschakeld"
    print(f"Logging {status}!")
    time.sleep(1)

def save_config(config):
    try:
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Fout bij opslaan: {e}")

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
            print("=== LOGBOEK ===")
            if os.path.exists("netsupport_log.txt"):
                with open("netsupport_log.txt", "r", encoding="utf-8") as f:
                    print(f.read())
            else:
                print("Geen logboek gevonden.")
                print("Schakel logboek in via Instellingen.")
            input("\\nDruk op Enter om terug te gaan...")
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
    echo Python niet gevonden! Installeer Python eerst.
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
            return "[WAARSCHUWING] LEERKRACHT VERBONDEN"
        return "[VEILIG] Geen verbinding"

    def get_last_check(self):
        """Get last check time"""
        last_check = getattr(self.monitor, 'last_check_time', None)
        if last_check:
            return datetime.fromtimestamp(last_check).strftime("%H:%M:%S")
        return "Nog niet gecontroleerd"

    def show_settings_window(self):
        """Open CMD window directly to settings screen"""
        if self.cmd_window and self.cmd_window.poll() is None:
            # Window already open - close it first
            try:
                self.cmd_window.terminate()
            except:
                pass

        # Create a settings-focused script (Dutch)
        script_content = '''
import json
import os
import sys
import time
from datetime import datetime

def load_config():
    default_config = {
        "detection_method": "process",
        "scan_interval": 2,
        "logging": False
    }
    try:
        if os.path.exists("config.json"):
            with open("config.json", "r", encoding="utf-8") as f:
                loaded = json.load(f)
                return {**default_config, **loaded}
    except:
        pass
    return default_config

def save_config(config):
    try:
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Opslaan fout: {e}")

def get_single_key():
    try:
        import msvcrt
        return msvcrt.getch().decode('utf-8')
    except:
        return input().strip()[:1]

def show_settings():
    os.system("mode con: cols=58 lines=14")

    while True:
        os.system("cls")
        config = load_config()

        print("+======================================================+")
        print("|                   INSTELLINGEN                     |")
        print("+======================================================+")
        print("|                                                    |")
        print(f"| 1) Detectiemethode: {config.get('detection_method', 'process'):<27} |")
        print(f"| 2) Scan Interval: {config.get('scan_interval', 2)} seconden{' '*(21)} |")
        logging_status = "Aan" if config.get('logging', False) else "Uit"
        print(f"| 3) Logboek: {logging_status:<36} |")
        print("|                                                    |")
        print("| [1-3] Wijzig instelling                           |")
        print("| [S] Opslaan en terug                              |")
        print("| [Q] Terug zonder opslaan                          |")
        print("+======================================================+")
        print()
        print("Druk op toets: [1-3/S/Q]")

        choice = get_single_key().lower()

        if choice == '1':
            os.system("cls")
            print("Kies detectiemethode:")
            print("1) Process Detection (Snelst)")
            print("2) Port Monitoring")
            print("3) Registry Check (Windows)")
            print("4) Hybrid Mode (Meest accuraat)")
            print()
            print("Druk op toets [1-4]:")

            method_choice = get_single_key()
            methods = {"1": "process", "2": "port", "3": "registry", "4": "hybrid"}

            if method_choice in methods:
                config["detection_method"] = methods[method_choice]
                save_config(config)
                print(f"Methode gewijzigd naar: {methods[method_choice]}")
                time.sleep(1)

        elif choice == '2':
            os.system("cls")
            try:
                interval = int(input("Nieuwe scan interval (1-10 seconden): "))
                if 1 <= interval <= 10:
                    config["scan_interval"] = interval
                    save_config(config)
                    print(f"Interval gewijzigd naar: {interval} seconden")
                    time.sleep(1)
                else:
                    print("Ongeldig interval (moet 1-10 zijn)")
                    time.sleep(1)
            except ValueError:
                print("Ongeldige invoer")
                time.sleep(1)

        elif choice == '3':
            current = config.get('logging', False)
            config['logging'] = not current
            save_config(config)
            status = "ingeschakeld" if not current else "uitgeschakeld"
            print(f"Logboek {status}")
            time.sleep(1)

        elif choice == 's':
            print("Instellingen opgeslagen!")
            time.sleep(1)
            break

        elif choice == 'q':
            break

if __name__ == "__main__":
    os.system("title NetSupport Monitor - Instellingen")
    os.system("color 0A")
    show_settings()
'''

        script_path = "netsupport_settings.py"
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)

            batch_script = f'''@echo off
title NetSupport Monitor - Instellingen
color 0A
mode con: cols=58 lines=14

python "{script_path}"
'''

            batch_path = "netsupport_settings_launcher.bat"
            with open(batch_path, 'w', encoding='ascii', errors='replace') as f:
                f.write(batch_script)

            self.cmd_window = subprocess.Popen([batch_path],
                                             creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            print(f"Kon instellingen venster niet openen: {e}")

    def show_statistics_window(self, stats):
        """Show statistics in CMD window (Dutch)"""
        # Format statistics
        total = stats.get('total_connections', 0)
        today = stats.get('connections_today', 0)
        duration = stats.get('total_connection_duration', 0) / 60
        last_conn = stats.get('last_connection_time')
        history_count = len(stats.get('connection_history', []))

        if last_conn:
            last_conn_str = datetime.fromtimestamp(last_conn).strftime('%Y-%m-%d %H:%M:%S')
        else:
            last_conn_str = 'Nooit'

        # Create statistics display script (Dutch)
        script_content = f'''
import os
import sys

def show_stats():
    os.system("cls")
    os.system("mode con: cols=58 lines=18")

    print("+======================================================+")
    print("|            VERBINDINGSSTATISTIEKEN                 |")
    print("+======================================================+")
    print("|                                                    |")
    print(f"| Totaal verbindingen:   {total:<27} |")
    print(f"| Verbindingen vandaag:  {today:<27} |")
    print(f"| Totale duur:           {duration:.1f} minuten{' '*(27-len(str(int(duration)))-9)} |")
    print("|                                                    |")
    print(f"| Laatste verbinding:                                |")
    print(f"|   {last_conn_str:<50} |")
    print("|                                                    |")
    print(f"| Recente geschiedenis:  {history_count} items{' '*(27-len(str(history_count))-6)} |")
    print("|                                                    |")
    print("+======================================================+")
    print("|                                                    |")
    print("| Druk op een toets om te sluiten...                |")
    print("+======================================================+")

    try:
        import msvcrt
        msvcrt.getch()
    except:
        input()

if __name__ == "__main__":
    os.system("title NetSupport Monitor - Statistieken")
    os.system("color 0A")
    show_stats()
'''

        script_path = "netsupport_statistics.py"
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)

            batch_script = f'''@echo off
title NetSupport Monitor - Statistieken
color 0A
mode con: cols=58 lines=18

python "{script_path}"
'''

            batch_path = "netsupport_statistics_launcher.bat"
            with open(batch_path, 'w', encoding='ascii', errors='replace') as f:
                f.write(batch_script)

            subprocess.Popen([batch_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            print(f"Kon statistieken venster niet openen: {e}")

class NetSupportMonitorSimple:
    def __init__(self):
        self.config_file = "config.json"
        self.log_file = "netsupport_log.txt"
        self.status_file = "netsupport_status.json"
        self.stats_file = "netsupport_stats.json"
        self.translations_file = "translations.json"
        self.running = False
        self.log_buffer = []
        self.last_flush = time.time()

        # Load configuration
        self.config = self.load_config()

        # Load translations
        self.translations = self.load_translations()
        # Set default language to Dutch for NL version
        self.current_language = self.config.get("language", "nl")
        if "language" not in self.config or self.config.get("language") == "en":
            self.config["language"] = "nl"
            self.current_language = "nl"

        # Initialize interfaces
        self.tray_icon = None
        self.cmd_interface = SimpleCMDInterface(self)
        self.tray_ready = threading.Event()

        # Status tracking
        self.last_status = None
        self.last_check_time = None

        # Statistics tracking
        self.stats = self.load_stats()

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
            "log_flush_interval": 30,
            "auto_start": False,
            "silent_mode": False,
            "show_notifications": True,
            "language": "en",
            "network_adapter": "all"
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    return {**default_config, **loaded}
            except Exception as e:
                print(f"Config load error: {e}")

        return default_config

    def load_translations(self) -> Dict[str, Dict[str, str]]:
        """Load translations from file"""
        default_translations = {
            "en": {"app_title": "NetSupport Monitor"},
            "nl": {"app_title": "NetSupport Monitor"}
        }

        if os.path.exists(self.translations_file):
            try:
                with open(self.translations_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Translations load error: {e}")

        return default_translations

    def t(self, key: str) -> str:
        """Translate a key to current language"""
        lang = self.current_language
        if lang in self.translations and key in self.translations[lang]:
            return self.translations[lang][key]
        # Fallback to English
        if "en" in self.translations and key in self.translations["en"]:
            return self.translations["en"][key]
        # Fallback to key itself
        return key

    def switch_language(self, lang: str):
        """Switch application language"""
        if lang in self.translations:
            self.current_language = lang
            self.config["language"] = lang
            self.save_config()
            print(f"Language switched to: {lang}")
            # Update tray icon title
            if self.tray_icon:
                self.update_tray_icon(self.last_status or False)
            return True
        return False

    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Config save error: {e}")

    def save_status(self):
        """Save current status to shared file for CMD window"""
        try:
            status_data = {
                "connected": self.last_status or False,
                "last_check": self.last_check_time,
                "method_used": self.config.get("detection_method", "unknown"),
                "timestamp": time.time()
            }
            with open(self.status_file, "w", encoding="utf-8") as f:
                json.dump(status_data, f, indent=2)
        except Exception as e:
            print(f"Status save error: {e}")

    def load_stats(self) -> Dict[str, Any]:
        """Load connection statistics"""
        default_stats = {
            "total_connections": 0,
            "connections_today": 0,
            "last_connection_time": None,
            "total_connection_duration": 0,
            "last_reset": datetime.now().strftime("%Y-%m-%d"),
            "connection_history": []
        }

        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    # Reset daily counter if new day
                    if loaded.get("last_reset") != datetime.now().strftime("%Y-%m-%d"):
                        loaded["connections_today"] = 0
                        loaded["last_reset"] = datetime.now().strftime("%Y-%m-%d")
                    return {**default_stats, **loaded}
            except Exception as e:
                print(f"Stats load error: {e}")

        return default_stats

    def save_stats(self):
        """Save connection statistics"""
        try:
            with open(self.stats_file, "w", encoding="utf-8") as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"Stats save error: {e}")

    def update_stats(self, connected: bool):
        """Update connection statistics"""
        if connected and not self.last_status:
            # New connection detected
            self.stats["total_connections"] += 1
            self.stats["connections_today"] += 1
            self.stats["last_connection_time"] = time.time()

            # Add to history (keep last 50)
            history_entry = {
                "timestamp": time.time(),
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.stats["connection_history"].append(history_entry)
            if len(self.stats["connection_history"]) > 50:
                self.stats["connection_history"] = self.stats["connection_history"][-50:]

            self.save_stats()
        elif not connected and self.last_status:
            # Connection ended - calculate duration
            if self.stats.get("last_connection_time"):
                duration = time.time() - self.stats["last_connection_time"]
                self.stats["total_connection_duration"] += duration
                self.save_stats()

    def setup_auto_start(self, enable: bool):
        """Setup auto-start with Windows"""
        if not WINDOWS_AVAILABLE:
            print("Automatisch opstarten alleen beschikbaar op Windows")
            return False

        try:
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            app_name = "NetSupportMonitor"

            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)

            if enable:
                # Add to startup
                exe_path = os.path.abspath(sys.argv[0])
                if exe_path.endswith('.py'):
                    # If running from Python, use pythonw to hide console
                    exe_path = f'pythonw "{exe_path}"'
                else:
                    # If it's an exe, use it directly
                    exe_path = f'"{exe_path}"'

                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
                print("✅ Automatisch opstarten ingeschakeld")
            else:
                # Remove from startup
                try:
                    winreg.DeleteValue(key, app_name)
                    print("✅ Automatisch opstarten uitgeschakeld")
                except FileNotFoundError:
                    pass

            winreg.CloseKey(key)
            self.config["auto_start"] = enable
            self.save_config()
            return True

        except Exception as e:
            print(f"Automatisch opstarten fout: {e}")
            return False

    def check_auto_start_status(self) -> bool:
        """Check if auto-start is currently enabled"""
        if not WINDOWS_AVAILABLE:
            return False

        try:
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            app_name = "NetSupportMonitor"

            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            try:
                winreg.QueryValueEx(key, app_name)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception:
            return False

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

    def get_network_adapters(self) -> List[str]:
        """Get list of available network adapters"""
        try:
            adapters = []
            addrs = psutil.net_if_addrs()
            for adapter_name in addrs.keys():
                adapters.append(adapter_name)
            return adapters
        except Exception as e:
            print(f"Network adapter list error: {e}")
            return []

    def check_netsupport_port(self) -> bool:
        """Check for NetSupport port connections"""
        target_port = int(self.config.get("port", 5405))
        selected_adapter = self.config.get("network_adapter", "all")

        try:
            connections = psutil.net_connections(kind="inet")

            # Get adapter IP addresses if specific adapter selected
            adapter_ips = set()
            if selected_adapter != "all":
                try:
                    addrs = psutil.net_if_addrs()
                    if selected_adapter in addrs:
                        for addr in addrs[selected_adapter]:
                            if addr.family == 2:  # AF_INET (IPv4)
                                adapter_ips.add(addr.address)
                except Exception as e:
                    print(f"Adapter IP lookup error: {e}")

            for conn in connections:
                if (hasattr(conn, 'laddr') and conn.laddr and
                    hasattr(conn.laddr, 'port') and conn.laddr.port == target_port and
                    conn.status == "ESTABLISHED"):

                    # If specific adapter selected, check if connection is on that adapter
                    if selected_adapter != "all":
                        if conn.laddr.ip not in adapter_ips:
                            continue

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
            print(f"Log flush error: {e}")

    def load_icon_from_file(self, filename: str) -> Optional[Image.Image]:
        """Load icon from file if it exists"""
        try:
            if os.path.exists(filename):
                return Image.open(filename)
        except Exception as e:
            print(f"Icon load error ({filename}): {e}")
        return None

    def create_tray_icon(self, connected: bool) -> Image.Image:
        """Create system tray icon"""
        # Try to load pre-made icons first
        if connected:
            icon = self.load_icon_from_file("icon_warning.ico")
            if not icon:
                icon = self.load_icon_from_file("icon_warning.png")
        else:
            icon = self.load_icon_from_file("icon_safe.ico")
            if not icon:
                icon = self.load_icon_from_file("icon_safe.png")

        # If pre-made icon found, resize and return
        if icon:
            return icon.resize((32, 32), Image.Resampling.LANCZOS)

        # Fallback: Generate icon dynamically
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
                    self.tray_icon.title = self.t("tray_title_warning")
                else:
                    self.tray_icon.title = self.t("tray_title_safe")
            except Exception as e:
                print(f"Tray icon update error: {e}")

    def show_notification(self, connected: bool):
        """Show Windows notification on status change"""
        if not self.tray_icon or not self.config.get("show_notifications", True):
            return

        # Don't show notifications in silent mode
        if self.config.get("silent_mode", False):
            return

        try:
            if connected:
                self.tray_icon.notify(
                    title=self.t("notification_title_alert"),
                    message=self.t("notification_message_connected")
                )
            else:
                self.tray_icon.notify(
                    title=self.t("notification_title_safe"),
                    message=self.t("notification_message_disconnected")
                )
        except Exception as e:
            print(f"Notification error: {e}")

    def start_tray(self):
        """Initialize system tray icon"""
        try:
            # Create menu with visible/invisible option based on silent mode
            if self.config.get("silent_mode", False):
                # Minimal menu in silent mode
                menu = pystray.Menu(
                    pystray.MenuItem("❌ Afsluiten", self.exit_program)
                )
            else:
                # Full menu in normal mode
                menu = pystray.Menu(
                    pystray.MenuItem("📊 Toon Details", self.cmd_interface.show_details, default=True),
                    pystray.MenuItem("⚙️ Instellingen", self.show_simple_settings),
                    pystray.MenuItem("📈 Statistieken", self.show_statistics),
                    pystray.Menu.SEPARATOR,
                    pystray.MenuItem("🔔 Meldingen", self.toggle_notifications,
                                   checked=lambda item: self.config.get("show_notifications", True)),
                    pystray.MenuItem("🚀 Automatisch opstarten", self.toggle_auto_start,
                                   checked=lambda item: self.check_auto_start_status()),
                    pystray.Menu.SEPARATOR,
                    pystray.MenuItem("❌ Afsluiten", self.exit_program)
                )

            self.tray_icon = pystray.Icon(
                "netsupport_monitor",
                self.create_tray_icon(False),
                self.t("tray_title_safe"),
                menu
            )

            self.tray_ready.set()
            self.tray_icon.run()

        except Exception as e:
            print(f"Tray start error: {e}")

    def show_simple_settings(self):
        """Show simple settings via CMD"""
        self.cmd_interface.show_settings_window()

    def show_statistics(self):
        """Show connection statistics in CMD window"""
        self.cmd_interface.show_statistics_window(self.stats)

    def toggle_notifications(self):
        """Toggle notifications on/off"""
        current = self.config.get("show_notifications", True)
        self.config["show_notifications"] = not current
        self.save_config()
        status = "ingeschakeld" if not current else "uitgeschakeld"
        print(f"Meldingen {status}")

    def toggle_auto_start(self):
        """Toggle auto-start on/off"""
        current = self.check_auto_start_status()
        self.setup_auto_start(not current)

    def reload_config(self):
        """Reload configuration from file (live reload)"""
        try:
            old_config = self.config.copy()
            self.config = self.load_config()

            # Check if detection method changed
            if old_config.get("detection_method") != self.config.get("detection_method"):
                print(f"Detectiemethode gewijzigd naar: {self.config.get('detection_method')}")

            # Check if scan interval changed
            if old_config.get("scan_interval") != self.config.get("scan_interval"):
                print(f"Scan interval gewijzigd naar: {self.config.get('scan_interval')}s")

            return True
        except Exception as e:
            print(f"Config herlaad fout: {e}")
            return False

    def background_monitor(self):
        """Background monitoring thread"""
        last_config_check = time.time()

        while self.running:
            try:
                # Reload config every 10 seconds for live updates
                if time.time() - last_config_check > 10:
                    self.reload_config()
                    last_config_check = time.time()

                start_time = time.time()
                connected = self.check_connection()
                check_duration = time.time() - start_time

                status_changed = connected != self.last_status
                time_passed = (self.last_check_time is None or
                              time.time() - self.last_check_time > 30)

                # Always update timestamp for refresh functionality
                self.last_check_time = time.time()
                self.save_status()

                if status_changed or time_passed:
                    self.update_tray_icon(connected)

                    status_msg = "Leerkracht verbonden" if connected else "Geen verbinding"
                    self.log_status(f"{status_msg} (controle: {check_duration:.2f}s)")

                    # Update stats
                    self.update_stats(connected)

                    # Show Windows notification on status change
                    if status_changed:
                        self.show_notification(connected)

                    self.last_status = connected

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
        print("NetSupport Monitor wordt afgesloten...")

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
        print("=== NetSupport Monitor v0.4.1beta - Nederlandse Versie ===")
        print("Detectiemethode:", self.config.get("detection_method", "process"))
        print("Scan interval:", self.config.get("scan_interval", 2), "seconden")
        print("Interface: Tray icoon + CMD details")

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

        print("✅ NetSupport Monitor draait in systeem tray")
        print("🖱️  Rechtsklik op tray icoon voor opties")
        print("📊 'Toon Details' voor CMD interface")

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
        print(f"Fatale fout: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)