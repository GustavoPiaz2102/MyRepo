#!/usr/bin/env python3

import argparse
import json
import os
import random
import sys
import time
import tty
import termios

PROGRAM = os.path.realpath(__file__)
PROGRAM_DIR = os.path.dirname(PROGRAM)
COLORSCRIPTS_DIR = f"{PROGRAM_DIR}/colorscripts"
STATS_FILE = os.path.expanduser("~/.pokemon-player.json")

REGULAR_SUBDIR = "regular"
SHINY_SUBDIR = "shiny"
LARGE_SUBDIR = "large"
SMALL_SUBDIR = "small"

SHINY_RATE = 1 / 128

def load_stats():
	default = {"Captured": {}, "AtualLevel": 1, "ExpToNextLevel": 50, "CurrentExp": 0, "LastDetectedTime": 0}
	if not os.path.exists(STATS_FILE):
		return default
	try:
		with open(STATS_FILE, 'r') as f:
			return json.load(f)
	except:
		return default

def save_stats(stats):
	with open(STATS_FILE, 'w') as f:
		json.dump(stats, f, indent=4)

def get_pokemon_name(p_id):
	with open(f"{PROGRAM_DIR}/pokemon.json", "r") as file:
		pokemon_list = json.load(file)
		return pokemon_list[p_id - 1]["name"]

def get_char():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
		if ch == '\x1b':
			ch += sys.stdin.read(2)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def list_captured():
	stats = load_stats()
	captured = stats.get("Captured", {})
	
	if not captured:
		print("\033[1;31mVocê ainda não capturou nenhum Pokémon!\033[0m")
		return

	tabs = ["regular", "shiny"]
	tab_idx = 0
	current_index = 0

	while True:
		current_tab = tabs[tab_idx]
		filtered_ids = [p_id for p_id, counts in captured.items() if counts.get(current_tab, 0) > 0]
		filtered_ids.sort(key=lambda x: int(x))

		if current_index >= len(filtered_ids) and len(filtered_ids) > 0:
			current_index = len(filtered_ids) - 1
		elif len(filtered_ids) == 0:
			current_index = 0

		print("\033[H\033[J", end="")
		
		print(f"\033[1;35m--- POKÉDEX (Nível {stats['AtualLevel']}) ---\033[0m")
		print("\033[1;37m[←/→] Mudar Aba  |  [↑/↓] Selecionar  |  [Q] Sair\033[0m")
		
		reg_color = "\033[1;30;46m" if current_tab == "regular" else "\033[1;36m"
		shi_color = "\033[1;30;43m" if current_tab == "shiny" else "\033[1;33m"
		
		print(f"{reg_color}  NORMAL  \033[0m {shi_color}  SHINY ★  \033[0m\n")

		image_lines = []
		if filtered_ids:
			sel_id = filtered_ids[current_index]
			sel_name = get_pokemon_name(int(sel_id))
			sel_count = captured[sel_id][current_tab]
			
			img_path = f"{COLORSCRIPTS_DIR}/{SMALL_SUBDIR}/{current_tab}/{sel_name}"
			if os.path.exists(img_path):
				with open(img_path, "r") as f:
					image_lines = [line.rstrip() for line in f.readlines()]

			menu_width = 25
			max_display = 12
			start_view = max(0, current_index - 5)
			
			for i in range(max(max_display, len(image_lines))):
				line_idx = start_view + i
				if i < max_display and line_idx < len(filtered_ids):
					p_id = filtered_ids[line_idx]
					name = get_pokemon_name(int(p_id))
					is_sel = (line_idx == current_index)
					
					prefix = "» " if is_sel else "  "
					text = f"{prefix}{name.capitalize()}"
					padding = " " * (menu_width - len(text))
					
					if is_sel:
						color = "\033[1;97;46m" if current_tab == "regular" else "\033[1;97;43m"
					else:
						color = "\033[0m"
					
					print(f"{color}{text}{padding}\033[0m", end="  ")
				else:
					print(" " * (menu_width + 2), end="")

				if i < len(image_lines):
					print(image_lines[i], end="")
				print()

			print(f"\n\033[1mCapturados:\033[0m {sel_count}")
		else:
			print(f"\n\n\033[1;90m   Nenhum Pokémon nesta categoria...\033[0m")

		key = get_char()
		if key in ('\x1b[A', 'w', 'W'):
			if filtered_ids: current_index = (current_index - 1) % len(filtered_ids)
		elif key in ('\x1b[B', 's', 'S'):
			if filtered_ids: current_index = (current_index + 1) % len(filtered_ids)
		elif key in ('\x1b[D', 'a', 'A'):
			tab_idx = (tab_idx - 1) % 2
			current_index = 0
		elif key in ('\x1b[C', 'd', 'D'):
			tab_idx = (tab_idx + 1) % 2
			current_index = 0
		elif key in ('q', 'Q', '\x1b'):
			print("\033[H\033[J", end="")
			break

def process_capture(pokemon_name, p_id, is_shiny, stats):
	p_id_str = str(p_id)
	print(f"\n\033[1;34m[?]\033[0m Um {pokemon_name.capitalize()}{' SHINY' if is_shiny else ''} apareceu!")
	choice = input("Pressione [ENTER] para capturar ou qualquer tecla para fugir: ")
	if choice == "":
		stats["LastDetectedTime"] = time.time()
		print("Lançando Pokébola", end="", flush=True)
		for _ in range(3):
			time.sleep(0.4)
			print(".", end="", flush=True)
		print("\n")
		if random.random() <= 0.5:
			if p_id_str not in stats["Captured"]:
				stats["Captured"][p_id_str] = {"regular": 0, "shiny": 0}
			key = "shiny" if is_shiny else "regular"
			stats["Captured"][p_id_str][key] += 1
			stats["CurrentExp"] += 100
			print(f"\033[1;32m[*]\033[0m Gotcha! {pokemon_name.capitalize()} capturado!")
			while stats["CurrentExp"] >= stats["ExpToNextLevel"]:
				stats["CurrentExp"] -= stats["ExpToNextLevel"]
				stats["AtualLevel"] += 1
				stats["ExpToNextLevel"] = round(stats["ExpToNextLevel"] * 1.1, 2)
				print(f"\033[1;35m[\u231b]\033[0m LEVEL UP! Nível {stats['AtualLevel']}!")
		else:
			print(f"\033[1;31m[X]\033[0m O {pokemon_name.capitalize()} quebrou a Pokébola e fugiu!")
		save_stats(stats)
	else:
		print(f"\033[1;90m[-] Você fugiu do combate...\033[0m")

def show_encounter(is_tiny):
	stats = load_stats()
	current_time = time.time()
	last_time = stats.get("LastDetectedTime", 0)
	if current_time - last_time < 60:
		wait_time = int(60 - (current_time - last_time))
		print(f"\033[1;31m[!] Os Pokémons estão assustados. Espere {wait_time}s para procurar novamente.\033[0m")
		return
	p_id = random.randint(1, 898)
	is_shiny = random.random() <= SHINY_RATE
	name = get_pokemon_name(p_id)
	size_dir = SMALL_SUBDIR if is_tiny else LARGE_SUBDIR
	color_dir = SHINY_SUBDIR if is_shiny else REGULAR_SUBDIR
	filepath = f"{COLORSCRIPTS_DIR}/{size_dir}/{color_dir}/{name}"
	if os.path.exists(filepath):
		with open(filepath, "r") as f:
			print(f.read())
	title = f"{name} (SHINY)" if is_shiny else name
	print(f"\033[1m{title.upper()}\033[0m")
	process_capture(name, p_id, is_shiny, stats)

def main():
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument("-t", "--tiny", action="store_true")
	parser.add_argument("-l", "--list", action="store_true")
	args = parser.parse_args()
	if args.list:
		list_captured()
	else:
		show_encounter(args.tiny)

if __name__ == "__main__":
	main()