# import libraries
from signal import signal
from tkinter import *
from turtle import bgcolor
import pygame
import os.path
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
from pedalboard import Pedalboard, Chorus, Reverb, Compressor, Delay, Distortion, Gain
from pedalboard.io import AudioFile
import librosa
import soundfile as sf
import wave
import numpy as np
root = Tk()
root.title("Music.hub")
root.geometry("600x400")

board = Pedalboard();

pygame.mixer.init()

global pause
pause = False
global is_sliding
is_sliding = False

song_box = Listbox(root, bg="white", fg="black", selectbackground="gray", selectforeground="white", font=("Helvetica", 10), relief=FLAT)
song_box.pack(pady=20, padx=20, fill=BOTH, expand=True)


style = ttk.Style()
style.theme_use("clam")
style.configure("TButton",
                background="#f47676",
                foreground="white",
                font=("Helvetica", 10),
                relief=FLAT,
                width=10,
                padding=5)
style.map("TButton",
          background=[('active', '#f47676')])

style.configure("TScale",
                background="#f47676",
                troughcolor="#424242",
                sliderlength=20,
                sliderthickness=10,
                troughrelief=FLAT,
                gripcount=0)
style.map("TScale",
          background=[('active', '#f47676')])

song_dict = {}


def play_time():
    if pygame.mixer.music.get_busy() and not pause and not is_sliding:
        current_time = pygame.mixer.music.get_pos() / 1000
        converted_time = time.strftime("%M:%S", time.gmtime(current_time))
        song_title = song_box.get(ACTIVE)
        song_path = song_dict.get(song_title)
        song_mut = MP3(song_path)
        song_len = song_mut.info.length
        converted_song_len = time.strftime("%M:%S", time.gmtime(song_len))
        if int(my_slider.get()) == int(song_len):
            pass
        elif int(my_slider.get()) == int(current_time):
            slider_position = int(song_len)
            my_slider.config(to=slider_position, value=current_time)
        else:
            slider_position = int(song_len)
            my_slider.config(to=slider_position, value=my_slider.get())
            converted_time = time.strftime("%M:%S", time.gmtime(int(my_slider.get())))
            status_bar.config(text=f"{converted_time}/{converted_song_len}")
            next_time = int(my_slider.get()) + 1
            my_slider.set(next_time)

    status_bar.after(1000, play_time)


def play_music():
    song_title = song_box.get(ACTIVE)
    song_path = song_dict.get(song_title)
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(loops=0)
    update_status_bar()
    play_time()


def update_status_bar():
    song_title = song_box.get(ACTIVE)
    song_path = song_dict.get(song_title)
    song_mut = MP3(song_path)
    song_len = song_mut.info.length
    converted_song_len = time.strftime("%M:%S", time.gmtime(song_len))

def add_songs():
    songs = filedialog.askopenfilenames(initialdir="Music/", title="Choose songs", filetypes=(("MP3 Files", "*.mp3"),))
    for song in songs:
        song_title = os.path.basename(song)
        song_title = song_title.replace(".mp3", "")
        song_box.insert(END, song_title)
        song_dict[song_title] = song
 
def remove_song():
    selected_song = song_box.curselection()
    song_title = song_box.get(selected_song)
    song_box.delete(selected_song)
    del song_dict[song_title]


def clear_songs():
    song_box.delete(0, END)
    song_dict.clear()


def pause_music():
    global pause
    if not pause:
        pygame.mixer.music.pause()
        pause = True
    else:
        pygame.mixer.music.unpause()
        pause = False


def next_song():
    selected_song = song_box.curselection()
    next_song = (selected_song[0] + 1) % song_box.size()
    song_box.selection_clear(0, END)
    song_box.activate(next_song)
    song_box.selection_set(next_song, last=None)
    my_slider.set(0)  
    play_music()


def previous_song():
    selected_song = song_box.curselection()
    prev_song = (selected_song[0] - 1 + song_box.size()) % song_box.size()
    song_box.selection_clear(0, END)
    song_box.activate(prev_song)
    song_box.selection_set(prev_song, last=None)
    my_slider.set(0)  
    play_music()


def slide(event):
    global is_sliding
    is_sliding = True
    song_title = song_box.get(ACTIVE)
    song_path = song_dict.get(song_title)
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))
    volume = volume_scale.get() / 100
    pygame.mixer.music.set_volume(volume)


def release_position(event):
    global is_sliding
    is_sliding = False
    song_title = song_box.get(ACTIVE)
    song_path = song_dict.get(song_title)
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))
    volume = volume_scale.get() / 100
    pygame.mixer.music.set_volume(volume)
    update_status_bar()


def release_volume(event):
    volume = volume_scale.get() / 100
    pygame.mixer.music.set_volume(volume)

def compress():
            # Add a compressor pedal
            signal,sm= librosa.load(song_box.get(ACTIVE))
            tmp1 = librosa.effects.time_stretch(signal,rate=3)
            sf.write("args1.wav", tmp1, sm)
            pygame.mixer.music.load("args1.wav")
            pygame.mixer.music.play()
            wav0=wave.open("args1.wav", "r")
            raw=wav0.readframes(-1)
            raw=np.frombuffer(raw,"int16")
            sampleRate=wav0.getframerate()

def expansion():
            # Add a compressor pedal
            signal,sm= librosa.load(song_box.get(ACTIVE))
            tmp1 = librosa.effects.time_stretch(signal,rate=0.5)
            sf.write("args2.wav", tmp1, sm)
            pygame.mixer.music.load("args2.wav")
            pygame.mixer.music.play()
            wav0=wave.open("args2.wav", "r")
            raw=wav0.readframes(-1)
            raw=np.frombuffer(raw,"int16")
            sampleRate=wav0.getframerate()

def increase_amp():
       signal,sm= librosa.load(song_box.get(ACTIVE))
       tmp1 = librosa.effects.pitch_shift(signal,sr=sm, n_steps = 7)
       sf.write("args3.wav", tmp1, sm)
       pygame.mixer.music.load("args3.wav")
       pygame.mixer.music.play()

def decrease_amp():
       signal,sm= librosa.load(song_box.get(ACTIVE))
       tmp1 = librosa.effects.pitch_shift(signal,sr=sm, n_steps = -7)
       sf.write("args4.wav", tmp1, sm)
       pygame.mixer.music.load("args4.wav")
       pygame.mixer.music.play()


# Creating buttons icons
next_ico = PhotoImage(file="Icons/next.png").subsample(2, 2)
back_ico = PhotoImage(file="Icons/previous.png").subsample(2, 2)
play_ico = PhotoImage(file="Icons/play.png").subsample(2, 2)
pause_ico = PhotoImage(file="Icons/pause.png").subsample(2, 2)
add_ico = PhotoImage(file="Icons/add.png").subsample(2, 2)
remove_ico = PhotoImage(file="Icons/remove.png").subsample(2, 2)
clear_ico = PhotoImage(file="Icons/remove.png").subsample(2, 2)

# Creating control frame
control_frame = Frame(root)
control_frame.pack(pady=10)

# Creating control buttons
next_button = Button(control_frame, image=next_ico, borderwidth=0, command=next_song)
back_button = Button(control_frame, image=back_ico, borderwidth=0, command=previous_song)
play_button = Button(control_frame, image=play_ico, borderwidth=0, command=play_music)
pause_button = Button(control_frame, image=pause_ico, borderwidth=0, command=pause_music)
add_button = Button(control_frame, image=add_ico, borderwidth=0, command=add_songs)
remove_button = Button(control_frame, image=remove_ico, borderwidth=0, command=remove_song)
clear_button = Button(control_frame, image=clear_ico, borderwidth=0, command=clear_songs)

back_button.grid(row=0, column=0, padx=5)
play_button.grid(row=0, column=1, padx=5)
pause_button.grid(row=0, column=2, padx=5)
next_button.grid(row=0, column=3, padx=5)
add_button.grid(row=0, column=4, padx=5)
remove_button.grid(row=0, column=5, padx=5)
clear_button.grid(row=0, column=6, padx=5)

# Creating status bar
status_bar = Label(root, text='', bd=1, relief=SUNKEN, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Creating Menu
my_menu = Menu(root)
root.config(menu=my_menu)

features = Menu(my_menu)
my_menu.add_cascade(label="Effects", menu=features)
features.add_command(label="Compress", command=compress)
features.add_command(label="expansion",command= expansion)
features.add_command(label="increase_amp", command=increase_amp)
features.add_command(label="decrease_amp", command=decrease_amp)


# Creating slider
slider_frame = Frame(root)
slider_frame.pack(pady=10)

my_slider = ttk.Scale(slider_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=360)
my_slider.pack(fill=X)

volume_scale = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, length=200)
volume_scale.set(100)
volume_scale.pack(pady=10)

my_slider.bind("<ButtonRelease-1>", release_position)
volume_scale.bind("<ButtonRelease-1>", release_volume)


root.mainloop()
