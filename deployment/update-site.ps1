$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
if (git status --porcelain) { throw 'Server has uncommitted changes. Commit or resolve them before deployment.' }
if ((git branch --show-current) -ne 'Main') { throw 'Expected Main branch.' }
git pull --ff-only origin Main
if ($LASTEXITCODE -ne 0) { throw 'Git pull failed.' }
$backupDirectory = Join-Path (Get-Location) 'backups'
New-Item -ItemType Directory -Force -Path $backupDirectory | Out-Null
$backupName = 'database-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.dump'
docker compose --env-file .env.production exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc -f /tmp/eidos-backup.dump'
if ($LASTEXITCODE -ne 0) { throw 'Database backup failed; deployment stopped.' }
docker compose --env-file .env.production cp db:/tmp/eidos-backup.dump (Join-Path $backupDirectory $backupName)
if ($LASTEXITCODE -ne 0) { throw 'Backup copy failed; deployment stopped.' }
docker compose --env-file .env.production up -d --build
if ($LASTEXITCODE -ne 0) { throw 'Deployment failed; inspect Docker logs.' }
docker compose --env-file .env.production ps
