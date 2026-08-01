#!/bin/bash

echo "==> Iniciando a configuração do ambiente Hyprland + Tide-island..."

# 1. Sincronização e atualização da base do sistema
echo "==> Atualizando os pacotes do sistema..."
sudo pacman -Syu --noconfirm

# 2. Instalação das dependências oficiais (Core, QML, tema e CLI tools)
echo "==> Instalando pacotes dos repositórios oficiais..."
sudo pacman -S --needed --noconfirm \
    hyprland \
    kitty \
    dolphin \
    cava \
    upower \
    wireplumber \
    networkmanager \
    bluez \
    bluez-utils \
    ttf-jetbrains-mono-nerd \
    qt6-wayland \
    qt6-declarative \
    qt6-svg \
    python \
    python-pillow \
    python-numpy \
    git \
    cmake \
    ninja \
    base-devel

# 3. Instalação das dependências via AUR (awww, grimblast, chrome)
echo "==> Procurando por um AUR helper (yay ou paru)..."
if command -v yay &> /dev/null; then
    AUR_HELPER="yay"
elif command -v paru &> /dev/null; then
    AUR_HELPER="paru"
else
    AUR_HELPER=""
fi

if [ -n "$AUR_HELPER" ]; then
    echo "==> $AUR_HELPER encontrado. Instalando pacotes do AUR..."
    $AUR_HELPER -S --needed --noconfirm awww-git grimblast-git google-chrome
else
    echo "==> [AVISO] Nenhum AUR helper detectado (yay/paru)."
    echo "==> Instale manualmente: awww-git, grimblast-git, google-chrome."
fi

# 4. Quickshell + tide-island (build a partir do código-fonte)
#    O Quickshell não vem do AUR neste setup: é compilado e instalado junto
#    com o tide-island pelo instalador oficial em Tide-island/install.sh.
echo "==> Instalando Quickshell + tide-island a partir do código-fonte..."
if [ -x "$HOME/git/Tide-island/install.sh" ]; then
    (cd "$HOME/git/Tide-island" && ./install.sh)
else
    echo "==> [AVISO] Não encontrei ~/git/Tide-island/install.sh."
    echo "==> Clone https://github.com/GustavoPiaz2102/Tide-island (ou o repo correspondente)"
    echo "==> e rode o install.sh para compilar o Quickshell e instalar o tide-island."
fi

# 5. Habilitando serviços básicos (Bluetooth e Rede)
echo "==> Habilitando serviços do sistema..."
sudo systemctl enable --now NetworkManager
sudo systemctl enable --now bluetooth

# 6. Script de tema por wallpaper (kitty/GTK/Neovim/Hyprland)
echo "==> Instalando script de tema (wallpaper-theme.sh)..."
mkdir -p "$HOME/.config/scripts"
cp -f "$(dirname "$0")/wallpaper-theme.sh" "$HOME/.config/scripts/wallpaper-theme.sh"
chmod +x "$HOME/.config/scripts/wallpaper-theme.sh"

# 7. Copiando as confs do repo para os respectivos diretórios
echo "==> Copiando confs/kitty/kitty.conf e confs/hypr/hyprland.conf..."
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$HOME/.config/kitty" "$HOME/.config/hypr"
cp -f "$REPO_DIR/confs/kitty/kitty.conf" "$HOME/.config/kitty/kitty.conf"
cp -f "$REPO_DIR/confs/hypr/hyprland.conf" "$HOME/.config/hypr/hyprland.conf"

echo "==> Instalação concluída! O sistema está pronto para receber o clone dos seus dotfiles."
echo "==> Lembre-se de configurar o campo 'wallpaperCustomCommand' em"
echo "    ~/.config/tide-island/userconfig.json para:"
echo '    bash ~/.config/scripts/wallpaper-theme.sh "$1" "$2"'
