# PC Action Timer - Shutdown/Restart/Lock/Sleep - Version 2.0

A Windows application to schedule shutdown, restart, lock, or sleep actions with a timer.

## Features

- ⏰ Set timer in hours, minutes, and seconds
- 🔴 Shutdown PC
- 🔄 Restart PC
- 🔒 Lock screen
- 💤 Put PC to sleep
- 🖥️ Modern GUI interface
- ⏱️ Real-time countdown display
- ✅ Confirmation dialogs for safety

## Built on:

- Python 3.9+
- Tkinter (included with Python)

## Two Versions Available:

### 1. GUI Version (Recommended) - `timer_gui.py`

Modern graphical interface with buttons and visual countdown.

### 2. Console Version - `trunOFFpc.py`

Original command-line interface version.

## How to Run:

### Option A: Run GUI with Python

1. Download [Python 3.9+](https://www.python.org/downloads/) and install
2. Run the GUI application:
   ```
   python timer_gui.py
   ```

### Option B: Build Standalone Executable (.exe)

1. Install Python 3.9+ from https://www.python.org/downloads/
2. Double-click `build_exe.bat` to build the executable
3. Find the executable in the `dist` folder: `PC_Action_Timer.exe`
4. Run `PC_Action_Timer.exe` - no Python installation needed!

### Option C: Manual Build

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "PC_Action_Timer" timer_gui.py
```

The executable will be in the `dist` folder.

## Usage:

1. Select an action (Shutdown/Restart/Lock/Sleep)
2. Set the timer duration
3. Click "Start Timer"
4. Confirm the action
5. Cancel anytime before the timer expires

## Requirements:

- Windows OS only
- Python 3.9+ (for running .py files)
- No additional dependencies for GUI version

## Console Version Requirements:

If using `trunOFFpc.py`:

```bash
pip install colorama
```

## Troubleshooting:

### "pip not found" Error

If you get a "pip not found" error, try these solutions:

**Solution 1: Use python -m pip**
Instead of `pip install`, use:

```bash
python -m pip install pyinstaller
```

**Solution 2: Run the fix script**
Double-click `fix_pip.bat` to automatically fix pip installation.

**Solution 3: Manual pip installation**

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

After fixing pip, you can use `build_exe.bat` which now uses `python -m pip` automatically.

---

**Note:** This application is designed exclusively for Windows operating systems.
