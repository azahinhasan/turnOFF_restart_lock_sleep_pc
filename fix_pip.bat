@echo off
echo ========================================
echo Fixing pip installation
echo ========================================
echo.

echo Checking Python installation...
python --version
echo.

echo Installing/Upgrading pip...
python -m ensurepip --upgrade
echo.

echo Upgrading pip to latest version...
python -m pip install --upgrade pip
echo.

echo ========================================
echo Testing pip...
echo ========================================
python -m pip --version
echo.

echo ========================================
echo pip is now ready to use!
echo ========================================
echo.
echo You can now use: python -m pip install [package]
echo Or simply: pip install [package]
echo.
pause
