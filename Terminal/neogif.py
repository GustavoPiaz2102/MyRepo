import os
import sys
import time
import shutil
import termios
import select
import subprocess
import getpass
import socket
import argparse
from PIL import Image

# --- DEFAULT SETTINGS ---
DEFAULT_SCALE = 0.172
CHARS = "@#S%?*+; ,. "

USER = getpass.getuser()
HOSTNAME = socket.gethostname()

def read_file(path, fallback=''):
	try:
		with open(path) as f:
			return f.read().strip()
	except Exception:
		return fallback

def run_cmd(cmd, fallback=''):
	try:
		return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, text=True).strip()
	except Exception:
		return fallback

def get_os():
	for line in read_file('/etc/os-release').splitlines():
		if line.startswith('PRETTY_NAME='):
			name = line.split('=', 1)[1].strip('"')
			arch = run_cmd('uname -m', 'x86_64')
			return f"{name} {arch}"
	return 'Linux'

def get_host():
	name = read_file('/sys/class/dmi/id/product_name', 'Unknown')
	version = read_file('/sys/class/dmi/id/product_version', '').strip()
	if version and version.lower() not in ('', 'none', 'not applicable'):
		return f"{name} {version}"
	return name

def get_kernel():
	return run_cmd('uname -r', 'unknown')

def get_uptime():
	try:
		secs = float(read_file('/proc/uptime').split()[0])
		h = int(secs // 3600)
		m = int((secs % 3600) // 60)
		if h > 0:
			return f"{h} hour{'s' if h != 1 else ''}, {m} min{'s' if m != 1 else ''}"
		return f"{m} min{'s' if m != 1 else ''}"
	except Exception:
		return 'unknown'

def get_packages():
	dpkg = run_cmd('dpkg-query -f ".\n" -W 2>/dev/null | wc -l', '?')
	flatpak = run_cmd('flatpak list 2>/dev/null | wc -l', '?')
	parts = []
	if dpkg != '?':
		parts.append(f"{dpkg} (dpkg)")
	if flatpak != '?' and flatpak != '0':
		parts.append(f"{flatpak} (flatpak)")
	return ', '.join(parts) if parts else 'unknown'

def get_shell():
	shell_path = os.environ.get('SHELL', run_cmd('which fish', '/bin/fish'))
	name = os.path.basename(shell_path)
	version = run_cmd(f"{shell_path} --version 2>&1 | head -1 | grep -oP '[\\d.]+'", '')
	if version:
		return f"{name} {version}"
	return name

def get_resolution():
	res = run_cmd("xrandr 2>/dev/null | grep ' connected' | grep -oP '\\d+x\\d+' | head -1")
	if res:
		return res
	res = run_cmd("xdpyinfo 2>/dev/null | grep dimensions | grep -oP '\\d+x\\d+' | head -1")
	return res or 'unknown'

def get_de():
	de = os.environ.get('XDG_CURRENT_DESKTOP', '')
	if not de:
		de = os.environ.get('DESKTOP_SESSION', '')
	return de if de else 'unknown'

def get_theme():
	theme = run_cmd("gsettings get org.gnome.desktop.interface gtk-theme 2>/dev/null")
	return theme.strip("'") if theme else 'unknown'

def get_icons():
	icons = run_cmd("gsettings get org.gnome.desktop.interface icon-theme 2>/dev/null")
	return icons.strip("'") if icons else 'unknown'

def get_terminal():
	terminals = {'cosmic-term', 'gnome-terminal', 'konsole', 'alacritty',
				 'kitty', 'wezterm', 'xterm', 'tilix', 'terminator'}
	try:
		pid = os.getpid()
		for _ in range(6):
			ppid = int(read_file(f'/proc/{pid}/status').split('PPid:')[1].split()[0])
			name = read_file(f'/proc/{ppid}/comm', '')
			if name.lower() in terminals:
				return name
			pid = ppid
	except Exception:
		pass
	return os.environ.get('TERM_PROGRAM', os.environ.get('TERM', 'unknown'))

def get_cpu():
	cores = 0
	model = 'unknown'
	for line in read_file('/proc/cpuinfo').splitlines():
		if 'model name' in line and model == 'unknown':
			model = line.split(':', 1)[1].strip()
		if line.startswith('processor'):
			cores += 1
	freq_str = run_cmd(
		"cat /sys/devices/system/cpu/cpu*/cpufreq/cpuinfo_max_freq 2>/dev/null | sort -n | tail -1"
	)
	if freq_str:
		try:
			freq_ghz = int(freq_str) / 1_000_000
			return f"{model} ({cores}) @ {freq_ghz:.3f}GHz"
		except Exception:
			pass
	return f"{model} ({cores})" if cores else model

def get_gpus():
	lines = run_cmd("lspci 2>/dev/null | grep -iE 'vga|3d|display'").splitlines()
	gpus = []
	for line in lines:
		parts = line.split(': ', 1)
		if len(parts) > 1:
			name = parts[1].strip().split('[')[0].strip()
			gpus.append(name)
	return gpus if gpus else ['unknown']

def get_memory():
	mem = {}
	for line in read_file('/proc/meminfo').splitlines():
		parts = line.split()
		if len(parts) >= 2:
			mem[parts[0].rstrip(':')] = int(parts[1])
	try:
		total_mib = mem['MemTotal'] // 1024
		available_mib = mem['MemAvailable'] // 1024
		used_mib = total_mib - available_mib
		return f"{used_mib}MiB / {total_mib}MiB"
	except Exception:
		return 'unknown'

def get_disk(path='/'):
	try:
		total, used, _ = shutil.disk_usage(path)
		to_gib = lambda b: b / (1024 ** 3)
		return f"{to_gib(used):.0f}GiB / {to_gib(total):.0f}GiB"
	except Exception:
		return 'unknown'

def get_battery():
	base = '/sys/class/power_supply'
	try:
		supplies = os.listdir(base)
	except Exception:
		return []
	results = []
	for name in sorted(supplies):
		path = f"{base}/{name}"
		ptype = read_file(f"{path}/type", '').upper()
		if ptype != 'BATTERY':
			continue
		capacity = read_file(f"{path}/capacity", '?')
		status = read_file(f"{path}/status", '?')
		results.append(f"{capacity}% [{status}]")
	return results

def get_system_info():
	C = "\033[1;36m"
	W = "\033[0m"
	gpus = get_gpus()
	batteries = get_battery()
	header = f"{USER}@{HOSTNAME}"
	separator = "-" * len(header)

	lines = [
		f"{C}{header}{W}",
		f"{C}{separator}{W}",
		f"{C}OS:{W} {get_os()}",
		f"{C}Host:{W} {get_host()}",
		f"{C}Kernel:{W} {get_kernel()}",
		f"{C}Uptime:{W} {get_uptime()}",
		f"{C}Packages:{W} {get_packages()}",
		f"{C}Shell:{W} {get_shell()}",
		f"{C}Resolution:{W} {get_resolution()}",
		f"{C}DE:{W} {get_de()}",
		f"{C}Theme:{W} {get_theme()}",
		f"{C}Icons:{W} {get_icons()}",
		f"{C}Terminal:{W} {get_terminal()}",
		f"{C}CPU:{W} {get_cpu()}",
	]
	for gpu in gpus:
		lines.append(f"{C}GPU:{W} {gpu}")
	lines.append(f"{C}Memory:{W} {get_memory()}")
	lines.append(f"{C}Disk (/):{W} {get_disk('/')}")
	for i, bat in enumerate(batteries):
		lines.append(f"{C}Battery{i}:{W} {bat}")
	lines.append("")
	lines.append("\033[1;30m   ● \033[1;31m● \033[1;32m● \033[1;33m● \033[1;34m● \033[1;35m● \033[1;36m● \033[1;37m●\033[0m")
	return lines

def get_ansi_color(r, g, b):
	return f"\033[38;2;{r};{g};{b}m"

def compute_scale(gif_path, target_cols_fraction=0.40):
	"""
	Calcula a scale dinamicamente para que o GIF ocupe
	`target_cols_fraction` da largura do terminal.
	O fator 0.5 compensa que caracteres são mais altos que largos.
	"""
	term_cols, _ = shutil.get_terminal_size(fallback=(120, 40))
	try:
		img = Image.open(gif_path)
		orig_w, _ = img.size
	except Exception:
		return DEFAULT_SCALE
	target_cols = int(term_cols * target_cols_fraction)
	return target_cols / orig_w

def convert_gif_to_frames(path, scale):
	try:
		img = Image.open(path)
	except Exception as e:
		print(f"Error opening file: {e}")
		sys.exit(1)

	frames = []
	orig_w, orig_h = img.size
	new_w = int(orig_w * scale)
	new_h = int(orig_h * scale * 0.5)
	try:
		while True:
			frame_rgb = img.convert('RGB')
			frame_resized = frame_rgb.resize((new_w, new_h), Image.Resampling.LANCZOS)
			ascii_lines = []
			for y in range(new_h):
				line = ""
				for x in range(new_w):
					r, g, b = frame_resized.getpixel((x, y))
					brightness = int(sum([r, g, b]) / 3)
					char = CHARS[int((brightness / 255) * (len(CHARS) - 1))]
					line += f"{get_ansi_color(r, g, b)}{char}"
				ascii_lines.append(line + "\033[0m")
			frames.append((ascii_lines, new_w))
			img.seek(img.tell() + 1)
	except EOFError:
		pass
	return frames

def key_pressed():
	return select.select([sys.stdin], [], [], 0)[0] != []

def run_neogif(gif_path, scale, argumentsAdd = None):
	sys_info = get_system_info()
	frames_data = convert_gif_to_frames(gif_path, scale)
	sys.stdout.write("\033[?25l")
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	new_settings = termios.tcgetattr(fd)
	new_settings[3] &= ~(termios.ICANON | termios.ECHO)
	new_settings[6][termios.VMIN] = 0
	new_settings[6][termios.VTIME] = 0
	try:
		termios.tcsetattr(fd, termios.TCSAFLUSH, new_settings)
		while True:
			for frame_lines, current_w in frames_data:
				if scale != compute_scale(gif_path, argumentsAdd.fraction):
					scale = compute_scale(gif_path, argumentsAdd.fraction)
					frames_data = convert_gif_to_frames(gif_path, scale)
					sys_info = get_system_info()
					os.system('clear')
					break
				if key_pressed():
					return
				output = "\033[H"
				max_lines = max(len(frame_lines), len(sys_info))
				for i in range(max_lines):
					ascii_part = frame_lines[i] if i < len(frame_lines) else " " * current_w
					info_part = sys_info[i] if i < len(sys_info) else ""
					output += f" {ascii_part}   {info_part}\033[K\n"
				sys.stdout.write(output)
				sys.stdout.write("\n\033[1mPress any key to skip\033[0m")
				sys.stdout.flush()
				time.sleep(0.07)
	except KeyboardInterrupt:
		pass
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, old_settings)
		sys.stdout.write("\033[?25h\n")
		print("Exiting...")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Neogif: Displays system information with an ASCII GIF.")
	parser.add_argument("path", help="Path to the .gif file")
	parser.add_argument("--scale", type=float, default=None,
		help="Image scale manual (padrão: automático baseado no terminal)")
	parser.add_argument("--fraction", type=float, default=0.40,
		help="Fração da largura do terminal que o GIF deve ocupar (padrão: 0.40)")

	args = parser.parse_args()

	scale = args.scale if args.scale is not None else compute_scale(args.path, args.fraction)

	os.system('clear')
	run_neogif(args.path, scale,args)
	os.system('clear')
