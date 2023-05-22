# import libraries
from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

# Create a GUI window
root = Tk()
root.title("Music.hub")
root.geometry("500x500")

pygame.mixer.init()

# Global variable for pause state
global pause
pause = False

# Create a listbox to display songs
song_box = Listbox(root, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

# Create a dictionary to map song titles to file paths
song_dict = {}

# Function to update the play time on the status bar
def play_time():
    current_time = pygame.mixer.music.get_pos() / 1000
    converted_time = time.strftime("%M:%S", time.gmtime(current_time))
    status_bar.after(1000, play_time)
    current_song = song_box.curselection()
    song_title = song_box.get(current_song)
    song = song_dict[song_title]
    song_mut = MP3(song)
    global song_len
    song_len = song_mut.info.length
    my_slider.config(value=current_time)
    converted_song_len = time.strftime("%M:%S", time.gmtime(song_len))
    status_bar.config(text=f'{converted_time}/{converted_song_len}')

# Function to play the selected song
def Play():
    song_title = song_box.get(ACTIVE)
    song = song_dict[song_title]
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    play_time()
    slider_position = int(song_len)
    my_slider.config(to=slider_position, value=0)

# Function to stop the currently playing song
def Stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    status_bar.config(text='')

# Function to add multiple songs to the song list
def add_many_song():
    songs = filedialog.askopenfilenames(initialdir="Music/", title="Choose a song", filetypes=(("MP3 Files", ".mp3"),))
    for song in songs:
        song_title = song.split("/")[-1]  # Extract the title from the file path
        song_title = song_title.replace(".mp3", "")  # Remove the .mp3 extension
        song_dict[song_title] = song
        song_box.insert(END, song_title)

# Function to remove the selected song from the song list
def remove_song():
    current_song = song_box.curselection()
    song_title = song_box.get(current_song)
    del song_dict[song_title]
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

# Function to remove all songs from the song list
def remove_all_songs():
    song_dict.clear()
    song_box.delete(0, END)
    pygame.mixer.music.stop()

# Function to pause or unpause the currently playing song
def Pause():
    global pause
    if not pause:
        pygame.mixer.music.pause()
        pause = True
    else:
        pygame.mixer.music.unpause()
        pause = False

# Function to play the next song in the song list
def next_song():
    current_song = song_box.curselection()
    next_song_index = (current_song[0] + 1) % song_box.size()
    if next_song_index < song_box.size():
        song_box.selection_clear(0, END)
        song_box.activate(next_song_index)
        song_box.selection_set(next_song_index, last=None)
        song_title = song_box.get(next_song_index)
        song = song_dict[song_title]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

# Function to play the previous song in the song list
def previous_song():
    current_song = song_box.curselection()
    prev_song_index = (current_song[0] - 1 + song_box.size()) % song_box.size()
    if prev_song_index >= 0:
        song_box.selection_clear(0, END)
        song_box.activate(prev_song_index)
        song_box.selection_set(prev_song_index, last=None)
        song_title = song_box.get(prev_song_index)
        song = song_dict[song_title]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

# Function to update the slider label with the current slider value
def slide(x):
    slider_label.config(text=int(my_slider.get()))

# Load the icons for control buttons
next_ico = PhotoImage(file="Icons/next.png")
back_ico = PhotoImage(file="Icons/previous.png")
play_ico = PhotoImage(file="Icons/play.png")
pause_ico = PhotoImage(file="Icons/pause.png")
stop_ico = PhotoImage(file="Icons/stop.png")
up_ico = PhotoImage(file="Icons/upload.png")

# Create a frame for control buttons
control_frame = Frame(root)
control_frame.pack()

# Create control buttons with icons and assign commands
next_button = Button(control_frame, image=next_ico, borderwidth=0, command=next_song)
back_button = Button(control_frame, image=back_ico, borderwidth=0, command=previous_song)
play_button = Button(control_frame, image=play_ico, borderwidth=0, command=Play)
pause_button = Button(control_frame, image=pause_ico, borderwidth=0, command=Pause)
stop_button = Button(control_frame, image=stop_ico, borderwidth=0, command=Stop)
up_button = Button(control_frame, image=up_ico, borderwidth=0, command=add_many_song)

next_button.grid(row=0, column=5, padx=10)
back_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=3, padx=10)
pause_button.grid(row=0, column=4, padx=10)
stop_button.grid(row=0, column=2, padx=10)
up_button.grid(row=1, column=3, pady=10)

# Create a menu for removing songs
my_menu = Menu(root)
root.config(menu=my_menu)
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove song", menu=remove_song_menu)
remove_song_menu.add_command(label="Remove one song", command=remove_song)
remove_song_menu.add_command(label="Remove all songs", command=remove_all_songs)

# Create a status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Create a slider for song progress
my_slider = ttk.Scale(root, from_=0, length=360, to=100, orient=HORIZONTAL, value=0, command=slide)
my_slider.pack(pady=20)

slider_label = Label(root, text="0")
slider_label.pack(pady=10)

# Execute the Tkinter event loop
root.mainloop()
