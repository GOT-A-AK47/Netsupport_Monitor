# 🚀 Git Commands for v0.3.0beta Release

## 📋 **Quick Commands to Run:**

```bash
# Navigate to PUB directory
cd "C:\Users\tijnw\OneDrive - Scholengroep Sint-Michiel vzw\Documenten\Netsupport_Monitor\Netsupport_Monitor_PUB"

# Check git status
git status

# Add all new files
git add .

# Commit with descriptive message
git commit -m "Release v0.3.0beta - Simple Tray + CMD Interface

🎯 Major Interface Redesign:
- Removed complex Tailscale-style GUI (too buggy for students)
- NEW: Simple Tray + CMD interface design
- Real-time settings updates, direct key input
- Auto-resize windows, ASCII-only compatibility

✨ New Features:
- Tray-first design: Green=safe, Red=teacher connected
- Dynamic Python CMD interface (replaces batch scripts)
- 4 detection methods: Process, Port, Registry, Hybrid
- Single-key navigation (no Enter required)

🔧 Technical Improvements:
- 60% smaller codebase (21KB vs 50KB)
- Fixed encoding errors, duplicate messages
- Better threading, improved stability
- Student-friendly: 99% usage = just check tray icon

📦 Files Updated:
- netsupport_monitor_en.py (v0.3.0beta)
- README.md (updated for new interface)
- CHANGELOG.md (full version history)
- RELEASE_NOTES_v0.3.0beta.md (detailed release info)

🧪 Status: Beta - Ready for student testing"

# Push to GitHub
git push origin main

# Create and push tag for release
git tag v0.3.0beta
git push origin v0.3.0beta
```

---

## 📂 **What's Being Committed:**

### **✅ New/Updated Files:**
- `.py/netsupport_monitor_en.py` - **Main application (v0.3.0beta)**
- `README.md` - **Updated for new interface**
- `CHANGELOG.md` - **Full version history**
- `RELEASE_NOTES_v0.3.0beta.md` - **Detailed release notes**

### **🗑️ Removed Files:**
- `netsupport_monitor_en.exe` - **Old executable (v0.2.x)**
- `netsupport_monitor_nl.exe` - **Old executable (v0.2.x)**

### **📝 Unchanged Files:**
- `LICENSE.md` - **Still valid**
- `CODE_OF_CONDUCT.md` - **Still valid**
- `DISCLAIMER.md` - **Still valid**
- `.py/netsupport_monitor_nl.py` - **Dutch version (not updated yet)**

---

## 🏷️ **Release Creation (GitHub Web):**

After pushing, create GitHub release:

1. **Go to**: GitHub → Releases → "Create a new release"
2. **Tag**: `v0.3.0beta`
3. **Title**: `NetSupport Monitor v0.3.0beta - Simple Interface`
4. **Description**: Copy from `RELEASE_NOTES_v0.3.0beta.md`
5. **Check**: "This is a pre-release" ✅
6. **Attach**:
   - `netsupport_monitor_en.py` (source)
   - *(Executables will be added later)*

---

## 🔍 **Verify Before Push:**

```bash
# Check what will be committed
git diff --staged

# Check file sizes
ls -la .py/

# Verify main file works
python .py/netsupport_monitor_en.py --help
```

---

## 🚨 **Important Notes:**

1. **Pre-release**: Mark as beta on GitHub
2. **Executables**: Need to be built separately with PyInstaller
3. **Testing**: Encourage community testing before v0.3.0 stable
4. **Dutch version**: Not updated yet - English only for beta

---

**Ready to push? Run the commands above! 🚀**