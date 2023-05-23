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
# Create a GUI window
root = Tk()
root.title("Music.hub")
root.geometry("600x800")
board = Pedalboard();

pygame.mixer.init()

global pause
pause = False

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


def Play():
    song = song_box.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    volume = volume_scale.get() / 100
    pygame.mixer.music.set_volume(volume)
    play_time()

def add_many_song():
    songs = filedialog.askopenfilenames(initialdir="Music/", title="Choose a song", filetypes=(("mp3 Files", ".mp3"),))
    for song in songs:
        song_box.insert(END, song)


def remove_song():
    status_bar.config(text='')
    my_slider.config(value=0)
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()


def remove_all_songs():
    status_bar.config(text='')
    my_slider.config(value=0)
    song_box.delete(0, END)
    pygame.mixer.music.stop()


def Pause():
    global pause
    if not pause:
        pygame.mixer.music.pause()
        pause = True
    else:
        pygame.mixer.music.unpause()
        pause = False


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
            board.append(Compressor(threshold_db=-20, ratio=5, attack_ms=10, release_ms=50))
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


next_ico = PhotoImage(file="Icons/next.png")
back_ico = PhotoImage(file="Icons/previous.png")
play_ico = PhotoImage(file="Icons/play.png")
pause_ico = PhotoImage(file="Icons/pause.png")
up_ico = PhotoImage(file="Icons/upload.png")

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



my_menu = Menu(root)
root.config(menu=my_menu)

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove song", menu=remove_song_menu)
remove_song_menu.add_command(label="Remove one song", command=remove_song)
remove_song_menu.add_command(label="Remove all songs", command=remove_all_songs)

features = Menu(my_menu)
my_menu.add_cascade(label="Effects", menu=features)
features.add_command(label="Compress", command=compress)
features.add_command(label="expansion",command= expansion)
features.add_command(label="increase_amp", command=increase_amp)
features.add_command(label="decrease_amp", command=decrease_amp)

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
       