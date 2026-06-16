param(
  [int]$BackendPort = 18033,
  [int]$FrontendPort = 19024
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$LogDir = Join-Path $Root ".logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Test-PythonDeps($PythonExe) {
  & $PythonExe -c "import flask, flask_cors, flask_sqlalchemy, sqlalchemy" *> $null
  return $LASTEXITCODE -eq 0
}

$PythonExe = "python"
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
if ((Test-Path $VenvPython) -and (Test-PythonDeps $VenvPython)) {
  $PythonExe = $VenvPython
} elseif (-not (Test-PythonDeps "python")) {
  Write-Host "Backend dependencies are missing."
  Write-Host "Run: python -m pip install -r backend\requirements.txt"
  exit 1
}

$env:PORT = "$BackendPort"
$env:FLASK_DEBUG = "0"
$env:VITE_API_PROXY = "http://127.0.0.1:$BackendPort"

$BackendOut = Join-Path $LogDir "backend.out.log"
$BackendErr = Join-Path $LogDir "backend.err.log"
$FrontendOut = Join-Path $LogDir "frontend.out.log"
$FrontendErr = Join-Path $LogDir "frontend.err.log"

$Backend = Start-Process -PassThru -WindowStyle Hidden `
  -FilePath $PythonExe `
  -ArgumentList @("backend\run.py") `
  -WorkingDirectory $Root `
  -RedirectStandardOutput $BackendOut `
  -RedirectStandardError $BackendErr

$Frontend = Start-Process -PassThru -WindowStyle Hidden `
  -FilePath "npm.cmd" `
  -ArgumentList @("run", "dev", "--", "--host", "127.0.0.1", "--port", "$FrontendPort") `
  -WorkingDirectory (Join-Path $Root "frontend") `
  -RedirectStandardOutput $FrontendOut `
  -RedirectStandardError $FrontendErr

Start-Sleep -Seconds 4

try {
  $Health = Invoke-WebRequest -UseBasicParsing "http://127.0.0.1:$BackendPort/api/health" -TimeoutSec 10
  $FrontendHome = Invoke-WebRequest -UseBasicParsing "http://127.0.0.1:$FrontendPort" -TimeoutSec 10
  Write-Host "Backend PID: $($Backend.Id), health: $($Health.StatusCode)"
  Write-Host "Frontend PID: $($Frontend.Id), page: $($FrontendHome.StatusCode)"
  Write-Host "Open: http://127.0.0.1:$FrontendPort"
  Write-Host "Logs: $LogDir"
} catch {
  Write-Host "Startup check failed: $($_.Exception.Message)"
  Write-Host "Backend log: $BackendErr"
  Write-Host "Frontend log: $FrontendErr"
  exit 1
}
