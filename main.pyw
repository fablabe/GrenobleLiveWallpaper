# -*- coding: utf-8 -*-

import requests
from datetime import datetime
import json
import wget
import platform # pour détecter l'OS
import os
import sys # pour stderr
import time

SLEEP_TIME = 60


sys.stdout = open("logfile.out","a")
sys.stderr = sys.stdout

def print_datetime():
	print(datetime.now().strftime("%Y-%m-%d %H:%M:%S -- "), end="")

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
	if len(rJSON["medias"])>0:
		print_datetime()
		print("Downloading", rJSON["medias"][-1]["src"])
		
		img_name = rJSON["medias"][-1]["src"].split('/')[-1]
		if img_name != current_img_name:
			current_img_name = img_name
			try :
				if os.path.exists('bg.jpg'):
					os.remove('bg.jpg')
				fname = wget.download(rJSON["medias"][-1]["src"], 'bg.jpg', bar=None)
			except :
				print_datetime()
				print("Download failed. URL =", rJSON["medias"][-1]["src"])
				time.sleep(SLEEP_TIME)
				continue
	#		if os.path.exists('bg.jpg'):
	#			os.remove('bg.jpg')
	#		os.rename(fname, "bg.jpg")
			
			change_wallpaper(os.path.abspath("bg.jpg"))
	else:
		print_datetime()
		print("Error fetching URL.")
	
	time.sleep(SLEEP_TIME)
	
		
	
