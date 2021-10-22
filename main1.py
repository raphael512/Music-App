from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import messagebox
import tkinter
from tkinter import font
import pickle
import vlc
import time
import ai
from playlist import VLC
import random
from tinytag import TinyTag
from stack import stack
from cancel import cancelId

def countdown():
    wnd = Toplevel()
    wnd.title("Smile!")

    x = root.winfo_x()
    y = root.winfo_y()
    wnd.minsize(300, 300)
    wnd.geometry("+%d+%d" % (x + 400, y + 200))
    smileLabel = Label(wnd, text = "SMILE!", font = 'Helvetica 56 bold')
    smileLabel.place(x = 30, y = 5)
    countLabel = Label(wnd, text = "3", font = 'Helvetica 92 bold')
    countLabel.place(x = 115, y = 80)
    wnd.after(1000, lambda: changeLabel(countLabel, '2'))
    wnd.after(2000, lambda: changeLabel(countLabel, '1'))
    wnd.after(3000, lambda: changeLabel(countLabel, '0'))
    wnd.after(4000, detectEmotionFunc)

def detectEmotionFunc():
    ai.img_capture()
    emotion = ai.detect_emotion()
    if(emotion == 0):
        messagebox.showwarning("Warning!", "No face detected")
        return

    messagebox.showinfo("Hi", "You are " + str(emotion))
    

def getData():
    with open("song_data.py", "rb") as fp:
        tempArr = pickle.load(fp)

    return tempArr

def changeLabel(lbl, txt):
    lbl['text'] = txt

def prevSong():
    songStack.subIteration()
    if(nextButton['state'] == DISABLED):
        nextButton['state'] = NORMAL
    if(songStack.getIteration() == 0):
        previousButton['state'] = DISABLED
    
    tempArr = songStack.getCurrentItems()
    for child in tv.get_children():
        if(tempArr[0] in tv.item(child)['values']):
            tv.focus(child)
            tv.selection_set(child)
            break
    player.previous()
    cancelAll()
    progressBarFunc(getInterval(tempArr[1]))

def nextSong():
    songStack.addIteration()
    if(previousButton['state'] == DISABLED):
        previousButton['state'] = NORMAL
    if(songStack.getIteration() + 1 == songStack.length()):
        nextButton['state'] = DISABLED
    
    tempArr = songStack.getCurrentItems()
    for child in tv.get_children():
        if(tempArr[0] in tv.item(child)['values']):
            tv.focus(child)
            tv.selection_set(child)
            break
    player.next()
    cancelAll()
    progressBarFunc(getInterval(tempArr[1]))

def playSong(song):
    
    if(hehe.getFlag() == True):
        global songData
        playButton.configure(image=playImage)
        playButton.image = playImage
        player.stop()
        hehe.setFlag(False)
        songData = getData()
        songStack.clear()
        player.__init__()
        cancelAll()
        return
    playButton.configure(image=stopImage)
    playButton.image = stopImage
    nextButton['state'] = NORMAL
    hehe.setFlag(True)
    temp = tv.item(song, 'values')   
    timeArr = temp[2].split(':')
    timeArr = int(int(timeArr[0])*60) + int(timeArr[1])
    progressBarFunc(int(timeArr*.01*1000))

    player.add(songDir[temp[0]])
    audioTag = TinyTag.get(songDir[temp[0]])
    for x in range(len(songData)):
        if(songDir[temp[0]] in songData[x]):
            if(audioTag.title):
                songStack.add([audioTag.title, audioTag.duration])
            else:
                songStack.add([songDir[temp[0]], audioTag.duration])
            del songData[x]
            break

    while True:
        if(len(songData) == 0):
            break
        """ for x in range(len(songData)): """
        num = random.randint(0, len(songData)-1)
        audioTag = TinyTag.get(songData[num][0])
        if(audioTag.title):
            songStack.add([audioTag.title, audioTag.duration])
        else:
            songStack.add([songData[num][0], audioTag.duration])
        player.add(songData[num][0])
            
        del songData[num]
        continue
    

    player.play()
    return

def getInterval(duration):
    return int(duration*.01*1000)

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
        if(songStack.getIteration() + 1 == songStack.length()):
            playSong()
            return
        temp = PhotoImage(file = "./res/progBars/0-progBar.png")
        progressBar.configure(image=temp)
        progressBar.image = temp
        nextSong()

root = Tk()
root.geometry("1000x650")
root.title("MoodSic")
fnt = font.Font(size = 12)
w = PanedWindow(root)
controlPanel = PanedWindow(root)
tv = ttk.Treeview(w, height = 25, selectmode = "browse")
hehe = cancelId()
player = VLC()
songStack = stack()
songDir = {}


lbl = Label(root, text = "My Music", font = 'Helvetica 18 bold')
detectEmotion = Button(root, text = "DETECT EMOTION", font = 'Arial 11 bold', background = "#AED5C0", command = countdown)

playImage = PhotoImage(file = "./res/playButton.png")
nextImage = PhotoImage(file = "./res/nextButton.png")
prevImage = PhotoImage(file = "./res/prevButton.png")
stopImage = PhotoImage(file = "./res/stopButton.png")
progBar = PhotoImage(file = "./res/progBars/0-progBar.png")
progressBar = Label(root, image = progBar, borderwidth=0)

scrollBar = ttk.Scrollbar(root, orient ="vertical", command = tv.yview)
scrollBar.pack(side = 'right', fill = 'y')
tv.configure(yscrollcommand = scrollBar.set)

playButton = Button(controlPanel, image = playImage, font = fnt, command = lambda: playSong(tv.focus()))
nextButton = Button(controlPanel, image = nextImage, font = fnt, command = lambda: nextSong(), state = DISABLED)
previousButton = Button(controlPanel, image = prevImage, font = fnt, command = lambda: prevSong(), state = DISABLED)

previousButton.grid(row = 0, column = 0)
playButton.grid(row = 0, column = 1, padx = 30)
nextButton.grid(row = 0, column = 2)



lbl.place(x = 170, y = 0)
w.place(x = 170, y = 40)
progressBar.place(x = 315, y = 615)
detectEmotion.place(x = 12, y = 490)
controlPanel.place(x = 465, y = 573)

songData = getData()

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