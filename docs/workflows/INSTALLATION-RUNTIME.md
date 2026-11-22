# Installation & Runtime Bootstrap

current release makes PSE installable as a runtime rather than requiring users to work inside a framework checkout.

## Requirements

- Windows, macOS or Linux;
- Python 3.11 or newer;
- a TeX distribution providing LuaLaTeX;
- required LaTeX packages used by the core;
- the open-licensed Latin Modern fonts distributed by standard TeX installations.

PSE does not require manuscript source to leave the user's own machine or organization-controlled infrastructure.

## Standard installation from a checked-out release

```text
python -m pip install .
pse doctor
```

For development:

```text
python -m pip install -e .
```

The end-user runtime should normally be installed, not run through manual `PYTHONPATH` changes.

## Managed bootstrap scripts

For users who should not manage Python environments manually, the repository provides bootstrap scripts.

### macOS / Linux

```text
./scripts/bootstrap/unix-install.sh
```

The script installs PSE into `~/.pse/venv` by default and creates a launcher in `~/.local/bin`. `PSE_HOME` and `PSE_BIN_DIR` can override these locations.

### Windows

From PowerShell:

```text
.\scripts\bootstrap\windows-install.ps1
```

By default PSE is installed under `%LOCALAPPDATA%\PSE`. To add its launcher directory to the user PATH:

```text
.\scripts\bootstrap\windows-install.ps1 -AddToPath
```

The installer does not install a TeX distribution. Organizations may provision Python and TeX centrally using their normal endpoint-management tools.

## `pse doctor`

Run after installation and whenever a workstation behaves unexpectedly:

```text
pse doctor
```

Machine-readable output:

```text
pse doctor --json
```

Deeper secure-build test:

```text
pse doctor --deep
```

The lightweight doctor checks Python, CLI/runtime discovery, LuaLaTeX, required TeX packages where `kpsewhich` is available, the open font baseline, temporary write access and the safe-build policy. `--deep` additionally performs a temporary LuaLaTeX build and verifies that shell escape remains disabled.

## Severity

A missing runtime, Python version failure, missing LuaLaTeX, missing required TeX package or inability to write temporary build data is a required failure. Optional inspection capabilities such as `kpsewhich` are advisory warnings when unavailable.

`doctor` is a diagnostic tool, not a full book regression suite. A successful doctor does not prove that a particular manuscript or profile is editorially or typographically correct.

## Organizations

Publishing organizations may deploy PSE through managed Python environments, internal package repositories, signed installers or endpoint-management systems. current release defines the discovery contract but does not require a particular enterprise deployment technology.
