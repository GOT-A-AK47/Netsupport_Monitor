# 🚀 NetSupport Monitor Release Notes

---

## v0.4.1beta - Bug Fixes & UI Improvements

**Release Date**: January 2025
**Status**: Beta - Stable
**Focus**: Bug fixes and usability improvements

### 🐛 **Bug Fixes**

1. **Settings Menu Fixed**
   - Settings tray menu option now opens directly to settings window
   - Previously opened general details window requiring manual navigation
   - Now uses dedicated `show_settings_window()` method

2. **Statistics Display Fixed**
   - Statistics now display in dedicated CMD window
   - Previously printed to Python terminal (invisible to users)
   - Properly formatted window with "Press any key to close"

3. **Menu Display Fixed**
   - Fixed tray menu showing "menu_settings", "menu_statistics" etc.
   - Removed translation system from menu, hardcoded menu items
   - All menu items now display correctly in both EN/NL versions

4. **Timestamp Refresh Fixed**
   - Manual refresh (R key) now updates timestamp immediately
   - Previously only updated after status change or 30s timeout
   - Timestamp now updates on every check for better UX

5. **Keyboard Shortcuts Standardized**
   - Dutch version now uses same keys as English: S/L/R/Q
   - Previously used I/L/V/A in Dutch (confusing)
   - Consistent shortcuts across both language versions

### ✨ **Improvements**

- **Dedicated Windows**: Settings and Statistics each have their own CMD window
- **Better UX**: Direct access to features from tray menu
- **Consistent Behavior**: Both EN/NL versions behave identically

### 📋 **Files Updated**

- `netsupport_monitor_en_v0.4.1beta.py` - English version with all fixes
- `netsupport_monitor_nl_v0.4.1beta.py` - Dutch version with all fixes

---

## v0.3.0beta - Feature Complete Release

**Release Date**: September 30, 2024
**Status**: Beta - Feature Complete
**Interface**: Complete redesign - Tray + CMD with advanced features

---

## 🎯 **What's New: Simple Design for Students**

### **Problem with v0.2.7beta:**
- Complex Tailscale-style GUI was **too confusing** for students
- **Menu bugs** and selection issues
- **Performance problems** with fancy interface
- Students only need: *"Is teacher connected? Yes/No"*

### **Solution in v0.3.0beta:**
- **🟢 Tray Icon**: Green = Safe, Red = Teacher connected
- **💻 CMD Details**: Only when you need advanced info
- **⚙️ Simple Settings**: Keyboard-driven, no fancy menus

---

## ✨ **New Features**

### **🎛️ Tray-First Interface**
```
99% of usage: Just look at tray icon
 1% of usage: Right-click → access full menu
 0% confusion: No complex menus to break
```

### **💻 Real-Time CMD Interface**
- **Live status sync**: CMD window shows actual monitor status (not hardcoded!)
- **Real-time updates**: Settings changes visible immediately
- **Direct key input**: Press [S] for settings (no Enter needed)
- **Auto-resize**: Perfect window size for each screen
- **Error handling**: Graceful fallbacks for corrupt configs

### **🔔 Windows Notifications**
- **Instant alerts**: Popup notifications when teacher connects/disconnects
- **Customizable**: Toggle via tray menu or config
- **Silent mode**: Disable for stealth operation
- **Native Windows**: Uses pystray notification system

### **🚀 Auto-Start Support**
- **Windows startup**: Launch automatically at login
- **Registry integration**: Proper Windows implementation
- **Toggle via menu**: Enable/disable with one click
- **Smart detection**: Works with both .py and .exe files

### **📈 Connection Statistics & History**
- **Total connections**: Lifetime counter
- **Daily tracking**: Resets automatically each day
- **Connection duration**: Total time teacher was connected
- **History log**: Last 50 connections with timestamps
- **View via menu**: Access statistics from tray icon

### **🌍 Multi-Language Support**
- **Runtime switching**: Change language without restart
- **Full translation**: All UI elements translated
- **English & Dutch**: Native support for both languages
- **Extensible**: Easy to add more languages via translations.json

### **⚙️ Advanced Settings**
- **4 Detection Methods**: Process, Port, Registry, Hybrid
- **Flexible Intervals**: 1-10 seconds scan time
- **Live config reload**: Settings update every 10 seconds (no restart!)
- **Network adapter selection**: Filter port monitoring by adapter
- **Silent/stealth mode**: Minimal UI for enterprise deployment
- **Custom icons**: Load high-quality .ico or .png files

---

## 🔧 **Technical Improvements**

### **Performance**
- **60% smaller code**: 21KB vs 50KB (old complex version)
- **Faster startup**: No complex GUI initialization
- **Lower memory**: Efficient threading and buffering
- **Live config reload**: No restart overhead

### **Reliability**
- **Fixed encoding errors**: No more `'charmap' codec` issues
- **Improved error handling**: Graceful fallbacks throughout
- **Config backup/restore**: Automatic backup before saving
- **Status synchronization**: Real-time sharing via JSON files
- **Better threading**: No UI conflicts, proper cleanup

### **Architecture**
- **Status sharing**: `netsupport_status.json` for real-time sync
- **Statistics persistence**: `netsupport_stats.json` for history
- **Translation system**: Centralized `translations.json`
- **Icon flexibility**: Load custom icons or generate dynamically
- **Modular design**: Easy to extend and maintain

### **Compatibility**
- **All Windows versions**: Works on Windows 7+
- **Python 3.7+**: Modern Python support
- **Works everywhere**: No special fonts or dependencies
- **Student-proof**: Simple = harder to break

---

## 📋 **How to Use**

### **Step 1: Easy Setup**
```bash
# Option A: Run setup script (recommended)
python setup.py

# Option B: Manual install
pip install psutil pillow pystray
python Beta/netsupport_monitor_en_v0.3.0beta.py
```

### **Step 2: Daily Usage**
1. **Check tray icon**: 🟢 = Safe, 🔴 = Teacher connected
2. **Watch notifications**: Popup alerts when status changes
3. **That's it!** 99% of the time, you're done

### **Step 3: Tray Menu (Right-click)**
- 📊 **Show Details** - Open CMD interface with live status
- ⚙️ **Settings** - Configure detection method, intervals
- 📈 **Statistics** - View connection history and stats
- 🔔 **Notifications** - Toggle popup alerts
- 🚀 **Auto-start** - Enable Windows startup
- 🌍 **Language** - Switch English/Nederlands
- ❌ **Exit** - Close application

### **Step 4: CMD Details Window (Optional)**
1. **Right-click tray** → "Show Details"
2. **Press [S]** for settings, **[L]** for logs, **[R]** to refresh
3. **Press [Q]** to close details window
4. **Live updates**: Status refreshes automatically!

---

## 🎓 **Perfect for Students**

### **What Students Want:**
- ✅ **Instant status**: One glance at tray icon
- ✅ **Notifications**: Popup alerts when teacher connects
- ✅ **Always works**: No complex menus to break
- ✅ **No confusion**: Green = safe, red = warning
- ✅ **Fast**: Lightweight, doesn't slow down computer
- ✅ **Statistics**: See how often you've been monitored

### **What Teachers/IT Want:**
- ✅ **Reliable detection**: 4 different methods (hybrid mode)
- ✅ **Configurable**: Easy settings for different networks
- ✅ **Network adapter filtering**: Target specific connections
- ✅ **Logging**: Optional activity logs with buffered writes
- ✅ **Auto-start**: Launches automatically at login
- ✅ **Silent mode**: Minimal UI for school deployment
- ✅ **Statistics tracking**: Monitor usage patterns
- ✅ **Low maintenance**: Set-and-forget operation

---

## 🐛 **Known Issues**

### **Minor Issues:**
- ~~Some detection methods may need restart to fully apply~~ ✅ **FIXED** (Live config reload)
- ~~CMD window status is hardcoded~~ ✅ **FIXED** (Real-time sync)
- ~~No notifications~~ ✅ **FIXED** (Windows notifications added)
- ~~Manual startup required~~ ✅ **FIXED** (Auto-start support)

### **Current Status:**
- **No known issues!** All major features implemented and tested

---

## 🔄 **Migration from v0.2.7beta**

### **If you have v0.2.7beta:**
1. **Stop old version**
2. **Delete old files** (complex GUI version)
3. **Install v0.3.0beta**
4. **Copy your `config.json`** (settings will be preserved)

### **Settings Migration:**
- ✅ **Detection method**: Automatically preserved
- ✅ **Scan interval**: Automatically preserved
- ✅ **Logging settings**: Automatically preserved
- ❌ **Theme settings**: Removed (no longer needed)

---

## 🚀 **Next Steps**

### **Completed for v0.3.0beta:**
- [x] **Real-time status sync**: Live CMD window updates
- [x] **Windows notifications**: Popup alerts implemented
- [x] **Auto-start support**: Registry integration complete
- [x] **Statistics tracking**: Connection history and analytics
- [x] **Multi-language**: Runtime switching EN/NL
- [x] **Live config reload**: No restart needed
- [x] **Network adapter selection**: Filter by adapter
- [x] **Silent mode**: Enterprise deployment ready
- [x] **Custom icons**: High-quality icon support
- [x] **Error handling**: Improved throughout
- [x] **Setup script**: Automated dependency check
- [x] **Build executables**: .exe files ready
- [x] **Dutch version**: Full feature parity
- [x] **GitHub release**: Published and available

### **Before v1.0 (Full Release):**
- [ ] **Student testing**: Get feedback from real users
- [ ] **Documentation**: Screenshots and video guides
- [ ] **Performance testing**: Verify memory/CPU usage in production
- [ ] **Bug fixes**: Address any issues found during testing

### **Feedback Welcome:**
- 🐛 **Report bugs**: GitHub Issues
- 💡 **Suggest improvements**: Keep it simple!
- 🧪 **Test with students**: Real-world usage feedback
- ⭐ **Star on GitHub**: Show your support!

---

## 📞 **Support & Feedback**

**Found issues?** Report on GitHub: [Create Issue]
**Need help?** Check README.md for troubleshooting
**Want to contribute?** See CONTRIBUTING.md

**Remember**: This is beta software - test thoroughly before deploying to all students!

---

*Happy monitoring! 🎯*