-- hyprland.lua
-- Convertido a partir do hyprland.conf (sintaxe hyprlang antiga)
-- Ref: https://wiki.hypr.land/Configuring/Start/

-------------------------------
---- ENVIRONMENT VARIABLES ----
-------------------------------
hl.env("XDG_DATA_DIRS", "/home/gustavo/.local/share/flatpak/exports/share:/var/lib/flatpak/exports/share:/usr/local/share:/usr/share")

---------------------
---- MY PROGRAMS ----
---------------------
local mainMod       = "SUPER"
local terminal       = "kitty"
local fileManager    = "dolphin"
local menu           = "hyprlauncher"
local nav            = "google-chrome-stable"
local wallpaperBnd   = "/tmp/qs-wallpaper-toggle"

-------------------
---- AUTOSTART ----
-------------------
-- Regra de layer que antes era chamada via `hyprctl keyword "hl.layer_rule(...)"`
-- agora é só uma chamada direta na config lua.
hl.layer_rule({
    match = { namespace = "bar-0" },
    on_demand_exclusive = false,
})

hl.on("hyprland.start", function()
    hl.exec_cmd("awww-daemon")
    -- hl.exec_cmd("quickshell")
    hl.exec_cmd("/usr/bin/tide-island")
end)

-----------------------
---- LOOK AND FEEL ----
-----------------------
hl.config({
    general = {
        gaps_in = 0,
        gaps_out = 0,
        border_size = 1,
    },
    decoration = {
        rounding = 18,
    },
    input = {
        kb_layout = "br",
    },
})

---------------------
---- KEYBINDINGS ----
---------------------

-- Apps
hl.bind(mainMod .. " + Q", hl.dsp.exec_cmd(terminal))
hl.bind("CTRL + ALT + T", hl.dsp.exec_cmd(terminal))
hl.bind("CTRL + ALT + E", hl.dsp.exec_cmd(nav))
hl.bind(mainMod .. " + E", hl.dsp.exec_cmd(fileManager))
hl.bind(mainMod .. " + R", hl.dsp.exec_cmd(menu))
hl.bind(mainMod .. " + W", hl.dsp.exec_cmd("touch " .. wallpaperBnd))
hl.bind("Print", hl.dsp.exec_cmd("grimblast copy area"))
hl.bind(mainMod .. " + SHIFT + S", hl.dsp.exec_cmd("grimblast copy area"))

-- Window management
hl.bind("ALT + F4", hl.dsp.window.close())
hl.bind(mainMod .. " + V", hl.dsp.window.float({ action = "toggle" }))
hl.bind(mainMod .. " + M", hl.dsp.exec_cmd(
    "command -v hyprshutdown >/dev/null 2>&1 && hyprshutdown || hyprctl dispatch 'hl.dsp.exit()'"
))
hl.bind("SUPER + P", hl.dsp.window.move({ monitor = "Virtual-1" }))
hl.bind("SUPER + O", hl.dsp.window.move({ monitor = "HDMI-A-1" }))

-- Focus
hl.bind(mainMod .. " + left",  hl.dsp.focus({ direction = "left" }))
hl.bind(mainMod .. " + right", hl.dsp.focus({ direction = "right" }))
hl.bind(mainMod .. " + up",    hl.dsp.focus({ direction = "up" }))
hl.bind(mainMod .. " + down",  hl.dsp.focus({ direction = "down" }))

-- Workspaces
hl.bind("ALT + Tab",         hl.dsp.focus({ workspace = "e+1" }))
hl.bind("ALT + SHIFT + Tab", hl.dsp.focus({ workspace = "e-1" }))

for i = 1, 5 do
    hl.bind(mainMod .. " + " .. i,          hl.dsp.focus({ workspace = i }))
    hl.bind(mainMod .. " + SHIFT + " .. i,  hl.dsp.window.move({ workspace = i }))
end

hl.bind("ALT + W", hl.dsp.exec_cmd("wtype ?"))

--------------------------------------
---- BINDS GERADOS PELO TIDE-ISLAND ----
--------------------------------------
-- ATENÇÃO: o arquivo abaixo é gerado pelo tide-island e, no seu .conf original,
-- estava sendo carregado com `source = ...`, ou seja, ele ainda usa a sintaxe
-- hyprlang antiga (não lua). O `source` do hyprlang não existe mais no formato
-- lua — o equivalente é `require(...)`, mas isso só funciona se o arquivo em
-- questão também for um módulo .lua válido.
--
-- Verifique se o tide-island já foi atualizado para gerar um
-- hyprland-shortcuts.lua. Se sim, troque a linha abaixo por:
--   require("tide-island/hyprland-shortcuts")
-- (sem a extensão .lua, com o caminho relativo à hyprland.lua)
--
-- Se ainda gerar .conf (hyprlang), a forma mais simples de manter funcionando
-- é rodar esse arquivo antigo via hyprctl na inicialização, algo como:
--   hl.on("hyprland.start", function()
--       hl.exec_cmd("hyprctl reload -- ~/.config/tide-island/hyprland-shortcuts.conf")
--   end)
-- Mas o ideal é falar com o mantenedor do tide-island sobre suporte a lua.

require("tide-island/hyprland-shortcuts")