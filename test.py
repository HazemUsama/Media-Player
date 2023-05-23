# import libraries
from tkinter import *
from turtle import bgcolor
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
from pedalboard import Pedalboard, Chorus, Reverb, Compressor, Delay, Distortion, Gain
from pedalboard.io import AudioFile
# Create a GUI window
root = Tk()
root.title("Music.hub")
root.geometry("600x600")
board = Pedalboard();

pygame.mixer.init()

# Global variable for pause state
global pause
pause = False

song_box = Listbox(root, bg="#121212", fg="#FFFFFF", selectbackground="#4CAF50", selectforeground="#FFFFFF", bd=0,
                   font=("Arial", 10))
song_box.pack(pady=(20, 10), padx=(int(root.winfo_width() * 0.2), int(root.winfo_width() * 0.2)), fill=BOTH, expand=True)


# Create a dictionary to map song titles to file paths
song_dict = {}

# Function to update the play time on the status bar
def play_time():
    current_time = pygame.mixer.music.get_pos() / 1000
    converted_time = time.strftime("%M:%S", time.gmtime(current_time))
    song = song_box.get(ACTIVE)
    song_mut = MP3(song)
    global song_len
    song_len = song_mut.info.length
    converted_song_len = time.strftime("%M:%S", time.gmtime(song_len))
    if int(my_slider.get()) == int(song_len):
        pass
    elif pause:
        pass
    elif int(my_slider.get()) == int(current_time):
        slider_position = int(song_len)
        my_slider.config(to=slider_position, value=current_time)
    else:
        slider_position = int(song_len)
        my_slider.config(to=slider_position, value=my_slider.get())
        converted_time = time.strftime("%M:%S", time.gmtime(int(my_slider.get())))
        status_bar.config(text=F'{converted_time}/{converted_song_len}')
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    status_bar.after(1000, play_time)


# Function to play the selected song
def Play():
    song = song_box.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    volume = volume_scale.get() / 100
    pygame.mixer.music.set_volume(volume)
    play_time()


# Function to add multiple songs to the song list
def add_many_song():
    songs = filedialog.askopenfilenames(initialdir="Music/", title="Choose a song", filetypes=(("mp3 Files", ".mp3"),))
    for song in songs:
        song_box.insert(END, song)


# Function to remove the selected song from the song list
def remove_song():
    status_bar.config(text='')
    my_slider.config(value=0)
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()


# Function to remove all songs from the song list
def remove_all_songs():
    status_bar.config(text='')
    my_slider.config(value=0)
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
    status_bar.config(text='')
    my_slider.config(value=0)
    nxtsong = song_box.curselection()
    nxtsong = nxtsong[0] + 1
    song = song_box.get(nxtsong)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.select_clear(0, END)
    song_box.activate(nxtsong)
    song_box.select_set(nxtsong, last=None)


# Function to play the previous song in the song list
def previous_song():
    status_bar.config(text='')
    my_slider.config(value=0)
    prevsong = song_box.curselection()
    prevsong = prevsong[0] - 1
    song = song_box.get(prevsong)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.select_clear(0, END)
    song_box.activate(prevsong)
    song_box.select_set(prevsong, last=None)


# Function to update the slider label with the current slider value
def slide(x):
    song = song_box.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))
    volume = volume_scale.get() / 100
    pygame.mixer.music.set_volume(volume)

def reverb():
            # Add reverb effect
            board.append(Reverb(room_size=0.2))
            
def compress():
            # Add a compressor pedal
            board.append(Compressor(threshold_db=-20, ratio=5, attack_ms=10, release_ms=50))
            
def delay():
            # Add a delay pedal
            board.append(Delay(delay_seconds=0.2))
        
def distortion():
            # Add a distortion pedal
            board.append(Distortion(distortion=0.2))
            
            
def gain():
            board.append(Gain(gain_db=10))


# Load the icons for control buttons
next_ico = PhotoImage(file="Icons/next.png")
back_ico = PhotoImage(file="Icons/previous.png")
play_ico = PhotoImage(file="Icons/play.png")
pause_ico = PhotoImage(file="Icons/pause.png")
up_ico = PhotoImage(file="Icons/upload.png")

# Create a frame for control buttons
control_frame = Frame(root)
control_frame.pack()

next_button = Button(control_frame, image=next_ico, borderwidth=0, command=next_song)
back_button = Button(control_frame, image=back_ico, borderwidth=0, command=previous_song)
play_button = Button(control_frame, image=play_ico, borderwidth=0, command=Play)
pause_button = Button(control_frame, image=pause_ico, borderwidth=0, command=Pause)
up_button = Button(control_frame, image=up_ico, borderwidth=0, command=add_many_song)

next_button.grid(row=0, column=5, padx=10)
back_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=4, padx=10)
pause_button.grid(row=0, column=2, padx=10)
up_button.grid(row=0, column=3, padx=10)



# Create a menu for removing songs
my_menu = Menu(root)
root.config(menu=my_menu)
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove song", menu=remove_song_menu)
remove_song_menu.add_command(label="Remove one song", command=remove_song)
remove_song_menu.add_command(label="Remove all songs", command=remove_all_songs)

features = Menu(my_menu)
my_menu.add_cascade(label="Features", menu=features)
features.add_command(label="Compress", command=compress)
features.add_command(label="Delay", command=delay)
features.add_command(label="Gain", command=gain)
features.add_command(label="Reverb",command= reverb)

status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

my_slider = ttk.Scale(root, from_=0, length=360, to=100, orient=HORIZONTAL, value=0, command=slide)
my_slider.pack(fill=X, padx=root.winfo_screenmmwidth() * 0.2)

volume_scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=slide)
volume_scale.set(100)
volume_scale.pack(pady=0, padx=(int(root.winfo_screenmmwidth() * 0.9)), fill=X)

pedalboard = Pedalboard()  # Create the Pedalboard object

# Execute Tkinter
root.mainloop()
