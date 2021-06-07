from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import messagebox
import tkinter
from tkinter import font
import pickle

def playSong():
    if(playButton['text'] == "Pause"):
        val = progressBar['value']
        progressBar.stop()
        progressBar['value'] = val
        playButton['text'] = "Play"
    else:
        playButton['text'] = "Pause"
        progressBar.start(interval = 2150)

def getInterval(songLength):
    return  

root = Tk()
root.geometry("800x700")
root.title("MoodSic")
fnt = font.Font(size = 12)
w = PanedWindow(root)
controlPanel = PanedWindow(root)

sb = Scrollbar(w)
sb.pack(side = RIGHT, fill = BOTH)
lb = Listbox(w, height = 33, width = 90, font = fnt, yscrollcommand=sb.set)
lb.pack(side = LEFT)

playButton = Button(controlPanel, text = "Play", font = fnt, command = playSong)
nextButton = Button(controlPanel, text = "Next", font = fnt)
previousButton = Button(controlPanel, text = "Previous", font = fnt)

previousButton.grid(row = 0, column = 0, padx = 20)
playButton.grid(row = 0, column = 1, padx = 20)
nextButton.grid(row = 0, column = 2, padx = 20)

progressBar = Progressbar(root, orient = HORIZONTAL, length = 600, mode = 'determinate')

w.pack(side = TOP, fill = "x")
progressBar.place(x = 70, y = 635)
controlPanel.place(x = 250, y = 660)

with open("song_data.py", "rb") as fp:
    temp = pickle.load(fp)

for x in range(len(temp)):
    lb.insert(x, temp[x][0])


root.mainloop()