@echo off
echo ========================================
echo Building PC Action Timer GUI Executable
echo ========================================
echo.

echo Installing PyInstaller...
python -m pip install pyinstaller
echo.

echo Building executable...
python -m PyInstaller --onefile --windowed --name "PC_Action_Timer" --icon=plug.ico timer_gui.py
echo.

echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Your executable is located in the 'dist' folder
echo File: dist\PC_Action_Timer.exe
echo.
pause
