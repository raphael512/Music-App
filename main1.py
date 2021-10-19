from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import messagebox
import tkinter
from tkinter import font
import pickle
import vlc
import time
from playlist import VLC
import random

class playing:
    def __init__(self):
        self.player = 0
        self.songHistory = []
        
    def play(self):
        self.player.play()

    def stop(self):
        self.player.stop()

    def setSong(self, songInfo):
        self.player = vlc.MediaPlayer(songInfo)

class stack:
    def __init__(self):
        self.arr = []

    def pop(self):
        self.arr.pop()

    def peek(self):
        return self.arr[-1]

    def add(self, item):
        self.arr.append(item)

    def length(self):
        return len(self.arr)
        
    def search(self, item):
        if item in self.arr:
            return True

    def clear(self):
        self.arr = []


class cancelId:
    def __init__(self):
        self.id = [] 
        self.time = 0
        self.flag = False

    def getFlag(self):
        return self.flag

    def setFlag(self, value):
        self.flag = value

    def add(self, num):
        self.id.append(num)

    def getId(self):
        return self.id

    def getTime(self):
        return self.time
8
def prevSong():
    if(songStack.length() == 0):
        return
    """ player.setSong(songStack.pop())
    player.play() """
    return

def playSong(song):
    if(hehe.getFlag() == True):
        playButton.configure(image=playImage)
        playButton.image = playImage
        player.stop()
        hehe.setFlag(False)
        songStack.clear()
        cancelAll()
        return
    playButton.configure(image=stopImage)
    playButton.image = stopImage
    hehe.setFlag(True)
    temp = tv.item(song, 'values')   
    timeArr = temp[2].split(':')
    timeArr = int(int(timeArr[0])*60) + int(timeArr[1])
    progressBarFunc(int(timeArr*.01*1000))
    player.setSong(songDir[temp[0]])
    songStack.add(songDir[temp[0]])
    player.play()
    return

def getInterval(songLength):
    return 

def cancelAll():
    arr = hehe.getId()
    for x in arr:
        root.after_cancel(x)


def progressBarFunc(time, x = 0):
    if(x+1) < 100:
        temp = PhotoImage(file = "./res/progBars/"+ str(x) +"-progBar.png")
        progressBar.configure(image=temp)
        progressBar.image = temp
        root.after_id = root.after(time, lambda: progressBarFunc(time, x+1))
        hehe.add(root.after_id)
    else:
        temp = PhotoImage(file = "./res/progBars/0-progBar.png")
        progressBar.configure(image=temp)
        progressBar.image = temp
        playSong(tv.focus())
    
def nextSong():
    nextSongIndex = random.randint(0, len(songData)-1)
    temp = tv.item(nextSongIndex, 'values')
    """ if(songStack.search(songDir[temp[0]])):
        nextSong() """
    tv.selection_set(nextSongIndex)
    tv.focus(nextSongIndex)
    if(hehe.getFlag() == True):
        player.stop()
        hehe.setFlag(False)
        cancelAll()
    playSong(tv.focus())


root = Tk()
root.geometry("1000x650")
root.title("MoodSic")
fnt = font.Font(size = 12)
w = PanedWindow(root)
controlPanel = PanedWindow(root)
tv = ttk.Treeview(w, height = 25, selectmode = "browse")
hehe = cancelId()
player = playing()
songStack = stack()
songDir = {}


lbl = Label(root, text = "My Music", font = 'Helvetica 18 bold')
detectEmotion = Button(root, text = "DETECT EMOTION", font = 'Arial 11 bold', background = "#AED5C0")

playImage = PhotoImage(file = "./res/playButton.png")
nextImage = PhotoImage(file = "./res/nextButton.png")
prevImage = PhotoImage(file = "./res/prevButton.png")
stopImage = PhotoImage(file = "./res/stopButton.png")
progBar = PhotoImage(file = "./res/progBars/0-progBar.png")
progressBar = Label(root, image = progBar, borderwidth=0)

""" playButton = Button(controlPanel, image = playImage, font = fnt, command = cancelAll) """
playButton = Button(controlPanel, image = playImage, font = fnt, command = lambda: playSong(tv.focus()))
nextButton = Button(controlPanel, image = nextImage, font = fnt, command = lambda: nextSong())
previousButton = Button(controlPanel, image = prevImage, font = fnt, command = lambda: prevSong())

previousButton.grid(row = 0, column = 0)
playButton.grid(row = 0, column = 1, padx = 30)
nextButton.grid(row = 0, column = 2)



lbl.place(x = 170, y = 0)
w.place(x = 170, y = 40)
progressBar.place(x = 315, y = 615)
detectEmotion.place(x = 12, y = 490)
controlPanel.place(x = 465, y = 573)

with open("song_data.py", "rb") as fp:
    songData = pickle.load(fp)

tv['columns']=('Title', 'Artist', 'Duration', 'Tempo')
tv.column('#0', width=0, stretch=NO)
tv.column('Title', anchor=CENTER, width=400)
tv.column('Artist', anchor=CENTER, width=200)
tv.column('Duration', anchor=CENTER, width=80)
tv.column('Tempo', anchor=CENTER, width=80)

tv.heading('#0', text='', anchor=CENTER)
tv.heading('Title', text='Title', anchor=CENTER)
tv.heading('Artist', text='Artist', anchor=CENTER)
tv.heading('Duration', text='Duration', anchor=CENTER)
tv.heading('Tempo', text='Tempo', anchor=CENTER)

for x in range(len(songData)):
    if(int(songData[x][2])%60 < 10):
        if(songData[x][3] == None):
            songDir[songData[x][0]] = songData[x][0]
            tv.insert(parent='', index=x, iid=x, text='', values=(songData[x][0], songData[x][4], str(int(songData[x][2]/60)) + ':0' + str(int(songData[x][2])%60), int(songData[x][1])))
        else:
            songDir[songData[x][3]] = songData[x][0]
            tv.insert(parent='', index=x, iid=x, text='', values=(songData[x][3], songData[x][4], str(int(songData[x][2]/60)) + ':0' + str(int(songData[x][2])%60), int(songData[x][1])))
    else:
        if(songData[x][3] == None):
            songDir[songData[x][0]] = songData[x][0]
            tv.insert(parent='', index=x, iid=x, text='', values=(songData[x][0], songData[x][4], str(int(songData[x][2]/60)) + ':' + str(int(songData[x][2])%60), int(songData[x][1])))
        else:
            songDir[songData[x][3]] = songData[x][0]
            tv.insert(parent='', index=x, iid=x, text='', values=(songData[x][3], songData[x][4], str(int(songData[x][2]/60)) + ':' + str(int(songData[x][2])%60), int(songData[x][1])))
tv.pack(fill = "x")



root.mainloop()