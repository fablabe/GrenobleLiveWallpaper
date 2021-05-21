#!/usr/bin/env python3

import requests
from datetime import datetime
import json
import wget
import platform # pour détecter l'OS
import os
import sys # pour stderr
import time

SLEEP_TIME = 60


sys.stdout = open("logfile.out","w")
sys.stderr = sys.stdout

def print_datetime():
	t = time.localtime()
	print(t.tm_year,'/',t.tm_mon,'/',t.tm_mday,' ', t.tm_hour,':', t.tm_min,':', t.tm_sec, '\t', sep="", end="")

current_img_name = None

_platform = platform.system()

if _platform == 'Windows':
	import ctypes # pour windows
	
	SPI_SETDESKWALLPAPER = 20
	
	# MessageBox = ctypes.windll.user32.MessageBoxW
	# MessageBox(None, 'Grenoble Live Wallpaper started. (OK to continue)', 'pythonw.exe', 0)
	print_datetime()
	print("Grenoble Live Wallpaper started")
	
	def is_64_windows():
		"""Find out how many bits is OS. """
		return 'PROGRAMFILES(X86)' in os.environ

	def get_sys_parameters_info():
		"""Based on if this is 32bit or 64bit returns correct version of SystemParametersInfo function. """
		return ctypes.windll.user32.SystemParametersInfoW if is_64_windows() \
			else ctypes.windll.user32.SystemParametersInfoA

	def change_wallpaper(wallpaper_path):
		sys_parameters_info = get_sys_parameters_info()
		r = sys_parameters_info(SPI_SETDESKWALLPAPER, 0, wallpaper_path, 3)
		if not r:           # When the SPI_SETDESKWALLPAPER flag is used, SystemParametersInfo returns TRUE unless there is an error (like when the specified file doesn't exist).
			print_datetime()
			print(ctypes.WinError())
			
elif _platform == 'Linux':
	def change_wallpaper(wallpaper_path):
		os.system("feh --bg-fill --no-xinerama bg.jpg")
else:
	print_datetime()
	print("Platform not supported.")
	exit()

api_key="GdP46-rpcxB-2E6ZU-cGCg6"

while True:
	now = datetime.now().strftime("%Y-%m-%d 00:00:00")
	now10 = datetime.now().strftime("%Y-%m-%d 23:59:59")

	params={ "types":"image","start":now,"end":now10,"_n":"1440","api_key":api_key }
	url = "https://api.skaping.com/media/search"

	r = requests.get(url, params=params)

	rJSON = json.loads(r.text)
	rJSON_Medias_Length = len(rJSON["medias"])

	print(rJSON["medias"][rJSON_Medias_Length-1]["src"])
	
	img_name = rJSON["medias"][rJSON_Medias_Length-1]["src"].split('/')[-1]
	if img_name != current_img_name:
		current_img_name = img_name
		try :
			fname = wget.download(rJSON["medias"][rJSON_Medias_Length-1]["src"])
		except :
			print_datetime()
			print("Download failed. URL =", rJSON["medias"][rJSON_Medias_Length-1]["src"])
			time.sleep(SLEEP_TIME)
			continue
		if os.path.exists('bg.jpg'):
			os.remove('bg.jpg')
		os.rename(fname, "bg.jpg")
		
		change_wallpaper(os.path.abspath("bg.jpg"))
	
	time.sleep(SLEEP_TIME)
	
		
	