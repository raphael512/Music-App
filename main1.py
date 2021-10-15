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

class cancelId:
    def __init__(self):
        self.id = [] 
        self.time = 0

    def add(self, num):
        self.id.append(num)

    def getId(self):
        return self.id

    def getTime(self):
        return self.time

def playSong(song):
    temp = tv.item(song, 'values')   
    timeArr = temp[2].split(':')
    timeArr = int(int(timeArr[0])*60) + int(timeArr[1])
    progressBarFunc(int(timeArr*.01*1000))
    sing = vlc.MediaPlayer(songDir[temp[0]])
    sing.play()
    """ time.sleep(10)
    sing.stop() """
    return

def getInterval(songLength):
    return 

def cancelAll():
    arr = hehe.getId()
    for x in arr:
        root.after_cancel(x)


def progressBarFunc(time, x = 0):
    if(x+1) < 100:
        playButton['state'] = DISABLED
        temp = PhotoImage(file = "./res/progBars/"+ str(x) +"-progBar.png")
        progressBar.configure(image=temp)
        progressBar.image = temp
        root.after_id = root.after(time, lambda: progressBarFunc(time, x+1))
        hehe.add(root.after_id)
    else:
        playButton['state'] = NORMAL
        temp = PhotoImage(file = "./res/progBars/0-progBar.png")
        progressBar.configure(image=temp)
        progressBar.image = temp
        playSong(tv.focus())
    
    
    

root = Tk()
root.geometry("1000x650")
root.title("MoodSic")
fnt = font.Font(size = 12)
w = PanedWindow(root)
controlPanel = PanedWindow(root)
tv = ttk.Treeview(w, height = 25)
hehe = cancelId()
songDir = {}


lbl = Label(root, text = "My Music", font = 'Helvetica 18 bold')
detectEmotion = Button(root, text = "DETECT EMOTION", font = 'Arial 11 bold', background = "#AED5C0")

playImage = PhotoImage(file = "./res/playButton.png")
nextImage = PhotoImage(file = "./res/nextButton.png")
prevImage = PhotoImage(file = "./res/prevButton.png")
progBar = PhotoImage(file = "./res/progBars/0-progBar.png")
progressBar = Label(root, image = progBar, borderwidth=0)

""" playButton = Button(controlPanel, image = playImage, font = fnt, command = cancelAll) """
playButton = Button(controlPanel, image = playImage, font = fnt, command = lambda: playSong(tv.focus()))
nextButton = Button(controlPanel, image = nextImage, font = fnt, command = lambda: progressBarFunc(1000))
previousButton = Button(controlPanel, image = prevImage, font = fnt)

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