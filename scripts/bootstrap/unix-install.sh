#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
PYTHON=${PYTHON:-python3}
BASE=${PSE_HOME:-"$HOME/.pse"}
VENV="$BASE/venv"
BIN=${PSE_BIN_DIR:-"$HOME/.local/bin"}

command -v "$PYTHON" >/dev/null 2>&1 || { echo "Python 3 is required." >&2; exit 1; }
"$PYTHON" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)' || { echo "PSE requires Python 3.11 or newer." >&2; exit 1; }

mkdir -p "$BASE" "$BIN"
"$PYTHON" -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install "$ROOT"
cat > "$BIN/pse" <<LAUNCHER
#!/usr/bin/env sh
exec "$VENV/bin/pse" "\$@"
LAUNCHER
chmod +x "$BIN/pse"

echo "PSE installed in: $VENV"
echo "Launcher: $BIN/pse"
case ":${PATH}:" in
  *:"$BIN":*) ;;
  *) echo "NOTE: add $BIN to your PATH to run 'pse' directly." ;;
esac
"$VENV/bin/pse" doctor || true
