# ⏻ Shutdown Timer

A simple Windows shutdown timer app. Set hours, minutes, and seconds — your PC will shut down automatically.

## 🔧 How to Build (One-Time Setup)

### Prerequisites
1. Install **Python 3.8+** from [python.org](https://www.python.org/downloads/)
   - ⚠️ **Check "Add Python to PATH"** during installation

### Build Steps
1. Download/clone this project folder
2. **Double-click `build.bat`** — it installs PyInstaller and builds the `.exe` automatically
3. Find your app at `dist/ShutdownTimer.exe`

That's it! Share `ShutdownTimer.exe` with anyone — **no Python needed** on their PC.

## 🚀 Usage

1. Double-click `ShutdownTimer.exe`
2. Set **Hours**, **Minutes**, **Seconds** (default: 30 minutes)
3. Click **Start** — Windows shutdown is scheduled
4. Click **Cancel** anytime to abort
5. Closing the window while a timer is active will ask if you want to cancel

## 📁 Project Structure

```
├── main.py        # App source code
├── build.bat      # One-click build script
└── README.md      # This file
```

## Notes

- Uses the native Windows `shutdown` command under the hood
- The countdown turns **red** in the last 60 seconds as a warning
- Requires **Windows** (uses `shutdown /s /t` command)
