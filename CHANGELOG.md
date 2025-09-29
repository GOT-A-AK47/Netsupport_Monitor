# Changelog

All notable changes to NetSupport Monitor will be documented in this file.

## [v0.3.0beta] - 2024-09-29

### 🎯 **Major Interface Redesign**
- **BREAKING**: Removed complex Tailscale-style GUI (too many bugs for students)
- **NEW**: Simple Tray + CMD interface design
- **NEW**: Python-based dynamic CMD interface (replaces static batch scripts)
- **NEW**: Real-time settings updates without restart

### ✨ **New Features**
- **Direct key input**: Press S/L/R/Q directly (no Enter required)
- **Auto-resize CMD window**: Compact, perfect-sized windows
- **Dynamic configuration**: Settings changes visible immediately
- **Better detection methods**: Process, Port, Registry, Hybrid modes
- **Improved error handling**: No more duplicate error messages

### 🔧 **Technical Improvements**
- **ASCII-only interface**: Fixed encoding issues on all Windows versions
- **Single-key navigation**: Using `msvcrt.getch()` for instant response
- **Cleaner code**: 21KB vs 50KB (complex GUI version)
- **Better threading**: Reduced conflicts and improved stability

### 🐛 **Bug Fixes**
- Fixed CMD window encoding errors (`charmap` codec issues)
- Fixed duplicate error messages
- Fixed refresh functionality (time updates correctly)
- Fixed settings not showing changes until restart

### 📋 **Interface Changes**
```
Main Screen: 58x16 cols  - Shows status, last check, method, interval
Settings:    58x14 cols  - Interactive configuration
Logs:        Full screen - View/browse log files
```

### 🎓 **Student-Friendly Design**
- **99% usage**: Just check tray icon (green=safe, red=teacher connected)
- **1% usage**: Open CMD for details/settings when needed
- **0% confusion**: No complex menus that can break or confuse

### 📦 **Files**
- **Main**: `netsupport_monitor_en.py` (English)
- **Legacy**: `netsupport_monitor_nl.py` (Dutch - not updated)
- **Archive**: Complex GUI moved to `/Archive/old_versions/`

---

## [v0.2.7beta] - 2024-09-28 (Archived)

### ❌ **Complex GUI Version (Discontinued)**
- Tailscale-style interface with submenus
- Theme system (light/dark)
- Complex preferences window
- **Issues**: Too many bugs, confusing for students, performance problems

### 🗃️ **Status**: Archived due to complexity issues

---

## [v0.2.x and earlier] - See git history

### 📚 **Legacy Versions**
- Original NetSupport detection implementations
- Various GUI experiments
- Dutch/English language support development

---

## 🔮 **Planned for v0.3.0 (Full Release)**
- [ ] Build new executables for v0.3.0beta
- [ ] Testing with real students
- [ ] Performance optimizations
- [ ] Documentation improvements
- [ ] Silent/enterprise deployment mode

---

## 📋 **Version Naming**
- **v0.x.y**: Development versions
- **vX.Y.Z**: Stable releases
- **beta**: Feature-complete but needs testing
- **alpha**: Early development, may have bugs