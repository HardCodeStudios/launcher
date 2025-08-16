import requests
import os
import shutil
import zipfile
import subprocess
import sys
import time

# CONFIGURAZIONE GITHUB
VERSION_URL = "https://raw.githubusercontent.com/NAME_GITHUB/redm-launcher/main/upload/version.txt"
LAUNCHER_URL = "https://raw.githubusercontent.com/NAME_GITHUB/redm-launcher/main/upload/launcher_new.exe"
LOCAL_VERSION_FILE = "version.txt"
LAUNCHER_NAME = "launcher.exe"
TEMP_LAUNCHER_NAME = "launcher_new.exe"

def get_remote_version():
    try:
        response = requests.get(VERSION_URL, timeout=5)
        return response.text.strip()
    except Exception as e:
        print(f"[Updater] Error retrieving version: {e}")
        return None

def get_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return None
    with open(LOCAL_VERSION_FILE, "r") as f:
        return f.read().strip()

def update_launcher():
    print("[Updater] Download new version...")
    try:
        r = requests.get(LAUNCHER_URL, stream=True)
        with open(TEMP_LAUNCHER_NAME, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        print("[Updater] Download completed.")
    except Exception as e:
        print(f"[Updater] Error downloading launcher: {e}")
        return False

    print("[Updater] I close any launcher that is running...")
    try:
        subprocess.call(["taskkill", "/f", "/im", LAUNCHER_NAME], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

    print("[Updater] I replace the launcher...")
    try:
        if os.path.exists(LAUNCHER_NAME):
            os.remove(LAUNCHER_NAME)
        os.rename(TEMP_LAUNCHER_NAME, LAUNCHER_NAME)
    except Exception as e:
        print(f"[Updater] Error while replacing: {e}")
        return False

    return True

def launch_launcher():
    print("[Updater] I launch the updated launcher.")
    subprocess.Popen([LAUNCHER_NAME])
    sys.exit()

def main():
    print("[Updater] Starting check for updates...")
    remote_version = get_remote_version()
    local_version = get_local_version()

    if remote_version and remote_version != local_version:
        print(f"[Updater] New version available: {remote_version}")
        if update_launcher():
            with open(LOCAL_VERSION_FILE, "w") as f:
                f.write(remote_version)
            launch_launcher()
        else:
            print("[Updater] Update failed.")
    else:
        print("[Updater] No updates available.")
        launch_launcher()

if __name__ == "__main__":
    main()