@echo off
setlocal
cd /d "%~dp0washcut-agent-demo"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0washcut-agent-demo\scripts\start-public-test.ps1"
if errorlevel 1 pause
endlocal
