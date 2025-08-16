import customtkinter as ctk
import webbrowser
import os
import sys
from PIL import Image, ImageTk, ImageEnhance, ImageOps
import tkinter as tk
import pygame
import requests
import subprocess
import tkinter.messagebox as mbox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

SERVER_IP = "127.0.0.1"
SERVER_PORT = "30120"
VERSION = "Version 1.0.0.1"

def play_redm():
    webbrowser.open(f"redm://connect/{SERVER_IP}:{SERVER_PORT}")

def apri_discord():
    webbrowser.open("https://discord.gg/")

def open_ts():
    ts3_path = r"C:\Program Files\TeamSpeak 3 Client\ts3client_win64.exe"
    if not os.path.exists(ts3_path):
        mbox.showerror("Errore", "TeamSpeak not found in:\n" + ts3_path)
        return
    try:
        subprocess.Popen([ts3_path, "ts3server://ts3server.com?port=0000"], shell=True)
    except Exception as e:
        mbox.showerror("Errore", f"Unable to start TeamSpeak.\n{e}")

def apri_instagram():
    webbrowser.open("https://www.instagram.com/")

def apri_tiktok():
    webbrowser.open("https://www.tiktok.com/")

def apri_youtube():
    webbrowser.open("https://www.youtube.com/")

base_path = getattr(sys, '_MEIPASS', os.path.abspath(".")) if hasattr(sys, '_MEIPASS') else os.path.abspath(".")
logo_path = os.path.join(base_path, "logo_server.png")

app = ctk.CTk()
app.geometry("1000x600")
app.resizable(False, False)
app.title("Launcher - HardCode Studios")

logo_icon_img = ImageTk.PhotoImage(Image.open(logo_path))
app.iconphoto(True, logo_icon_img)

base_path = getattr(sys, '_MEIPASS', os.path.abspath(".")) if hasattr(sys, '_MEIPASS') else os.path.abspath(".")
bg_path = os.path.join(base_path, "background.png")
logo_path = os.path.join(base_path, "logo_server.png")
music_path = os.path.join(base_path, "music.mp3")
info_icon_path = os.path.join(base_path, "info.ico")
music_on_icon_path = os.path.join(base_path, "on.png")
music_off_icon_path = os.path.join(base_path, "off.png")
girocarte_path = os.path.join(base_path, "girocarte.png")

social_cards = [("instagram", 8), ("tiktok", 0), ("youtube", -7)]

bg_image = Image.open(bg_path).resize((1000, 600))
bg_image_flipped = ImageOps.mirror(bg_image)
bg_photo = ImageTk.PhotoImage(bg_image_flipped)

info_icon_orig = Image.open(info_icon_path)

info_icon = ImageTk.PhotoImage(info_icon_orig.resize((18, 18)))

canvas = tk.Canvas(app, width=1000, height=600, highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

canvas.create_text(25, 10, anchor="nw", text="HardCode Studios", fill="white", font=("Arial Black", 30, "bold"))
canvas.create_text(25, 55, anchor="nw", text="Turbocharge your roleplay server!", fill="gray", font=("Arial", 17, "italic"))

hint_messages = [
    "AUTO-UPDATER ATTIVO",
    "Benvenuto nel launcher! Preparati all'avventura.",
    "Ricordati di connetterti a Discord per assistenza.",
    "Il nostro server è online H24!",
    "Controlla spesso gli aggiornamenti nella sezione changelog.",
    "Hai bisogno di aiuto? Scrivi a un admin su Discord!"
]
current_hint_index = 0
hint_x_icon = 50
hint_y = 105

hint_icon_item = canvas.create_image(hint_x_icon, hint_y, image=info_icon, anchor="w")
hint_text_item = canvas.create_text(hint_x_icon + 25, hint_y, text=hint_messages[0], anchor="w", fill="white", font=("Arial", 12, "italic"))

def rotate_hint():
    global current_hint_index
    current_hint_index = (current_hint_index + 1) % len(hint_messages)
    new_text = hint_messages[current_hint_index]
    canvas.itemconfig(hint_text_item, text=new_text)
    app.after(5000, rotate_hint)

player_count_var = tk.StringVar()
player_count_var.set("Check server...")
player_count_label = tk.Label(app, textvariable=player_count_var, fg="white", bg="#1e1e1e", font=("Arial", 15, "bold"), padx=5)
player_count_label.place(x=80, y=130)

is_muted = False

def remove_black_background(img):
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] < 20 and item[1] < 20 and item[2] < 20:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    return img

music_on_img_raw = Image.open(music_on_icon_path).resize((30, 30), Image.BICUBIC)
music_off_img_raw = Image.open(music_off_icon_path).resize((30, 30), Image.BICUBIC)
music_on_clean = remove_black_background(music_on_img_raw)
music_off_clean = remove_black_background(music_off_img_raw)

music_on_ctk = ctk.CTkImage(light_image=music_on_clean)
music_off_ctk = ctk.CTkImage(light_image=music_off_clean)

def toggle_music():
    global is_muted
    is_muted = not is_muted
    if is_muted:
        pygame.mixer.music.set_volume(0.0)
        music_btn.configure(image=music_off_ctk)
    else:
        pygame.mixer.music.set_volume(0.5)
        music_btn.configure(image=music_on_ctk)

music_btn = ctk.CTkButton(app, image=music_on_ctk, width=30, height=30, fg_color="transparent", hover_color="#555555", text="", command=toggle_music)
music_btn.place(x=42, y=130)

def apply_bottom_fade(image, fade_height=100):
    fade = Image.new("L", (image.width, fade_height), color=0)
    for y in range(fade_height):
        alpha = int(255 * (y / fade_height))
        fade.paste(alpha, (0, y, image.width, y + 1))
    black = Image.new("RGBA", (image.width, fade_height), (0, 0, 0, 255))
    image.paste(black, (0, image.height - fade_height), mask=fade)
    return image

logo_image = Image.open(logo_path).convert("RGBA")
logo_size = 140
logo_image = logo_image.resize((logo_size, logo_size), Image.BICUBIC)
logo_photo = ImageTk.PhotoImage(logo_image)
canvas.create_image(930, 60, image=logo_photo, anchor="center")

def load_card_images(base_name, rotate_angle=0):
    normal_path = os.path.join(base_path, f"{base_name}.png")
    hover_path = os.path.join(base_path, f"{base_name}_hover.png")
    normal_img = Image.open(normal_path).convert("RGBA")
    hover_img = Image.open(hover_path).convert("RGBA")
    target_height = 400
    aspect_ratio = 946 / 1344
    target_width = int(target_height * aspect_ratio)
    normal_img = normal_img.resize((target_width, target_height), Image.BICUBIC)
    hover_img = hover_img.resize((target_width, target_height), Image.BICUBIC)

    zoom_img = hover_img.resize((int(target_width * 1.1), int(target_height * 1.1)), Image.BICUBIC)

    normal_img = apply_bottom_fade(normal_img, fade_height=80)
    hover_img = apply_bottom_fade(hover_img, fade_height=80)
    zoom_img = apply_bottom_fade(zoom_img, fade_height=80)

    normal_rotated = normal_img.rotate(rotate_angle, expand=True, resample=Image.BICUBIC)
    hover_rotated = hover_img.rotate(rotate_angle, expand=True, resample=Image.BICUBIC)
    zoom_rotated = zoom_img.rotate(rotate_angle, expand=True, resample=Image.BICUBIC)

    enhancer = ImageEnhance.Brightness(hover_rotated)
    hover_bright = enhancer.enhance(1.3)

    enhancer_zoom = ImageEnhance.Brightness(zoom_rotated)
    zoom_bright = enhancer_zoom.enhance(1.3)

    return ImageTk.PhotoImage(normal_rotated), ImageTk.PhotoImage(hover_bright), ImageTk.PhotoImage(zoom_bright)

main_cards_data = [("char1", 8), ("char2", 0), ("char3", -7)]
main_images = [load_card_images(name, angle) for name, angle in main_cards_data]
social_images = [load_card_images(name, angle) for name, angle in social_cards]

main_canvases = []
social_canvases = []
state_main = True

def create_cards(images, ys, actions):
    canvases = []
    x_positions = [195, 450, 705]
    for i, img in enumerate(images):
        c = canvas.create_image(x_positions[i], 900, image=img[0], anchor="s")
        canvases.append(c)
    animate_enter(canvases, ys)
    for i, c in enumerate(canvases):
        canvas.tag_bind(c, "<Enter>", lambda e, ci=c, zi=images[i][2]: canvas.itemconfig(ci, image=zi))
        canvas.tag_bind(c, "<Leave>", lambda e, ci=c, ni=images[i][0]: canvas.itemconfig(ci, image=ni))
        canvas.tag_bind(c, "<Button-1>", actions[i])
    return canvases

def animate_exit(canvases, callback):
    def move():
        finished = True
        for c in canvases:
            x, y = canvas.coords(c)
            if y < 900:
                canvas.move(c, 0, 20)
                finished = False
        if not finished:
            app.after(15, move)
        else:
            for c in canvases:
                canvas.delete(c)
            callback()
    move()

def animate_enter(canvases, final_ys):
    def move():
        finished = True
        for i, c in enumerate(canvases):
            x, y = canvas.coords(c)
            if y > final_ys[i]:
                canvas.move(c, 0, -20)
                finished = False
        if not finished:
            app.after(15, move)
    move()

def switch_cards():
    global state_main, main_canvases, social_canvases
    if state_main:
        animate_exit(main_canvases, switch_to_social)
    else:
        animate_exit(social_canvases, switch_to_main)

def switch_to_social():
    global social_canvases, state_main
    social_actions = [lambda e: apri_instagram(), lambda e: apri_tiktok(), lambda e: apri_youtube()]
    social_canvases = create_cards(social_images, [645, 603, 647], social_actions)
    state_main = False

def switch_to_main():
    global main_canvases, state_main
    main_actions = [lambda e: apri_discord(), lambda e: play_redm(), lambda e: open_ts()]
    main_canvases = create_cards(main_images, [645, 603, 647], main_actions)
    state_main = True

main_actions = [lambda e: apri_discord(), lambda e: play_redm(), lambda e: open_ts()]
main_canvases = create_cards(main_images, [645, 603, 647], main_actions)

# Girocarte
girocarte_img_raw = Image.open(girocarte_path).resize((45, 47), Image.BICUBIC)
girocarte_clean = remove_black_background(girocarte_img_raw)
girocarte_img = ImageTk.PhotoImage(girocarte_clean)
girocarte_canvas = canvas.create_image(925, 450, image=girocarte_img, anchor="center")
canvas.tag_bind(girocarte_canvas, "<Button-1>", lambda e: switch_cards())

def shine(brightness=1.0, increasing=True):
    enhancer = ImageEnhance.Brightness(girocarte_clean)
    bright_img = enhancer.enhance(brightness)
    tk_img = ImageTk.PhotoImage(bright_img)
    canvas.itemconfig(girocarte_canvas, image=tk_img)
    canvas.girocarte_img = tk_img
    next_brightness = brightness + 0.02 if increasing else brightness - 0.02
    if next_brightness >= 1.5:
        increasing = False
    elif next_brightness <= 1.0:
        increasing = True
    app.after(50, lambda: shine(next_brightness, increasing))

shine()

def pulse_hint(scale=1.0, growing=True):
    new_size = int(18 * scale), int(18 * scale)
    resized = info_icon_orig.resize(new_size, Image.BICUBIC)
    img = ImageTk.PhotoImage(resized)
    canvas.itemconfig(hint_icon_item, image=img)
    canvas.hint_img = img
    next_scale = scale + 0.01 if growing else scale - 0.01
    if next_scale >= 1.1:
        growing = False
    elif next_scale <= 1.0:
        growing = True
    app.after(60, lambda: pulse_hint(next_scale, growing))

pulse_hint()

canvas.create_text(990, 590, text="Produced by AxeelWZ", fill="white", font=("Arial", 9, "italic"), anchor="se")
canvas.create_text(900, 600, text=VERSION, fill="white", font=("Arial", 7, "italic"), anchor="sw")

pygame.mixer.init()
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

def aggiorna_player_count():
    try:
        response = requests.get(f"http://{SERVER_IP}:{SERVER_PORT}/players.json", timeout=2)
        players = response.json()
        current = len(players)
        max_players = 128
        testo = f"{current}/{max_players} online ✅"
        color_to_use = "#00FF00"
    except:
        testo = "Server Offline ❌"
        color_to_use = "#FF3333"
    player_count_var.set(testo)
    player_count_label.config(fg=color_to_use)
    app.after(10000, aggiorna_player_count)

aggiorna_player_count()
rotate_hint()
app.mainloop()