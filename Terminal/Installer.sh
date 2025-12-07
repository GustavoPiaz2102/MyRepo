#!/usr/bin/env bash

set -e

if [ -n "$TERMUX_VERSION" ]; then
    INSTALL_CMD="pkg install -y"
    HAS_SUDO=false
else
    INSTALL_CMD="sudo apt install -y"
    HAS_SUDO=true
fi

if command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
else
    $INSTALL_CMD python
    PYTHON="python3"
fi

if ! $PYTHON -m pip --version >/dev/null 2>&1; then
    $INSTALL_CMD python-pip
fi

$INSTALL_CMD neofetch
$INSTALL_CMD fish

$PYTHON -m pip install --user requests

NEOFETCH_DIR="$HOME/.config/neofetch"
mkdir -p "$NEOFETCH_DIR"

for file in bitcoin.py wallet.py minha_ascii.txt config.conf; do
    if [ -f "./$file" ]; then
        mv "./$file" "$NEOFETCH_DIR/"
    fi
done

FISH_CONFIG_DIR="$HOME/.config/fish"
mkdir -p "$FISH_CONFIG_DIR"

if [ -f "./config.fish" ]; then
    mv "./config.fish" "$FISH_CONFIG_DIR/"
fi

if [ "$HAS_SUDO" = true ]; then
    chsh -s "$(which fish)"
fi
