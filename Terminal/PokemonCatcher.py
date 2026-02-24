#!/usr/bin/env python3

import argparse
import json
import os
import random
import sys
import time

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
	default = {"Captured": {}, "AtualLevel": 1, "ExpToNextLevel": 50, "CurrentExp": 0}
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

def list_captured():
	stats = load_stats()
	captured = stats.get("Captured", {})
	if not captured:
		print("\033[1;31mVocê ainda não capturou nenhum Pokémon!\033[0m")
		return
	print(f"\n\033[1;35m--- SUA COLEÇÃO (Nível {stats['AtualLevel']}) ---\033[0m")
	print(f"{'Pokémon':<20} | {'Normal':<8} | {'Shiny':<8}")
	print("-" * 42)
	for p_id_str, counts in sorted(captured.items(), key=lambda x: int(x[0])):
		name = get_pokemon_name(int(p_id_str))
		reg = counts.get("regular", 0)
		shi = counts.get("shiny", 0)
		name_display = f"\033[1;32m{name.capitalize()}\033[0m" if shi > 0 else name.capitalize()
		print(f"{name_display:<29} | {reg:<8} | {shi:<8}")
	total = sum(c.get("regular", 0) + c.get("shiny", 0) for c in captured.values())
	print("-" * 42)
	print(f"Total de capturas: {total}\n")

def process_capture(pokemon_name, p_id, is_shiny):
	stats = load_stats()
	p_id_str = str(p_id)
	print(f"\n\033[1;34m[?]\033[0m Um {pokemon_name.capitalize()}{' SHINY' if is_shiny else ''} apareceu!")
	choice = input("Pressione [ENTER] para capturar ou qualquer tecla para fugir: ")
	if choice == "":
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
			save_stats(stats)
		else:
			print(f"\033[1;31m[X]\033[0m O {pokemon_name.capitalize()} quebrou a Pokébola e fugiu!")
	else:
		print(f"\033[1;90m[-] Você fugiu do combate...\033[0m")

def show_encounter(is_tiny):
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
	process_capture(name, p_id, is_shiny)

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