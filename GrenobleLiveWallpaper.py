import subprocess
import os, signal
import platform
_platform = platform.system()
import time, uptime

if os.path.exists('.pid'):
	if time.time() - uptime.uptime() < os.path.getmtime('.pid') : # si le fichier a été modifié après le démarrage de l'OS
		c = input("Grenoble Live Wallpaper is already running. Do you wish to kill it? ([y]/n) ")
		if c in ['', 'y', 'Y']:
			with open('.pid', 'r') as pidfile:
				pid = int(pidfile.readline())
				print(pid)
				if _platform == 'Windows':
					subprocess.call(['taskkill', '/F', '/T', '/PID',  str(pid)])
				else:
					os.kill(pid, signal.SIGTERM)
			os.remove('.pid')
	else :
		os.remove('.pid')

else :
	p = subprocess.Popen(["python", "main.pyw"])
	print("Grenoble Live Wallpaper started.")
	with open('.pid', 'w') as pidfile:
		pidfile.write(str(p.pid))
