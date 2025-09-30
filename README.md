# NetSupport Monitor v0.4.1beta

NetSupport Monitor is a **simple, lightweight tool** for monitoring **NetSupport School** connections on your computer.
**Perfect for students** - just check the tray icon to see if a teacher is connected!

---

## ✨ What's New in v0.4.1beta
- 🎯 **Super Simple Interface** - No complex menus that can break
- 📊 **Tray-First Design** - 99% of the time just look at the tray icon
- 💻 **Real-Time CMD Details** - Live status synchronization
- 🔔 **Windows Notifications** - Instant alerts when teacher connects
- 🚀 **Auto-Start Support** - Launch automatically at Windows startup
- 📈 **Connection Statistics** - Track history and usage patterns in dedicated CMD window
- 🌍 **Multi-Language** - English and Dutch versions available
- ⚙️ **Direct Settings Access** - Settings open directly from tray menu
- 🔧 **Better Detection** - Multiple detection methods for accuracy
- 🐛 **Bug Fixes** - Fixed menu display, timestamp refresh, and keyboard shortcuts

---

## 🚀 How It Works

### **Tray Icon (Main Interface)**
- 🟢 **Green Icon** = Safe, no teacher connected
- 🔴 **Red Icon** = ⚠️ Teacher is connected to your computer
- **Right-click** for options

### **CMD Details Window**
- Shows **real-time live status** from monitor (not hardcoded!)
- Displays last check time, detection method, current settings
- Keyboard navigation: [S]ettings, [L]ogs, [R]efresh, [Q]uit
- Opens only when you need details

### **Tray Menu Features**
- 📊 Show Details - Open CMD interface
- ⚙️ Settings - Quick configuration access
- 📈 Statistics - View connection history and stats
- 🔔 Toggle Notifications - Enable/disable popup alerts
- 🚀 Toggle Auto-start - Enable/disable Windows startup
- 🌍 Language - Switch between English/Dutch
- ❌ Exit - Close application

## 📋 Features

### **Core Features**
- ✅ **Simple tray icon monitoring** - Green = Safe, Red = Warning
- ✅ **4 Detection methods**: Process, Port, Registry, Hybrid
- ✅ **Real-time status synchronization** - CMD window shows live data
- ✅ **Windows notifications** - Popup alerts on status changes
- ✅ **Customizable scan interval** (1-10 seconds)
- ✅ **Optional logging** to file with buffered writes
- ✅ **Lightweight and fast** (19KB vs 50KB old version)

### **Advanced Features**
- ✅ **Auto-start at Windows startup** - Registry integration
- ✅ **Connection statistics** - Track total connections, daily count, duration
- ✅ **Connection history** - Last 50 connections with timestamps
- ✅ **Network adapter selection** - Filter port monitoring by adapter
- ✅ **Silent/Stealth mode** - Minimal tray menu for enterprise
- ✅ **Live config reload** - Settings update every 10 seconds (no restart!)
- ✅ **Multi-language support** - Runtime switch between English & Dutch
- ✅ **Custom icon support** - Load high-quality .ico or .png files
- ✅ **Improved error handling** - Graceful fallbacks and config backups
- ✅ **Student-friendly** - No confusing interfaces

---

## ⚙️ Configuration

### **Via Tray Menu:**
- Right-click tray icon for quick access to:
  - Notifications toggle
  - Auto-start toggle
  - Language selection
  - Statistics viewer

### **Via CMD Interface:**
1. Right-click tray icon → "Show Details"
2. Press [S] for Settings
3. Use 1-3 to change: Detection Method, Scan Interval, Logging
4. Press [S] to save (updates live - no restart needed!)

### **Detection Methods:**
- **Process** (Fastest) - Scans for NetSupport processes
- **Port** - Monitors network connections on port 5405
- **Registry** (Windows) - Checks Windows registry keys
- **Hybrid** (Most Accurate) - Combines all methods

### **Configuration File (config.json):**
```json
{
  "detection_method": "hybrid",
  "scan_interval": 2,
  "logging": false,
  "port": 5405,
  "auto_start": false,
  "silent_mode": false,
  "show_notifications": true,
  "language": "en",
  "network_adapter": "all"
}
```  

---

## 📂 Project Status & Architecture

### **Current Files:**
- **Main Applications**:
  - `/.py/netsupport_monitor_en_v0.4.1beta.py` (English)
  - `/.py/netsupport_monitor_nl_v0.4.1beta.py` (Dutch)
- **Executables**:
  - `NetSupportMonitor_EN_v0.4.1beta.exe` (English)
  - `NetSupportMonitor_NL_v0.4.1beta.exe` (Dutch)
- **Utilities**:
  - `setup.py` - Dependency checker and installer
  - `create_icons.py` - High-quality icon generator
  - `translations.json` - Multi-language support
- **Runtime Files** (auto-generated):
  - `netsupport_status.json` - Real-time status sharing
  - `netsupport_stats.json` - Connection statistics
  - `netsupport_log.txt` - Optional activity log
- **Archive**: v0.3.0beta archived in Archive_v0.3.0beta/

### **Architecture:**
- **Tray-First Design**: Main interface via system tray icon
- **Real-Time Sync**: Status shared via JSON files
- **CMD Details Window**: Live-updating Python script
- **Background Monitoring**: Multi-threaded detection with live config reload
- **Statistics Tracking**: Persistent connection history and analytics
- **Multi-Language**: Translation system with runtime switching

### **Detection Methods:**
1. **Process Detection** (Default) - Scans for NetSupport executables
2. **Port Monitoring** - Checks network connections on port 5405
3. **Registry Check** - Windows registry monitoring
4. **Hybrid Mode** - Combines all methods for maximum accuracy

### **Current Status:**
- ✅ v0.4.1beta - Bug fixes and improvements
- ✅ Direct settings and statistics access from tray menu
- ✅ Fixed menu display issues and timestamp refresh
- ✅ Keyboard shortcuts standardized (S/L/R/Q)
- ✅ Student-friendly design completed
- ✅ Executables built and ready for release

---

## 🚀 Installation & Usage

### **Easy Setup (Recommended):**
1. Run `setup.py` to automatically check and install dependencies
2. Run the `.exe` file in your preferred language

### **Manual Setup:**
```bash
pip install psutil pillow pystray
python Beta/netsupport_monitor_en_v0.3.0beta.py
```

### **First Run:**
- Application creates default `config.json` if missing
- Tray icon appears in system tray
- Status checks begin automatically

### **Daily Usage:**
1. **Check tray icon**: 🟢 Green = Safe, 🔴 Red = Teacher connected
2. **Right-click tray**: Access full menu
3. **Notifications**: Automatic popup alerts (if enabled)
4. **Statistics**: View connection history via tray menu

### **Optional Features:**
- **Auto-start**: Enable via tray menu → Auto-start (checkmark)
- **Language**: Switch via tray menu → Language → English/Nederlands
- **Custom Icons**: Place `icon_safe.ico` and `icon_warning.ico` in app folder

---

## 🔧 Development Notes

### **Recent Improvements (v0.3.0beta):**
- ✅ Real-time status synchronization implemented
- ✅ Windows notifications added
- ✅ Auto-start functionality complete
- ✅ Connection statistics and history tracking
- ✅ Live config reload (updates every 10s)
- ✅ Multi-language runtime switching
- ✅ Network adapter selection for port monitoring
- ✅ Silent/stealth mode for enterprise
- ✅ Improved error handling throughout
- ✅ Custom icon support (.ico/.png)

### **Known Issues:**
- None currently - all major features implemented!

### **Potential Future Enhancements:**
- Sound alerts (optional beep on connection)
- Email notifications for IT administrators
- Web dashboard for network-wide monitoring
- MacOS/Linux support

---

## 📱 Screenshots
_(Screenshots will be added after v3.0 release)_

---

## ⚖️ Disclaimer
This software is provided **as-is**, without warranty of any kind.
The author is **not responsible for any misuse, damage, or consequences** caused by the use of this software.
**Educational use only** - respect school policies and local laws.

---

## 🤝 Contributing
Contributions welcome! Please:
- Test the simple interface design with real users
- Report bugs via GitHub Issues
- Suggest improvements for student usability
- Submit pull requests with clear descriptions

---

## 📄 License
MIT License - See [LICENSE.md](LICENSE.md) for details.

---

## 📋 Version History
- **v0.4.1beta** (Current) - Bug fixes and UI improvements
  - Fixed: Settings menu now opens directly to settings window
  - Fixed: Statistics display in dedicated CMD window (not terminal)
  - Fixed: Menu items showing as "menu_settings" etc.
  - Fixed: Timestamp refresh on manual refresh button
  - Fixed: Keyboard shortcuts standardized to S/L/R/Q in both EN/NL
  - Improved: Separate CMD windows for Settings and Statistics
- **v0.3.0beta** - Feature-complete release with all enhancements
  - Real-time status sync
  - Windows notifications
  - Auto-start support
  - Statistics tracking
  - Multi-language runtime switching
  - Live config reload
  - Network adapter selection
  - Silent mode
  - Custom icons
- **v0.2.7beta** (Archived) - Complex GUI with Tailscale-style menus
- **Earlier versions** - See git history for details