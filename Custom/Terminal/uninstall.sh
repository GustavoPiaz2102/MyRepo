#!/bin/bash

APP_NAME="pokemon-catcher"
INSTALL_DIR="/opt/$APP_NAME"
BIN_PATH="/usr/local/bin/$APP_NAME"
STATS_FILE="$HOME/.pokemon-player.json"

echo "--- Desinstalador do Pokemon Catcher ---"

# 1. Remove o link simbólico (comando global)
if [ -L "$BIN_PATH" ]; then
    echo "Removendo comando global em $BIN_PATH..."
    sudo rm "$BIN_PATH"
fi

# 2. Remove a pasta de instalação
if [ -d "$INSTALL_DIR" ]; then
    echo "Removendo arquivos em $INSTALL_DIR..."
    sudo rm -rf "$INSTALL_DIR"
fi

echo "-----------------------------------------------"
echo "O programa foi removido com sucesso."
echo ""
echo "Nota: O seu progresso (Pokédex e Nível) foi mantido em:"
echo "      $STATS_FILE"
echo "Se quiser apagar seu progresso permanentemente, rode:"
echo "      rm $STATS_FILE"
echo "-----------------------------------------------"