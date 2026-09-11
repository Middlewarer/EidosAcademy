$ErrorActionPreference = 'Stop'

$projectDirectory = Split-Path -Parent $PSScriptRoot
$docker = 'C:\Program Files\Docker\Docker\resources\bin\docker.exe'

& $docker desktop start | Out-Null

$dockerReady = $false
for ($attempt = 0; $attempt -lt 36; $attempt++) {
    & $docker info *> $null
    if ($LASTEXITCODE -eq 0) {
        $dockerReady = $true
        break
    }
    Start-Sleep -Seconds 5
}

if (-not $dockerReady) {
    throw 'Docker Engine did not become ready within three minutes.'
}

Push-Location $projectDirectory
try {
    & $docker compose --env-file .env.production up -d
    if ($LASTEXITCODE -ne 0) {
        throw "Docker Compose failed with exit code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}
