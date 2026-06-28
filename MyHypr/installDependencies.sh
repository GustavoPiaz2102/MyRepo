#!/bin/bash

echo "==> Iniciando a configuração do ambiente Hyprland + Quickshell..."

# 1. Sincronização e atualização da base do sistema
echo "==> Atualizando os pacotes do sistema..."
sudo pacman -Syu --noconfirm

# 2. Instalação das dependências oficiais (Core, QML e CLI tools da barra)
echo "==> Instalando pacotes dos repositórios oficiais..."
sudo pacman -S --needed --noconfirm \
    hyprland \
    kitty \
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
    git \
    base-devel

# 3. Instalação do Quickshell via AUR
echo "==> Procurando por um AUR helper (yay ou paru)..."
if command -v yay &> /dev/null; then
    echo "==> yay encontrado. Instalando Quickshell..."
    yay -S --needed --noconfirm quickshell-git
elif command -v paru &> /dev/null; then
    echo "==> paru encontrado. Instalando Quickshell..."
    paru -S --needed --noconfirm quickshell-git
else
    echo "==> [AVISO] Nenhum AUR helper detectado."
    echo "==> Você precisará compilar e instalar o 'quickshell' manualmente."
fi

# 4. Trava de segurança da versão do Hyprland
echo "==> Aplicando trava de versão no pacman.conf..."
if ! grep -q "IgnorePkg.*hyprland" /etc/pacman.conf; then
    # Procura a linha comentada do IgnorePkg e insere a regra logo abaixo
    sudo sed -i '/^#IgnorePkg/a IgnorePkg = hyprland' /etc/pacman.conf
    echo "==> Hyprland adicionado ao IgnorePkg com sucesso."
else
    echo "==> Hyprland já está no IgnorePkg."
fi

# 5. Habilitando serviços básicos (Bluetooth e Rede)
echo "==> Habilitando serviços do sistema..."
sudo systemctl enable --now NetworkManager
sudo systemctl enable --now bluetooth

echo "==> Instalação concluída! O sistema está pronto para receber o clone dos seus dotfiles."
