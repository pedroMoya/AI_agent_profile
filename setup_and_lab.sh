#!/bin/bash
set -e

cd /mnt/d/sandbox_workshop || { echo "Directory /mnt/d/sandbox_workshop does not exist"; exit 1; }

# If there is no venv, try to create one (using system venv)
if [ ! -d ".venv" ]; then
  if ! dpkg -s python3-venv >/dev/null 2>&1; then
    echo "[i] Installing python3-venv (requires sudo)..."
    sudo apt update
    sudo apt install -y python3-venv
  fi
  echo "[i] Creating .venv environment..."
  python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# pip and dependencies
python -m pip install --upgrade pip wheel
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi

# Ensure jupyterlab and ipykernel
python -c "import jupyterlab" 2>/dev/null || pip install jupyterlab
python -c "import ipykernel" 2>/dev/null || pip install ipykernel

# Register kernel pointing to THIS venv
python -m ipykernel install --user --name sandbox_workshop --display-name "Python (sandbox_workshop)"

echo "[i] Kernel registered. Launching Jupyter Lab..."
exec jupyter lab
