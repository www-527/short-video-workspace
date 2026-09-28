@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0washcut-agent-demo\scripts\stop-public-test.ps1"
echo.
pause
endlocal
