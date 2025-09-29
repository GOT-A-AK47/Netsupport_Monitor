# NetSupport Monitor v3.0

NetSupport Monitor is a **simple, lightweight tool** for monitoring **NetSupport School** connections on your computer.
**Perfect for students** - just check the tray icon to see if a teacher is connected!

---

## ✨ What's New in v3.0
- 🎯 **Super Simple Interface** - No complex menus that can break
- 📊 **Tray-First Design** - 99% of the time just look at the tray icon
- 💻 **CMD Details Window** - Clean, fast details when you need them
- ⚙️ **Reliable Settings** - Simple keyboard-driven configuration
- 🔧 **Better Detection** - Multiple detection methods for accuracy

---

## 🚀 How It Works

### **Tray Icon (Main Interface)**
- 🟢 **Green Icon** = Safe, no teacher connected
- 🔴 **Red Icon** = ⚠️ Teacher is connected to your computer
- **Right-click** for options

### **CMD Details Window**
- Shows real-time status, last check time, detection method
- Keyboard navigation: [S]ettings, [L]ogs, [R]efresh, [Q]uit
- Opens only when you need details

## 📋 Features
- ✅ **Simple tray icon monitoring**
- ✅ **4 Detection methods**: Process, Port, Registry, Hybrid
- ✅ **Customizable scan interval** (1-10 seconds)
- ✅ **Optional logging** to file
- ✅ **Lightweight and fast** (19KB vs 50KB old version)
- ✅ **Student-friendly** - no confusing interfaces
- ✅ **Multi-language** (English & Dutch)

---

## ⚙️ Configuration

Settings via simple CMD interface:
1. Right-click tray icon → "Toon details"
2. Press [S] for Settings
3. Use 1-3 to change: Detection Method, Scan Interval, Logging
4. Press [S] to save

**Detection Methods:**
- **Process** (Fastest) - Scans for NetSupport processes
- **Port** - Monitors network connections on port 5405
- **Registry** (Windows) - Checks Windows registry keys
- **Hybrid** (Most Accurate) - Combines all methods  

---

## 📂 Project Status & Architecture

### **Current Files:**
- **Main Application**: `.py/netsupport_monitor_en.py` (v3.0 - Simple Interface)
- **Development**: Located in `/Beta/netsupport_monitor_en_v0.3.0beta.py`
- **Archive**: Complex GUI version archived as v0.2.7beta
- **Languages**: English (EN) and Dutch (NL) versions available

### **Architecture:**
- **Tray-First Design**: Main interface via system tray icon
- **CMD Details Window**: Batch script for advanced options
- **Background Monitoring**: Multi-threaded detection system
- **Simple Configuration**: Keyboard-driven settings

### **Detection Methods:**
1. **Process Detection** (Default) - Scans for NetSupport executables
2. **Port Monitoring** - Checks network connections on port 5405
3. **Registry Check** - Windows registry monitoring
4. **Hybrid Mode** - Combines all methods for maximum accuracy

### **Current Status:**
- ✅ v3.0 Simple interface implemented
- ✅ Complex GUI removed (performance issues)
- ✅ Student-friendly design completed
- 🧪 **Testing Phase**: v0.3.0beta ready for validation
- ⏳ **Next**: Build executable and GitHub release

---

## 🚀 Installation & Usage

### **Requirements:**
```bash
pip install psutil pillow pystray
```

### **Run:**
Run the .exe file in the desired language

### **Usage:**
1. **Check tray icon**: Green = Safe, Red = Teacher connected
2. **Right-click tray**: Options menu
3. **"Toon details"**: Opens CMD interface for settings/logs

---

## 🔧 Development Notes

### **Known Issues:**
- CMD batch script may need encoding fixes for special characters
- Settings changes require restart for some detection methods

### **Future Improvements:**
- Real-time settings updates without restart
- Network adapter selection for port monitoring
- Silent mode for enterprise deployment

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
- **v3.0** (Pending) - Simple tray + CMD interface redesign
- **v0.2.7beta** (Archived) - Complex GUI with Tailscale-style menus
- **Earlier versions** - See git history for details