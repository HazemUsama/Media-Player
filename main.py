from multiprocessing.sharedctypes import Value
from tkinter import *
import os
import pygame
import time
from tkinter import filedialog
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from mutagen.mp3 import MP3
import random

class MusicPlayer:
    def __init__(self):
        self.root = Tk()
        self.root.title("Music.hub")
        self.root.geometry("600x400")
        self.root.configure(bg="#282828")

        icon_path = "Images/logo.png"

        # Set the icon for the root window
        icon = Image.open(icon_path)
        icon = icon.resize((32, 32), Image.ANTIALIAS)

        # Set the icon photo for the root window
        icon_photo = ImageTk.PhotoImage(icon)
        self.root.tk.call("wm", "iconphoto", self.root._w, "-default", icon_photo)
        pygame.mixer.init()

        self.song_list = []
        self.current_song = None
        self.song_slider = None
        self.status_bar = None
        self.repeat_mode = False
        self.shuffle_mode = False

        self.song_box = Listbox(self.root, bg="#121212", fg="#FFFFFF", selectbackground="#4CAF50",
                                selectforeground="#FFFFFF", bd=0, font=("Arial", 10))
        self.song_box.pack(pady=(20, 10), padx=(int(self.root.winfo_width() * 0.2), int(self.root.winfo_width() * 0.2)), fill=BOTH, expand=True)

        self.control_frame = Frame(self.root, bg="#282828")
        self.control_frame.pack(pady=(0, 20))

        next_ico = PhotoImage(file="Icons/next.png")
        previous_ico = PhotoImage(file="Icons/previous.png")
        play_ico = PhotoImage(file="Icons/play.png")
        pause_ico = PhotoImage(file="Icons/pause.png")
        stop_ico = PhotoImage(file="Icons/stop.png")
        upload_ico = PhotoImage(file="Icons/upload.png")
        shuffle_ico = PhotoImage(file="Icons/shuffle.png")
        repeat_ico = PhotoImage(file="Icons/repeat.png")
        volume_down_ico = PhotoImage(file="Icons/volume-down.png")
        volume_up_ico = PhotoImage(file="Icons/volume-up.png")

        self.button_previous = Button(self.control_frame, image=previous_ico, bd=0, bg="#282828",
                                      activebackground="#282828", command=self.previous_song)
        self.button_previous.grid(row=0, column=0, padx=5)

        self.button_play = Button(self.control_frame, image=play_ico, bd=0, bg="#282828", activebackground="#282828",
                                  command=self.play_selected_song)
        self.button_play.grid(row=0, column=1, padx=5)

        self.button_pause = Button(self.control_frame, image=pause_ico, bd=0, bg="#282828", activebackground="#282828",
                                   command=self.pause_song)
        self.button_pause.grid(row=0, column=2, padx=5)

        self.button_next = Button(self.control_frame, image=next_ico, bd=0, bg="#282828", activebackground="#282828",
                                  command=self.next_song)
        self.button_next.grid(row=0, column=4, padx=5)

        self.button_upload = Button(self.control_frame, image=upload_ico, bd=0, bg="#282828",
                                    activebackground="#282828", command=self.add_song)
        self.button_upload.grid(row=1, column=2, pady=(10, 0))

        self.song_slider = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, sliderlength=15, length=500,
                                 bg="#282828", fg="#4CAF50", activebackground="#4CAF50", troughcolor="#121212",
                                 command=self.slide)
        self.song_slider.pack(fill=X, padx = self.root.winfo_screenmmwidth()*0.2)

        self.volume_slider = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, sliderlength=15, length=200,
                                   bg="#282828", fg="#4CAF50", activebackground="#4CAF50", troughcolor="#121212",
                                   command=self.change_volume)
        self.volume_slider.set(50)
        self.volume_slider.pack(pady=(10, 0), padx=10)

        self.status_bar = Label(self.root, text='', bd=1, relief=GROOVE, anchor=E, bg="#121212", fg="#FFFFFF")
        self.status_bar.pack(fill=X, side=BOTTOM, ipady=2)

        my_menu = Menu(self.root, bg="#282828", fg="#FFFFFF")
        self.root.config(menu=my_menu)

        remove_song_menu = Menu(my_menu, bg="#282828", fg="#FFFFFF")
        my_menu.add_cascade(label="Remove song", menu=remove_song_menu)
        remove_song_menu.add_command(label="Remove one song", command=self.remove_song)
        remove_song_menu.add_command(label="Remove all songs", command=self.remove_all_songs)

        self.song_box.bind("<Double-Button-1>", self.play_selected_song)

        self.root.after(1000, self.update_status_bar)
        self.root.mainloop()

    def add_song(self):
        songs = filedialog.askopenfilenames(initialdir="Music/", title="Choose a song",
                                            filetypes=(("MP3 Files", "*.mp3"),))
        for song in songs:
            title = song.split("/")[-1]
            title = title.replace(".mp3", "")
            self.song_box.insert(END, title)
            self.song_list.append(song)

    def remove_song(self):
        selected_song = self.song_box.curselection()
        if selected_song:
            self.song_box.delete(selected_song)
            del self.song_list[selected_song[0]]

    def remove_all_songs(self):
        self.song_box.delete(0, END)
        self.song_list.clear()
        self.stop_song()

    def play_selected_song(self, event=None):
        selected_song = self.song_box.curselection()
        if selected_song:
            self.current_song = selected_song[0]
            song_path = self.song_list[self.current_song]
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play(loops = 0)
            self.update_status_bar()
            self.update_slider()
        else:
            self.stop_song()

    def pause_song(self):
        if pygame.mixer.music.get_busy():
            if pygame.mixer.music.get_pos() > 0:
                pygame.mixer.music.pause()

    def stop_song(self):
        pygame.mixer.music.stop()
        self.current_song = None
        self.song_box.selection_clear(ACTIVE)
        self.song_slider.set(0)
        self.status_bar.config(text='')

    def next_song(self):
        if self.shuffle_mode:
            self.current_song = random.randint(0, len(self.song_list) - 1)
        else:
            self.current_song = (self.current_song + 1) % len(self.song_list)
        self.play_selected_song()

    def previous_song(self):
        if self.shuffle_mode:
            self.current_song = random.randint(0, len(self.song_list) - 1)
        else:
            self.current_song = (self.current_song - 1 + len(self.song_list)) % len(self.song_list)
        self.play_selected_song()

    def slide(self, event=None):
        if self.current_song is not None:
            slider_value = self.song_slider.get()
            song_path = self.song_list[self.current_song]
            song_mut = MP3(song_path)
            song_len = song_mut.info.length
            play_time = int(song_len * (slider_value / 100))
            pygame.mixer.music.play(start=play_time)

    def update_slider(self):
        if self.current_song is not None:
            song_path = self.song_list[self.current_song]
            song_mut = MP3(song_path)
            song_len = song_mut.info.length
            current_time = pygame.mixer.music.get_pos();
            self.song_slider.config(value=current_time ,to=song_len)
    def update_status_bar(self):
        if self.current_song is not None:
            song_path = self.song_list[self.current_song]
            song_mut = MP3(song_path)
            song_len = song_mut.info.length
            current_time = pygame.mixer.music.get_pos() / 1000
            converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
            converted_song_len = time.strftime('%M:%S', time.gmtime(song_len))
            self.status_bar.after(1000, self.update_status_bar)
            self.status_bar.config(text= f'{converted_current_time} / {converted_song_len}')

    def change_volume(self, event=None):
        volume = float(self.volume_slider.get()) / 100
        pygame.mixer.music.set_volume(volume)


MusicPlayer()