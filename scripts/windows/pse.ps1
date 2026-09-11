$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$env:PYTHONPATH = "$Root\tools" + $(if ($env:PYTHONPATH) { ";$env:PYTHONPATH" } else { "" })
python -m pse_cli.cli @args
exit $LASTEXITCODE
