@echo off
REM Simple startup script - runs servers in background

cd /d "%~dp0backend"
start /min cmd /c "python -m app.main"

cd /d "%~dp0frontend"
start /min cmd /c "python -m http.server 8000"

timeout /t 3 /nobreak >nul
start http://localhost:8000

echo Backend: http://localhost:5000
echo Frontend: http://localhost:8000
echo.
echo Servers are running in the background.
echo Run stop.bat to stop all servers.
