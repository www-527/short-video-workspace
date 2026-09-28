@echo off
setlocal EnableExtensions

set "PROJECT_DIR=%~dp0washcut-agent-demo"
set "WEB_PORT_FILE=%TEMP%\washcut-agent-demo-web.port"
set "HEALTH_URL=http://127.0.0.1:8787/api/health"
set "QWEN_ACTIVATE_URL=http://127.0.0.1:8787/api/transcription/activate"
set "NO_BROWSER="
set "DOCKER_READY="

if /I "%~1"=="--no-browser" set "NO_BROWSER=1"

if not exist "%PROJECT_DIR%\package.json" (
  echo [ERROR] Project not found: %PROJECT_DIR%
  pause
  exit /b 1
)

set "PNPM_EXE="
for /f "delims=" %%P in ('where pnpm.cmd 2^>nul') do if not defined PNPM_EXE set "PNPM_EXE=%%P"

if not defined PNPM_EXE (
  set "PNPM_EXE=C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\bin\fallback\pnpm.cmd"
)

if not exist "%PNPM_EXE%" (
  echo [ERROR] pnpm was not found. Add pnpm to PATH or run this project in Codex first.
  pause
  exit /b 1
)

set "DOCKER_EXE="
for /f "delims=" %%D in ('where docker.exe 2^>nul') do if not defined DOCKER_EXE set "DOCKER_EXE=%%D"
if not defined DOCKER_EXE if exist "%LOCALAPPDATA%\Programs\DockerDesktop\resources\bin\docker.exe" set "DOCKER_EXE=%LOCALAPPDATA%\Programs\DockerDesktop\resources\bin\docker.exe"
if not defined DOCKER_EXE if exist "%ProgramFiles%\Docker\Docker\resources\bin\docker.exe" set "DOCKER_EXE=%ProgramFiles%\Docker\Docker\resources\bin\docker.exe"

if defined DOCKER_EXE (
  "%DOCKER_EXE%" info >nul 2>&1
  if errorlevel 1 (
    echo [WARNING] Docker is installed but the engine is not ready. Start Docker Desktop, then restart this program.
  ) else (
    set "DOCKER_READY=1"
    echo [READY] Docker engine is available.
  )
) else (
  echo [WARNING] Docker was not found. Install or start Docker Desktop, then restart this program to load Qwen automatically.
)

if not exist "%PROJECT_DIR%\node_modules" (
  echo [FIRST RUN] Installing dependencies...
  pushd "%PROJECT_DIR%"
  call "%PNPM_EXE%" install
  if errorlevel 1 (
    popd
    echo [ERROR] Dependency installation failed.
    pause
    exit /b 1
  )
  popd
)

call :RESOLVE_WEB_TARGET
if errorlevel 1 (
  pause
  exit /b 1
)
set "WASHCUT_WEB_PORT=%WEB_PORT%"

call :CHECK_WEB
if errorlevel 1 goto :CHECK_BACKEND

curl.exe -fsS "%HEALTH_URL%" >nul 2>&1
if errorlevel 1 goto :START_BACKEND
goto :OPEN_APP

:CHECK_BACKEND
curl.exe -fsS "%HEALTH_URL%" >nul 2>&1
if errorlevel 1 goto :START_ALL

echo [STARTING] The API is running; launching the missing web app...
start "Washcut Agent Demo - Web" /D "%PROJECT_DIR%" cmd.exe /k ""%PNPM_EXE%" dev:web"
goto :WAIT_FOR_SERVICES

:START_BACKEND
echo [STARTING] The web app is running; launching the missing API...
start "Washcut Agent Demo - API" /D "%PROJECT_DIR%" cmd.exe /k ""%PNPM_EXE%" dev:server"
goto :WAIT_FOR_SERVICES

:START_ALL
echo [STARTING] Launching Washcut Agent Demo...
start "Washcut Agent Demo" /D "%PROJECT_DIR%" cmd.exe /k ""%PNPM_EXE%" dev"

:WAIT_FOR_SERVICES
for /L %%I in (1,1,30) do (
  call :CHECK_SERVICES
  if not errorlevel 1 goto :OPEN_APP
  timeout /t 1 /nobreak >nul
)

echo [ERROR] Services did not become ready in 30 seconds. Check the Washcut Agent Demo window.
pause
exit /b 1

:OPEN_APP
if defined DOCKER_READY call :LOAD_QWEN
echo [READY] Washcut Agent Demo is running at %APP_URL%
if not defined NO_BROWSER start "" "%APP_URL%"
exit /b 0

:LOAD_QWEN
set "QWEN_RESPONSE=%TEMP%\washcut-qwen-startup-%RANDOM%-%RANDOM%.json"
echo [STARTING] Loading Qwen3-ASR and ForcedAligner...
curl.exe -sS --fail-with-body -X POST "%QWEN_ACTIVATE_URL%" -H "Content-Type: application/json" -H "x-tenant-id: tenant_demo" -H "x-user-id: user_demo" -H "x-role: producer" --data "{\"providerId\":\"qwen3-asr\"}" >"%QWEN_RESPONSE%" 2>&1
if errorlevel 1 (
  echo [WARNING] Qwen could not be loaded automatically. Confirm Docker Desktop is running, then use Settings - Transcription model - Reload.
  if exist "%QWEN_RESPONSE%" type "%QWEN_RESPONSE%"
  if exist "%QWEN_RESPONSE%" del /q "%QWEN_RESPONSE%"
  exit /b 0
)
if exist "%QWEN_RESPONSE%" del /q "%QWEN_RESPONSE%"
echo [READY] Qwen transcription model is loaded.
exit /b 0

:CHECK_SERVICES
call :CHECK_WEB
if errorlevel 1 exit /b 1
curl.exe -fsS "%HEALTH_URL%" >nul 2>&1
if errorlevel 1 exit /b 1
exit /b 0

:CHECK_WEB
curl.exe -fsS "%APP_URL%" 2>nul | findstr.exe /C:"washcut-agent-demo" >nul
exit /b %errorlevel%

:RESOLVE_WEB_TARGET
set "WEB_PORT="
if exist "%WEB_PORT_FILE%" set /p "WEB_PORT="<"%WEB_PORT_FILE%"
if defined WEB_PORT (
  set "APP_URL=http://127.0.0.1:%WEB_PORT%/"
  call :CHECK_WEB
  if not errorlevel 1 (
    echo [READY] Reusing the existing Washcut web app on port %WEB_PORT%.
    exit /b 0
  )
)

set "WEB_PORT="
for /f "usebackq delims=" %%P in (`powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%PROJECT_DIR%\scripts\find-available-web-port.ps1"`) do if not defined WEB_PORT set "WEB_PORT=%%P"
if not defined WEB_PORT (
  echo [ERROR] No available web port was found between 5173 and 5273.
  exit /b 1
)

set "APP_URL=http://127.0.0.1:%WEB_PORT%/"
>"%WEB_PORT_FILE%" echo %WEB_PORT%
echo [READY] Selected available web port %WEB_PORT%.
exit /b 0
