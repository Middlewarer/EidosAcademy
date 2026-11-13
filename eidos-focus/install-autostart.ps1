$ErrorActionPreference = "Stop"
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Executable = Join-Path $ProjectDir "app\Eidos Focus.exe"
if (-not (Test-Path -LiteralPath $Executable)) {
    throw "Не найден исполняемый файл: $Executable"
}
$StartupDir = [Environment]::GetFolderPath("Startup")
$ShortcutPath = Join-Path $StartupDir "Eidos Focus.lnk"
$Shell = New-Object -ComObject WScript.Shell
$Shortcut = $Shell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $Executable
$Shortcut.WorkingDirectory = Split-Path -Parent $Executable
$Shortcut.Description = "Eidos Focus — startup dashboard"
$Shortcut.Save()
Write-Host "Автозапуск Eidos Focus включён: $ShortcutPath"
