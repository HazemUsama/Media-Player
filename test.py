import os
from tkinter import *
import pygame
from PIL import Image, ImageTk

root = Tk()
root.title("Music.hub")
root.geometry("500x400")

# Obtain the absolute path to the icon file
home_dir = os.path.expanduser("~")
icon_path = os.path.join(home_dir, "Desktop/Media-Player/Images/logo.png")

# Set the icon for the root window
icon = Image.open(icon_path)
icon = icon.resize((32, 32), Image.ANTIALIAS)

# Set the icon photo for the root window
icon_photo = ImageTk.PhotoImage(icon)
root.tk.call("wm", "iconphoto", root._w, "-default", icon_photo)

pygame.mixer.init()

def play():
	pygame.mixer.music.load("Music/Ellos.mp3")
	pygame.mixer.music.play(loops=0)

my_button = Button(root, text="Play Song", font=("Helvetica", 32), command=play)
my_button.pack(pady=20)

root.mainloop()


