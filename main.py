
root = Tk()
root.title("Music.hub")
root.geometry("500x400")

pygame.mixer.init();

global pause
pause = False
# import libraries
import os
from tkinter import *
import pygame
from tkinter import filedialog
# Create a GUI window
song_box = Listbox(root, bg="black" , fg="blue" , width=60 , selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

def Play():
       song = song_box.get(ACTIVE)
       pygame.mixer.music.load(song)
       pygame.mixer.music.play(loops = 0)

def Stop():
       pygame.mixer.music.stop()
       song_box.selection_clear(ACTIVE)
def add_song():
       song = filedialog.askopenfilename(initialdir="Music/", title="choose a song" , filetypes=(("mp3 Files", ".mp3"), ))
       song_box.insert(END, song)

def add_many_song():
       songs = filedialog.askopenfilenames(initialdir="Music/", title="choose a song" , filetypes=(("mp3 Files", ".mp3"), ))
       for song in songs:
              song_box.insert(END,song)

def Pause(is_paused):
       global pause
       pause = is_paused
       if not pause:
              pygame.mixer.music.pause()
              pause = True
       else:
              pygame.mixer.music.unpause()
              pause = False

def next_song():
       nxtsong = song_box.curselection()
       song = str(nxtsong+1)
       pygame.mixer.music.load(song)
       pygame.mixer.music.play(loops=0)

next_ico = PhotoImage(file="Images/next.png")
back_ico = PhotoImage(file="Images/back.png")
play_ico = PhotoImage(file="Images/play.png")
pause_ico = PhotoImage(file="Images/pause.png")
stop_ico = PhotoImage(file="Images/stop.png")

control_frame = Frame(root)
control_frame.pack()

next_button = Button(control_frame,image=next_ico, borderwidth=0, command= next_song)
back_button = Button(control_frame,image=back_ico, borderwidth=0)
play_button = Button(control_frame,image=play_ico, borderwidth=0 , command= Play)
pause_butoon =Button(control_frame,image=pause_ico, borderwidth=0, command=lambda: Pause(pause) )
stop_butoon = Button(control_frame,image=stop_ico, borderwidth=0, command= Stop)

next_button.grid(row=0, column=5, padx=10)
back_button.grid(row = 0, column=1,padx=10)
play_button.grid(row =0, column=3,padx=10)
pause_butoon.grid(row = 0 , column=4,padx=10)
stop_butoon.grid(row = 0, column=2,padx=10)

my_menu = Menu(root)
root.config(menu=my_menu)

add_song_to_menu = Menu(my_menu)
my_menu.add_cascade(label="Add song", menu=add_song_to_menu)
add_song_to_menu.add_command(label="Add one song" , command= add_song)
add_song_to_menu.add_command(label="Add many songs" , command= add_many_song)

# Execute Tkinter
root.mainloop()