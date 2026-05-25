@echo off
cd /d "%~dp0"
echo Starting Spam Checker at http://127.0.0.1:8000
echo A server window will open. Keep it open while using the website.

set "CODEX_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%CODEX_PYTHON%" (
  start "Spam Checker Server" cmd /k ""%CODEX_PYTHON%" web_app.py"
  timeout /t 2 >nul
  start "" "http://127.0.0.1:8000"
  goto done
)

where python >nul 2>nul
if %errorlevel%==0 (
  start "Spam Checker Server" cmd /k "python web_app.py"
  timeout /t 2 >nul
  start "" "http://127.0.0.1:8000"
  goto done
)

py -3 --version >nul 2>nul
if %errorlevel%==0 (
  start "Spam Checker Server" cmd /k "py -3 web_app.py"
  timeout /t 2 >nul
  start "" "http://127.0.0.1:8000"
  goto done
)

echo.
echo Python is not installed or is not available on PATH.
echo Install Python 3 from https://www.python.org/downloads/
echo During installation, select "Add python.exe to PATH".

:done
pause
