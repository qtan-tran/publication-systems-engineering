---
title: Install and Check PSE
description: Install a checked-out PSE candidate and verify the local Python and LuaLaTeX runtime.
---

# Install and check PSE

PSE currently targets Windows, macOS, and Linux. You need **Python 3.11 or newer** and a TeX distribution that provides **LuaLaTeX**. PSE's installer does not install a TeX distribution for you.

## Install from the checked-out repository

Open a terminal in the PSE repository root and run:

```text
python -m pip install .
pse doctor --deep
```

`pse doctor --deep` checks the installed runtime and performs a temporary secure LuaLaTeX build. Continue only after required checks pass. Advisory warnings about optional inspection tools are different from required failures.

## Managed bootstrap option

If you do not want to manage a Python environment manually, the repository also provides bootstrap scripts. On macOS/Linux, from the repository root:

```text
./scripts/bootstrap/unix-install.sh
```

On Windows PowerShell:

```text
.\scripts\bootstrap\windows-install.ps1 -AddToPath
```

After either route, run:

```text
pse doctor --deep
```

## What success means

A successful doctor tells you that the workstation can run the PSE baseline safely. It does **not** certify a particular manuscript, layout, or final PDF. Those checks happen at project level.

Next: [Choose a book profile](choose-a-profile.md).
