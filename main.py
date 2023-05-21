# import libraries
import os
from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
# Create a GUI window
root = Tk()
root.title("Music.hub")
root.geometry("500x400")

pygame.mixer.init();

global pause
pause = False

song_box = Listbox(root, bg="black" , fg="green" , width=60 , selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

def play_time():
       current_time = pygame.mixer.music.get_pos() /1000      
       converted_time = time.strftime("%M:%S" , time.gmtime(current_time))     
       status_bar.after(1000, play_time)
       current_song = song_box.curselection()
       song = song_box.get(current_song)
       song_mut = MP3(song)
       song_len = song_mut.info.length
       converted_song_len = time.strftime("%M:%S" , time.gmtime(song_len))
       status_bar.config(text=F'{converted_time}/{converted_song_len}')




def Play():
       song = song_box.get(ACTIVE)
       pygame.mixer.music.load(song)
       pygame.mixer.music.play(loops = 0)
       play_time()

def Stop():
       pygame.mixer.music.stop()
       song_box.selection_clear(ACTIVE)
       status_bar.config(text='')

def add_song():
       song = filedialog.askopenfilename(initialdir="Music/", title="choose a song" , filetypes=(("mp3 Files", ".mp3"), ))
       song_box.insert(END, song)

def add_many_song():
       songs = filedialog.askopenfilenames(initialdir="Music/", title="choose a song" , filetypes=(("mp3 Files", ".mp3"), ))
       for song in songs:
              song_box.insert(END,song)

def remove_song():
       song_box.delete(ANCHOR)
       pygame.mixer.music.stop()

def remove_all_songs():
       song_box.delete(0,END)
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
       nxtsong = song_box.curselection()
       nxtsong = nxtsong[0] + 1
       song = song_box.get(nxtsong)
       pygame.mixer.music.load(song)
       pygame.mixer.music.play(loops=0)
       song_box.select_clear(0,END)
       song_box.activate(nxtsong)
       song_box.select_set(nxtsong, last=None)

def previous_song():
       prevsong = song_box.curselection()
       prevsong = prevsong[0] - 1
       song = song_box.get(prevsong)
       pygame.mixer.music.load(song)
       pygame.mixer.music.play(loops=0)
       song_box.select_clear(0,END)
       song_box.activate(prevsong)
       song_box.select_set(prevsong, last=None)



next_ico = PhotoImage(file="Icons/next.png")
back_ico = PhotoImage(file="Icons/previous.png")
play_ico = PhotoImage(file="Icons/play.png")
pause_ico = PhotoImage(file="Icons/pause.png")
stop_ico = PhotoImage(file="Icons/stop.png")

control_frame = Frame(root)
control_frame.pack()

next_button = Button(control_frame,image=next_ico, borderwidth=0, command= next_song)
back_button = Button(control_frame,image=back_ico, borderwidth=0, command = previous_song)
play_button = Button(control_frame,image=play_ico, borderwidth=0 , command= Play)
pause_butoon =Button(control_frame,image=pause_ico, borderwidth=0, command= Pause)
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

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove song", menu=remove_song_menu)
remove_song_menu.add_command(label="Remove one song" , command=remove_song)
remove_song_menu.add_command(label="Remove all songs" , command=remove_all_songs)

status_bar = Label(root, text='' , bd=1, relief=GROOVE , anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)      
# Execute Tkinter
root.mainloop()