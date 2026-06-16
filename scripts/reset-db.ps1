$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$DbPath = Join-Path $Root "backend\instance\elevator_maintenance.db"

if (Test-Path $DbPath) {
  Remove-Item -LiteralPath $DbPath -Force
  Write-Host "Removed $DbPath"
}

python -c "import sys; sys.path.insert(0, 'backend'); from app import create_app; create_app(); print('Database initialized')"
