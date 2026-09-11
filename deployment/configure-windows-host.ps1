$ErrorActionPreference = 'Stop'

powercfg /change standby-timeout-ac 0

$windowsFeatures = @(
    'Microsoft-Windows-Subsystem-Linux',
    'VirtualMachinePlatform'
)

foreach ($feature in $windowsFeatures) {
    $dism = Start-Process `
        -FilePath "$env:SystemRoot\System32\dism.exe" `
        -ArgumentList '/Online', '/Enable-Feature', "/FeatureName:$feature", '/All', '/NoRestart' `
        -Wait `
        -PassThru `
        -WindowStyle Hidden

    if ($dism.ExitCode -notin 0, 3010) {
        throw "Failed to enable Windows feature $feature (DISM exit code $($dism.ExitCode))."
    }
}

bcdedit /set hypervisorlaunchtype auto | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Failed to enable the Windows hypervisor at boot (bcdedit exit code $LASTEXITCODE)."
}

$firewallRules = @(
    @{ Name = 'EidosAcademy HTTP'; Port = 80 },
    @{ Name = 'EidosAcademy HTTPS'; Port = 443 }
)

foreach ($rule in $firewallRules) {
    if (-not (Get-NetFirewallRule -DisplayName $rule.Name -ErrorAction SilentlyContinue)) {
        New-NetFirewallRule `
            -DisplayName $rule.Name `
            -Direction Inbound `
            -Action Allow `
            -Protocol TCP `
            -LocalPort $rule.Port `
            -Profile Any | Out-Null
    }
}

$runKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
$dockerDesktop = '"C:\Program Files\Docker\Docker\Docker Desktop.exe" -Autostart'
New-ItemProperty `
    -Path $runKey `
    -Name 'Docker Desktop' `
    -Value $dockerDesktop `
    -PropertyType String `
    -Force | Out-Null

$startupScript = Join-Path $PSScriptRoot 'start-eidosacademy.ps1'
$startupAction = New-ScheduledTaskAction `
    -Execute 'powershell.exe' `
    -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$startupScript`""
$startupTrigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
Register-ScheduledTask `
    -TaskName 'EidosAcademyStartup' `
    -Action $startupAction `
    -Trigger $startupTrigger `
    -Description 'Start Docker Desktop and EidosAcademy after Windows logon.' `
    -Force | Out-Null

Write-Host 'Windows host configuration completed.'
