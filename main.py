from user import songDirectory
import tkinter as tk
from tkinter import messagebox
import librosa
import pickle
from tinytag import TinyTag
from glob import glob
from tkinter import filedialog

#Initialize ng empty list/array para sa mga kanta ni user
songList = []

#I-check muna ni tool kung may naka-save na ba na data si user. Yung data dito is yung location ng mga kanta ni user.
#Yung data is nakastore sa user.py, if walang laman yun, pupunta siya dito sa if statement sa baba netong comment na to. If merong laman, exit program na agad.
if(songDirectory == ""):
    root = tk.Tk()
    root.withdraw()

    #Dialog box lang to
    messagebox.showwarning("Warning", "Song directory not found. Select the folder where your songs are in.")

    #Initialize temporary array para sa mga makikitang mp3 at flac files ni user
    songs = []

    #Hihingiin na yung location ng mga kanta ni user
    songDirectory = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')

    #Eto ipe-prepare na yung pagupdate sa user.py para next time hindi na tanungin yung user ng location ng mga kanta ni user
    temp = open("user.py", "w")
    temp.write('songDirectory = "' + songDirectory + '"')
    messagebox.showinfo("Success!", "Song directory found, please wait. This will take a long time depending on the number of music you have.")

    #Dito i-check na ni tool(edited) if may flac and mp3 files yung folder ni user. Kasama na dito yung mga subfolder nung given directory.
    for x in glob(songDirectory + "/*.flac"):
        songs.append(x)

    for x in glob(songDirectory + "/*.mp3"):
        songs.append(x)

    for x in glob(songDirectory + "/**/*.flac"):
        songs.append(x)

    for x in glob(songDirectory + "/**/*.mp3"):
        songs.append(x)

    #Dito kukunin na yung data nung mga kanta. Eto yung BPM, Title, saka artist
    for x in songs:
        y, sr = librosa.load(x)
        audioFile = TinyTag.get(x)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        duration = librosa.get_duration(y = y, sr = sr)
        if(audioFile.title and audioFile.artist):
            songList.append([x, tempo, duration, audioFile.title, audioFile.artist])
        elif(audioFile.title):
            songList.append([x, tempo, duration, audioFile.title, "None"])
        elif(audioFile.artist):
            songList.append([x, tempo, duration, x, audioFile.artist])
        else:
            songList.append([x, tempo, duration, x, "None"])

    #etong statement na to is way siya para ma-save yung song array sa python file. Bale pwede mo nang mapasa yung array into another python file (y)
    with open("song_data.py", "wb") as fp:
        pickle.dump(songList, fp)

    #If walang kanta yung folder na binigay ni user, ty na lang
    if(len(songList) == 0):
        messagebox.showinfo("Error!", "No songs found on the folder provided.")
    #If successful, ty ulit
    else:
        messagebox.showinfo("Success!", "Audio loading finished, please restart the program")

