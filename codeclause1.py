import tkinter as tk
from tkinter import filedialog
import pygame
import os
import time

def play_music():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        status_label.config(text="Playing: " + os.path.basename(current_track))
        paused = False
    else:
        selected_song = playlistbox.curselection()
        if selected_song:
            selected_song = int(selected_song[0])
            play_selected_track(selected_song)

def stop_music():
    pygame.mixer.music.stop()
    status_label.config(text="Stopped")

def pause_music():
    global paused
    if not paused:
        pygame.mixer.music.pause()
        status_label.config(text="Paused")
        paused = True

def resume_music():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        status_label.config(text="Playing: " + os.path.basename(current_track))
        paused = False

def add_to_playlist():
    files = filedialog.askopenfilenames(title="Select Audio Files", filetypes=[("Audio files", "*.mp3 *.wav")])
    for file in files:
        playlistbox.insert(tk.END, os.path.basename(file))
        playlist.append(file)

def play_selected_track(selected_song):
    global current_track
    selected_song_path = playlist[selected_song]
    pygame.mixer.music.load(selected_song_path)
    pygame.mixer.music.play()
    current_track = selected_song_path
    status_label.config(text="Playing: " + os.path.basename(selected_song_path))

def next_track():
    current_index = playlist.index(current_track)
    if current_index + 1 < len(playlist):
        play_selected_track(current_index + 1)

def previous_track():
    current_index = playlist.index(current_track)
    if current_index > 0:
        play_selected_track(current_index - 1)

def set_volume(volume):
    pygame.mixer.music.set_volume(volume / 100)

def update_position():
    position = pygame.mixer.music.get_pos() / 1000  # Get playback position in seconds
    position_label.config(text="Position: {:.2f} sec".format(position))
    root.after(1000, update_position)

root = tk.Tk()
root.title("Python Music Player")

playlistbox = tk.Listbox(root, selectmode=tk.SINGLE)
playlistbox.pack()

add_button = tk.Button(root, text="Add Songs", command=add_to_playlist)
add_button.pack()

play_button = tk.Button(root, text="Play", command=play_music)
play_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_music)
stop_button.pack()

pause_button = tk.Button(root, text="Pause", command=pause_music)
pause_button.pack()

resume_button = tk.Button(root, text="Resume", command=resume_music)
resume_button.pack()

next_button = tk.Button(root, text="Next", command=next_track)
next_button.pack()

previous_button = tk.Button(root, text="Previous", command=previous_track)
previous_button.pack()

volume_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", command=set_volume)
volume_scale.pack()

status_label = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(side=tk.BOTTOM, fill=tk.X)

position_label = tk.Label(root, text="Position: 0.00 sec", bd=1, relief=tk.SUNKEN, anchor=tk.W)
position_label.pack(side=tk.BOTTOM, fill=tk.X)

pygame.mixer.init()
playlist = []
paused = False
current_track = ""

update_position()  # Start updating the playback position

root.mainloop()
