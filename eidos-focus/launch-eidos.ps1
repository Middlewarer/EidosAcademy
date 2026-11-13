$ErrorActionPreference = "SilentlyContinue"

$eidosExe = "D:\EidosAcademy\eidos-focus\app-ambient\Eidos Focus.exe"
$eidosFolder = Split-Path -Parent $eidosExe
$taskHelper = "D:\EidosAcademy\eidos-focus\task-helper.py"
$pythonw = "C:\Users\onmyf\AppData\Local\Programs\Python\Python314\pythonw.exe"

$running = @(Get-Process -Name "Eidos Focus" -ErrorAction SilentlyContinue)
if ($running.Count -gt 0) {
    $running | Stop-Process -Force
    Start-Sleep -Milliseconds 500
}

if (-not (Test-Path -LiteralPath $eidosExe)) {
    exit 2
}

$app = Start-Process -FilePath $eidosExe -WorkingDirectory $eidosFolder -ArgumentList "--show-widget" -PassThru

if ((Test-Path -LiteralPath $taskHelper) -and (Test-Path -LiteralPath $pythonw)) {
    Start-Sleep -Milliseconds 700
    Start-Process -FilePath $pythonw -WindowStyle Hidden -ArgumentList @($taskHelper, "--watch-pid", "$($app.Id)")
}
