$ErrorActionPreference = "Stop"
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $ProjectDir
if (-not (Test-Path -LiteralPath "$ProjectDir\web-dist\index.html")) {
    Write-Host "Собираю интерфейс Eidos..."
    npm install
    npm run build
}
python "$ProjectDir\backend\server.py"
