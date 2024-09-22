from tkinter import filedialog
from tkinter import *
import pygame
import os

root = Tk()
root.title('Music Player')
root.geometry("500x300")

pygame.mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

songs = []
current_song = ""
paused = False
def load_music():
    global current_song
    root.directory = filedialog.askdirectory()

    songs.clear()
    songlist.delete(0, END)

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext =='.mp3':
            songs.append(song)
    for song in songs:
        songlist.insert("end", song)

    songlist.selection_set(0)
    current_song = songs[songlist.curselection()[0]]
    play_music()

def play_music():
    global current_song, paused

    current_song = songs[songlist.curselection()[0]]
    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, current_song))
        pygame.mixer.music.play()
        root.after(1000, check_song_end)
    else:
        pygame.mixer.music.unpause()
        paused = False


def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_music():
    global current_song, paused
    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song)+1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass

def prev_music():
    global current_song, paused

    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song)-1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass

def check_song_end():
    if not pygame.mixer.music.get_busy():
        next_music()
    else:
        root.after(1000, check_song_end)

def on_song_double_click(event):
    global current_song
    try:
        current_song = songs[songlist.curselection()[0]]  # Get the clicked song
        play_music()  # Play the selected song
    except:
        pass

organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label='Select Folder', command=load_music)
menubar.add_cascade(label='Organise', menu=organise_menu)

songlist = Listbox(root, bg="black", fg="green", width=100, height=15)
songlist.bind("<Double-1>", on_song_double_click)
songlist.pack()

play_btn_image = PhotoImage(file='play.png').subsample(16, 16)
pause_btn_image = PhotoImage(file='pause.png').subsample(16, 16)
next_btn_image = PhotoImage(file='next.png').subsample(16, 16)
prev_btn_image = PhotoImage(file='prev.png').subsample(16, 16)

control_frame = Frame(root)
control_frame.pack()

play_btn = Button(control_frame,image=play_btn_image, borderwidth=0, command=play_music)
pause_btn = Button(control_frame,image=pause_btn_image, borderwidth=0, command=pause_music)
next_btn = Button(control_frame,image=next_btn_image, borderwidth=0,command=next_music)
prev_btn = Button(control_frame,image=prev_btn_image, borderwidth=0,command=prev_music)

play_btn.grid(row=0, column=2, padx=7, pady=10)
pause_btn.grid(row=0, column=1, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
prev_btn.grid(row=0, column=0, padx=7, pady=10)

root.mainloop()