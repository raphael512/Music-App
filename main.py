from user import songDirectory
import tkinter as tk
from tkinter import messagebox
import librosa
import pickle
import eyed3
from tkinter import filedialog

songList = []

if(songDirectory == ""):
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("Warning", "Song directory not found. Select the folder where your songs are in.")

    dirname = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
    songDirectory = dirname
    temp = open("user.py", "w")
    temp.write('songDirectory = "' + dirname + '"')
    messagebox.showinfo("Success!", "Song directory found, please wait. This will take a long time depending on the number of music you have.")

    songs = librosa.util.find_files(songDirectory)
    for x in songs:
        y, sr = librosa.load(x)
        audioFile = eyed3.load(x)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        duration = librosa.get_duration(y = y, sr = sr)
        songList.append([x, tempo, duration, audioFile.tag.title, audioFile.tag.artist])

    with open("song_data.py", "wb") as fp:
        pickle.dump(songList, fp)

    if(len(songList) == 0):
        messagebox.showinfo("Error!", "No songs found on the folder provided.")
    else:
        messagebox.showinfo("Success!", "Audio loading finished, please restart the program")

