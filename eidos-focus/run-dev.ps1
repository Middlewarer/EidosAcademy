$ErrorActionPreference = "Stop"
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $ProjectDir
Start-Process -WindowStyle Hidden python -ArgumentList @("$ProjectDir\backend\server.py", "--server-only")
npm run dev
