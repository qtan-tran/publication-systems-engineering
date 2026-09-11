param(
  [switch]$AddToPath
)
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$Base = if ($env:PSE_HOME) { $env:PSE_HOME } else { Join-Path $env:LOCALAPPDATA "PSE" }
$Venv = Join-Path $Base "venv"
$Bin = Join-Path $Base "bin"

if (Get-Command py -ErrorAction SilentlyContinue) {
  & py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)"
  if ($LASTEXITCODE -ne 0) { throw "PSE requires Python 3.11 or newer." }
  $CreateVenv = { param($Path) & py -3 -m venv $Path }
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  & python -c "import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)"
  if ($LASTEXITCODE -ne 0) { throw "PSE requires Python 3.11 or newer." }
  $CreateVenv = { param($Path) & python -m venv $Path }
} else {
  throw "Python 3.11 or newer is required."
}

New-Item -ItemType Directory -Force -Path $Base, $Bin | Out-Null
& $CreateVenv $Venv
$Vpy = Join-Path $Venv "Scripts\python.exe"
& $Vpy -m pip install --upgrade pip
& $Vpy -m pip install $Root
$Launcher = Join-Path $Bin "pse.cmd"
$PseExe = Join-Path $Venv "Scripts\pse.exe"
"@echo off`r`n`"$PseExe`" %*`r`n" | Set-Content -Encoding ASCII $Launcher

if ($AddToPath) {
  $UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
  $Parts = @($UserPath -split ';' | Where-Object { $_ })
  if ($Parts -notcontains $Bin) {
    [Environment]::SetEnvironmentVariable("Path", (($Parts + $Bin) -join ';'), "User")
    Write-Host "Added $Bin to your user PATH. Open a new terminal before using 'pse'."
  }
}
Write-Host "PSE installed in: $Venv"
Write-Host "Launcher: $Launcher"
if (-not $AddToPath) { Write-Host "Run again with -AddToPath if you want the installer to add the launcher directory to your user PATH." }
& $PseExe doctor
