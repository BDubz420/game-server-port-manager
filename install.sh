#!/bin/bash
# Game Server Port Manager Install Script
# Author: BDubz
# Installs server_ports.py as /usr/local/bin/server-ports

set -e

SCRIPT_SRC="$(dirname "$0")/server_ports.py"
SCRIPT_DEST="/usr/local/bin/server-ports"

if [ ! -f "$SCRIPT_SRC" ]; then
    echo "Error: server_ports.py not found in the current directory."
    exit 1
fi

chmod +x "$SCRIPT_SRC"
cp "$SCRIPT_SRC" "$SCRIPT_DEST"
chmod +x "$SCRIPT_DEST"

if command -v server-ports >/dev/null 2>&1; then
    echo "\n✔ Game Server Port Manager installed successfully!"
    echo "Run 'server-ports' from anywhere."
else
    echo "\n✔ Installed, but 'server-ports' not found in PATH."
    echo "You may need to add /usr/local/bin to your PATH."
fi
