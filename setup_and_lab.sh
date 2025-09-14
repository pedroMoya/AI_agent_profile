#!/bin/bash
set -e

cd /mnt/d/sandbox_workshop || { echo "No existe /mnt/d/sandbox_workshop"; exit 1; }

# Si no hay venv, intenta crear uno (con venv del sistema)
if [ ! -d ".venv" ]; then
  if ! dpkg -s python3-venv >/dev/null 2>&1; then
    echo "[i] Instalando python3-venv (requiere sudo)..."
    sudo apt update
    sudo apt install -y python3-venv
  fi
  echo "[i] Creando entorno .venv..."
  python3 -m venv .venv
fi

# Activar venv
source .venv/bin/activate

# pip y deps
python -m pip install --upgrade pip wheel
if [ -f requirements_min.txt ]; then
  pip install -r requirements_min.txt
fi

# Asegurar jupyterlab e ipykernel
python -c "import jupyterlab" 2>/dev/null || pip install jupyterlab
python -c "import ipykernel" 2>/dev/null || pip install ipykernel

# Registrar kernel apuntando a ESTE venv
python -m ipykernel install --user --name sandbox_workshop --display-name "Python (sandbox_workshop)"

echo "[i] Kernel registrado. Abriendo Jupyter Lab..."
exec jupyter lab
