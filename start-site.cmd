@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0deployment\start-eidosacademy.ps1"
if errorlevel 1 (
    echo.
    echo EidosAcademy failed to start. See the error above.
    pause
)
