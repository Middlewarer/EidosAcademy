@echo off
cd /d "%~dp0learning_tracker"
if exist "..\.venv-deploy-check\Scripts\pythonw.exe" (
    "..\.venv-deploy-check\Scripts\pythonw.exe" launch.py %*
) else if exist "..\.venv-deploy-check\Scripts\python.exe" (
    "..\.venv-deploy-check\Scripts\python.exe" launch.py %*
) else if exist "%LocalAppData%\Programs\Python\Python314\pythonw.exe" (
    "%LocalAppData%\Programs\Python\Python314\pythonw.exe" launch.py %*
) else (
    pythonw launch.py %*
)
