$ErrorActionPreference = 'Stop'
try {
    $capability = Get-WindowsCapability -Online -Name 'OpenSSH.Server*'
    if ($capability.State -ne 'Installed') {
        Add-WindowsCapability -Online -Name $capability.Name | Out-Null
    }
    Set-Service sshd -StartupType Automatic
    Start-Service sshd
    Get-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -ErrorAction SilentlyContinue | Disable-NetFirewallRule
    if (-not (Get-NetFirewallRule -Name 'EidosAcademy-SSH-VPN' -ErrorAction SilentlyContinue)) {
        New-NetFirewallRule -Name 'EidosAcademy-SSH-VPN' -DisplayName 'EidosAcademy SSH via Radmin VPN' -Direction Inbound -Action Allow -Protocol TCP -LocalPort 22 -InterfaceAlias 'Radmin VPN' -RemoteAddress '26.0.0.0/8' -Profile Any | Out-Null
    }
    'SSH_READY' | Set-Content (Join-Path $PSScriptRoot 'ssh-setup.local')
} catch {
    $_.Exception.Message | Set-Content (Join-Path $PSScriptRoot 'ssh-setup.local')
    throw
}
