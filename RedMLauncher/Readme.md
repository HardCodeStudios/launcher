# Launcher (with Auto-Updater)

This guide explains how to install prerequisites, run the **Launcher**, and configure the **auto-update system** via GitHub.

---

## 1. System Requirements

- **Operating System**: Windows 10/11 (recommended and tested).  
- **Python**: version **3.10+** (downloadable from [python.org](https://www.python.org/downloads/)).  
  ⚠️ During Python installation, make sure to check **“Add Python to PATH”**.  
- **Internet access** (for `requests` and web links).  
- **Working sound card** (for music playback via `pygame`).  
- (Optional) **TeamSpeak 3** if you want to launch it from the launcher.  

---

## 2. Install Python Libraries

Open a **Command Prompt** (cmd/terminal) in your project folder and run:

```bash
pip install customtkinter pillow pygame requests
```

### Libraries used:
- **customtkinter** → modern GUI framework  
- **pillow (PIL)** → image handling  
- **pygame** → audio playback  
- **requests** → HTTP requests (e.g., server player count)  

---

## 3. Project Folder Structure

Make sure your launcher folder contains the following files:

```
/launcher
 ├── launcher.py          # main script
 ├── background.png       # background image
 ├── logo_server.png      # server logo
 ├── music.mp3            # background music
 ├── info.ico             # info icon
 ├── on.png               # music ON icon
 ├── off.png              # music OFF icon
 ├── girocarte.png        # switch card icon
 ├── char1.png            # main card
 ├── char1_hover.png      # hover state
 ├── char2.png
 ├── char2_hover.png
 ├── char3.png
 ├── char3_hover.png
 ├── instagram.png        # social card
 ├── instagram_hover.png
 ├── tiktok.png
 ├── tiktok_hover.png
 ├── youtube.png
 ├── youtube_hover.png
```

⚠️ If any resource is missing, the launcher may crash.  
Keep the folder organized as above.  

---

## 4. Run the Launcher (Development Mode)

Open a terminal in the launcher folder and run:

```bash
python launcher.py
```

If everything is set up correctly, the **Launcher window** will appear.  

---

## 5. Main Features

✅ Connect to RedM server (`redm://connect/...`)  
✅ Discord, TeamSpeak, Social buttons (Instagram, TikTok, YouTube)  
✅ Automatic Player Count update  
✅ Background music with toggle On/Off  
✅ Animated cards with switch (main ↔ social)  
✅ Rotating hint messages  
✅ Button & icon animations (shine, pulse)  

---

## 6. Build Executable (.exe) with PyInstaller

To distribute the launcher without requiring Python:

### Install PyInstaller
```bash
pip install pyinstaller
```

### Build `launcher.exe`

Run inside the project folder:

```bash
pyinstaller --onefile --noconsole ^
  --add-data "background.png;." ^
  --add-data "logo_server.png;." ^
  --add-data "music.mp3;." ^
  --add-data "info.ico;." ^
  --add-data "on.png;." ^
  --add-data "off.png;." ^
  --add-data "girocarte.png;." ^
  --add-data "char1.png;." ^
  --add-data "char1_hover.png;." ^
  --add-data "char2.png;." ^
  --add-data "char2_hover.png;." ^
  --add-data "char3.png;." ^
  --add-data "char3_hover.png;." ^
  --add-data "instagram.png;." ^
  --add-data "instagram_hover.png;." ^
  --add-data "tiktok.png;." ^
  --add-data "tiktok_hover.png;." ^
  --add-data "youtube.png;." ^
  --add-data "youtube_hover.png;." ^
  -n launcher launcher.py
```

You will find the executable in:
```
/dist/launcher.exe
```

---

## 6.1 Build the `updater.exe`

```bash
pyinstaller --onefile --noconsole -n updater updater.py
```

You will find the executable in:
```
/dist/updater.exe
```

⚠️ Always distribute **updater.exe** and **launcher.exe** in the **same folder**.  

---

## 7. Recommended Startup Flow (with Auto-Update)

1. The user launches **`updater.exe`** (create a desktop shortcut).  
2. The updater will:  
   - Fetch remote version from GitHub (`version.txt`)  
   - Compare with local version (`version.txt` in the folder)  
   - If different: download `launcher_new.exe`, close `launcher.exe` if running, replace it, update `version.txt`  
   - Launch **launcher.exe**  

⚠️ Do **not** run the launcher directly → Always run the updater first.  

---

## 8. GitHub Repository Setup (Server Side)

Publish these files to your GitHub repository (public or private with raw URL access):

- `upload/version.txt` → version string (e.g., `1.0.0.2`)  
- `upload/launcher_new.exe` → compiled launcher binary  

The updater uses these URLs (edit with your GitHub account name):

- `https://raw.githubusercontent.com/NAME_GITHUB/redm-launcher/main/upload/version.txt`  
- `https://raw.githubusercontent.com/NAME_GITHUB/redm-launcher/main/upload/launcher_new.exe`  

### Each Release:
1. Compile new `launcher.exe`  
2. Rename and upload it as `launcher_new.exe`  
3. Update `version.txt` with the new version (e.g., `1.0.0.3`)  
4. Commit & push  

---

## 9. Updater Script (Ready to Use)

Save this file as `updater.py`:

```python
import requests
import os
import shutil
import subprocess
import sys

# GITHUB CONFIGURATION
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
        print(f"[Updater] Error while fetching remote version: {e}")
        return None

def get_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return None
    with open(LOCAL_VERSION_FILE, "r") as f:
        return f.read().strip()

def update_launcher():
    print("[Updater] Downloading new version...")
    try:
        r = requests.get(LAUNCHER_URL, stream=True)
        r.raise_for_status()
        with open(TEMP_LAUNCHER_NAME, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        print("[Updater] Download completed.")
    except Exception as e:
        print(f"[Updater] Error while downloading launcher: {e}")
        return False

    print("[Updater] Closing any running launcher instance...")
    try:
        subprocess.call(["taskkill", "/f", "/im", LAUNCHER_NAME],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

    print("[Updater] Replacing launcher...")
    try:
        if os.path.exists(LAUNCHER_NAME):
            os.remove(LAUNCHER_NAME)
        os.rename(TEMP_LAUNCHER_NAME, LAUNCHER_NAME)
    except Exception as e:
        print(f"[Updater] Error while replacing launcher: {e}")
        return False

    return True

def launch_launcher():
    print("[Updater] Starting the updated launcher.")
    subprocess.Popen([LAUNCHER_NAME])
    sys.exit()

def main():
    print("[Updater] Checking for updates...")
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
            launch_launcher()
    else:
        print("[Updater] No updates available.")
        launch_launcher()

if __name__ == "__main__":
    main()
```

⚠️ This script requires `requests`. Ensure it is installed and your firewall allows GitHub access.  

---

## 10. User Instructions

- Provide the user with a folder containing:  
  - `updater.exe`  
  - `launcher.exe`  
  - All resources (`.png`, `.mp3`, `.ico`)  
- Create a **desktop shortcut** pointing to `updater.exe`  
- The user should **always launch the updater**, which will then start the launcher.  

⚠️ Important: All resources must be included with `--add-data` during compilation.  

---

## ✅ Done!

Now you have a working **Launcher with Auto-Updater**.  
Users only need to open **Updater**, and everything else will be handled automatically.