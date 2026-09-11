# Synthetic Basic Book

This is the core smoke fixture for Publication Systems Engineering.

It contains synthetic prose only. It exists to verify the minimal lifecycle:

```text
book.yml → metadata validation → pse-core → LuaLaTeX → PDF → QA
```

From the repository root:

```bash
python -m pse_cli.cli clean examples/synthetic/basic-book
python -m pse_cli.cli build examples/synthetic/basic-book
python -m pse_cli.cli check examples/synthetic/basic-book
```

When the package is installed in editable mode (`python -m pip install -e .`), use `pse` instead of `python -m pse_cli.cli`.
