# -*- coding: utf-8 -*-
import subprocess
import os, signal
import platform
_platform = platform.system()
import time, uptime

def start():
    p = subprocess.Popen(["python", "main.pyw"])
    print("Grenoble Live Wallpaper started.")
    with open('.pid', 'w') as pidfile:
        pidfile.write(str(p.pid))

if __name__ == '__main__':

    if os.path.exists('.pid'):
        if time.time() - uptime.uptime() < os.path.getmtime('.pid') : # si le fichier a été modifié après le démarrage de l'OS
            with open('.pid', 'r') as pidfile:
                pid = int(pidfile.readline())
            c = input("Grenoble Live Wallpaper is already running (PID {}). Do you wish to kill it? ([y]/n) ".format(pid))
            if c in ['', 'y', 'Y']:
                if _platform == 'Windows':
                    subprocess.call(['taskkill', '/F', '/T', '/PID',  str(pid)])
                else:
                    os.kill(pid, signal.SIGTERM)
                os.remove('.pid')
        else :
            os.remove('.pid')
            start()
    else :
        start()


