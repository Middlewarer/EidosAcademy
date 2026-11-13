$ErrorActionPreference = "Stop"
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Executable = Join-Path $ProjectDir "app\Eidos Focus.exe"
if (-not (Test-Path -LiteralPath $Executable)) { throw "Не найден исполняемый файл: $Executable" }
$Shell = New-Object -ComObject WScript.Shell

function New-EidosShortcut([string]$Path) {
    $Shortcut = $Shell.CreateShortcut($Path)
    $Shortcut.TargetPath = $Executable
    $Shortcut.WorkingDirectory = Split-Path -Parent $Executable
    $Shortcut.Description = "Eidos Focus — карьерный фокус"
    $Shortcut.Save()
}

New-EidosShortcut (Join-Path ([Environment]::GetFolderPath("Startup")) "Eidos Focus.lnk")
New-EidosShortcut (Join-Path ([Environment]::GetFolderPath("Desktop")) "Eidos Focus.lnk")
Write-Host "Ярлыки Eidos Focus созданы на рабочем столе и в автозагрузке."
