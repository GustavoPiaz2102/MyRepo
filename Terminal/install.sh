#!/bin/bash

if ! command -v python3 &> /dev/null; then
	echo "Erro: Python 3 não encontrado. Por favor, instale-o antes de continuar."
	exit 1
fi

INSTALL_DIR="/opt/pokemon-catcher"
BIN_PATH="/usr/local/bin/pokemon-catcher"

echo "--- Iniciando Instalação do Pokemon Catcher ---"

sudo mkdir -p "$INSTALL_DIR"

sudo cp -r colorscripts pokemon.json PokemonCatcher.py "$INSTALL_DIR/"

sudo chmod +x "$INSTALL_DIR/PokemonCatcher.py"

sudo ln -sf "$INSTALL_DIR/PokemonCatcher.py" "$BIN_PATH"

echo "--- Instalação Concluída! ---"
echo "Comandos disponíveis:"
echo "  pokemon-catcher        -> Inicia um encontro"
echo "  pokemon-catcher -l     -> Abre sua Pokédex"
echo "  pokemon-catcher -t     -> Encontro versão pequena"