#!/bin/bash
# Applies a new wallpaper via awww, then re-themes kitty, GTK, Neovim and
# Hyprland borders from the wallpaper's color palette (extracted with
# iris.py, bundled in this repo). Wired up as tide-island's custom
# wallpaper command:
#   $1 = source wallpaper path, $2 = target wallpaper path (persisted copy)

set -u

SOURCE="$1"
TARGET="${2:-}"

IRIS="$HOME/git/MyRepo/MyHypr/confs/quickshell/iris/iris.py"
KITTY_COLORS="$HOME/.cache/qs/kitty-colors.conf"
GTK4_CSS="$HOME/.config/gtk-4.0/gtk.css"
GTK3_CSS="$HOME/.config/gtk-3.0/gtk.css"
NVIM_COLORS="$HOME/.config/nvim/lua/colors.lua"

[ -z "$SOURCE" ] && exit 2

# 1. Actually set the wallpaper (mirrors tide-island's built-in applyScript).
APPLIED="$SOURCE"
if [ -n "$TARGET" ]; then
    TARGET_EXPANDED="${TARGET/#\~/$HOME}"
    mkdir -p "$(dirname "$TARGET_EXPANDED")"
    if [ "$(readlink -f "$SOURCE")" != "$(readlink -f "$TARGET_EXPANDED" 2>/dev/null)" ]; then
        # Never copy through a symlink: it would overwrite whatever the
        # link points at instead of replacing the link itself.
        [ -L "$TARGET_EXPANDED" ] && rm -f "$TARGET_EXPANDED"
        cp -f "$SOURCE" "$TARGET_EXPANDED"
    fi
    APPLIED="$TARGET_EXPANDED"
fi

awww img "$APPLIED" \
    --transition-type random \
    --transition-duration 1 \
    --transition-fps 60

# 2. Extract a color palette from the wallpaper (Alphonso's iris.py).
THEME_JSON=$(python3 "$IRIS" --wallpaper "$APPLIED" --dark -1 --glass 0 2>/dev/null)
[ -z "$THEME_JSON" ] && exit 0

read -r BG FG ACCENT SURFACE DIM RED GREEN YELLOW DARK <<EOF
$(python3 -c "
import json, sys
p = json.loads(sys.argv[1])
print(p['bg'], p['fg'], p['accent'], p['surface'], p['dim'], p['red'], p['green'], p['yellow'], str(p.get('dark', False)).lower())
" "$THEME_JSON")
EOF

# 3. kitty (kitty.conf already `include`s this file).
mkdir -p "$(dirname "$KITTY_COLORS")"
cat > "$KITTY_COLORS" << KITTYEOF
foreground $FG
background $BG
cursor $ACCENT
cursor_text_color $BG
selection_foreground $BG
selection_background $ACCENT
url_color $ACCENT
active_tab_foreground $BG
active_tab_background $ACCENT
inactive_tab_foreground $DIM
inactive_tab_background $SURFACE
active_border_color $ACCENT
inactive_border_color $SURFACE
color0 $SURFACE
color8 $DIM
color1 $RED
color9 $RED
color2 $GREEN
color10 $GREEN
color3 $YELLOW
color11 $YELLOW
color4 $ACCENT
color12 $ACCENT
color5 $ACCENT
color13 $ACCENT
color6 $ACCENT
color14 $ACCENT
color7 $FG
color15 $FG
KITTYEOF

for sock in /tmp/kitty-socket-*; do
    [ -S "$sock" ] && kitty @ --to "unix:$sock" set-colors -a "$KITTY_COLORS" >/dev/null 2>&1
done

# 4. GTK 3/4 apps.
mkdir -p "$(dirname "$GTK4_CSS")" "$(dirname "$GTK3_CSS")"
GTK_CSS=$(cat << GTKEOF
@define-color accent_color $ACCENT;
@define-color accent_bg_color $ACCENT;
@define-color accent_fg_color $BG;
@define-color destructive_color $RED;
@define-color destructive_bg_color $RED;
@define-color destructive_fg_color $BG;
@define-color success_color $GREEN;
@define-color success_bg_color $GREEN;
@define-color success_fg_color $BG;
@define-color warning_color $YELLOW;
@define-color warning_bg_color $YELLOW;
@define-color warning_fg_color $BG;
@define-color window_bg_color $BG;
@define-color window_fg_color $FG;
@define-color view_bg_color $SURFACE;
@define-color view_fg_color $FG;
@define-color headerbar_bg_color $SURFACE;
@define-color headerbar_fg_color $FG;
@define-color headerbar_border_color $DIM;
@define-color popover_bg_color $SURFACE;
@define-color popover_fg_color $FG;
@define-color dialog_bg_color $BG;
@define-color dialog_fg_color $FG;
@define-color sidebar_bg_color $SURFACE;
@define-color sidebar_fg_color $FG;
@define-color card_bg_color $SURFACE;
@define-color card_fg_color $FG;
GTKEOF
)
printf '%s\n' "$GTK_CSS" > "$GTK4_CSS"
printf '%s\n' "$GTK_CSS" > "$GTK3_CSS"

if [ "$DARK" = "true" ]; then
    SCHEME="prefer-dark"
else
    SCHEME="prefer-light"
fi
gsettings set org.gnome.desktop.interface color-scheme "$SCHEME" 2>/dev/null || true

# 5. Neovim (watches this file and hot-reloads).
mkdir -p "$(dirname "$NVIM_COLORS")"
python3 -c "
import json
p = json.loads('''$THEME_JSON''')
def g(k, fb): return p.get(k, fb)
lines = [
    'return {',
    '    bg              = \"%s\",' % p['bg'],
    '    surface         = \"%s\",' % p['surface'],
    '    fg              = \"%s\",' % p['fg'],
    '    dim             = \"%s\",' % p['dim'],
    '    accent          = \"%s\",' % p['accent'],
    '    red             = \"%s\",' % p['red'],
    '    green           = \"%s\",' % p['green'],
    '    yellow          = \"%s\",' % p['yellow'],
    '    syntax_keyword  = \"%s\",' % g('syntax_keyword', p['accent']),
    '    syntax_string   = \"%s\",' % g('syntax_string', p['yellow']),
    '    syntax_func     = \"%s\",' % g('syntax_func', p['green']),
    '    syntax_type     = \"%s\",' % g('syntax_type', p['accent']),
    '    syntax_const    = \"%s\",' % g('syntax_const', p['red']),
    '    syntax_comment  = \"%s\",' % g('syntax_comment', p['dim']),
    '    syntax_param    = \"%s\",' % g('syntax_param', p['fg']),
    '    syntax_operator = \"%s\",' % g('syntax_operator', p['accent']),
    '    dark            = %s,' % ('true' if p.get('dark') else 'false'),
    '}',
    '',
]
open('$NVIM_COLORS', 'w').write('\n'.join(lines))
"

# 6. Hyprland window borders.
hyprctl keyword general:col.active_border "rgba(${ACCENT#\#}ff)" >/dev/null 2>&1
hyprctl keyword general:col.inactive_border "rgba(${SURFACE#\#}ff)" >/dev/null 2>&1