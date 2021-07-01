from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import messagebox
import tkinter
from tkinter import font
import pickle

def playSong():
    """ if(playButton['text'] == "Pause"):
        val = progressBar['value']
        progressBar.stop()
        progressBar['value'] = val
        playButton['text'] = "Play"
    else:
        playButton['text'] = "Pause"
        progressBar.start(interval = 2150) """
    return

def getInterval(songLength):
    return  

root = Tk()
root.geometry("1000x650")
root.title("MoodSic")
fnt = font.Font(size = 12)
w = PanedWindow(root)
controlPanel = PanedWindow(root)

""" sb = Scrollbar(w)
sb.pack(side = RIGHT, fill = BOTH)
lb = Listbox(w, height = 33, width = 90, font = fnt, yscrollcommand=sb.set)
lb.pack(side = LEFT) """

lbl = Label(root, text = "My Music", font = 'Helvetica 18 bold')
detectEmotion = Button(root, text = "DETECT EMOTION", font = 'Arial 11 bold', background = "#AED5C0")

playImage = PhotoImage(file = "./res/playButton.png")
nextImage = PhotoImage(file = "./res/nextButton.png")
prevImage = PhotoImage(file = "./res/prevButton.png")
progBar = PhotoImage(file = "./res/progBar.png")

playButton = Button(controlPanel, image = playImage, font = fnt, command = playSong)
nextButton = Button(controlPanel, image = nextImage, font = fnt)
previousButton = Button(controlPanel, image = prevImage, font = fnt)

previousButton.grid(row = 0, column = 0)
playButton.grid(row = 0, column = 1, padx = 30)
nextButton.grid(row = 0, column = 2)

progressBar = Label(root, image = progBar)

lbl.place(x = 170, y = 0)
w.place(x = 170, y = 40)
progressBar.place(x = 390, y = 625)
detectEmotion.place(x = 12, y = 490)
controlPanel.place(x = 550, y = 580)

with open("song_data.py", "rb") as fp:
    temp = pickle.load(fp)


tv = ttk.Treeview(w, height = 25)
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

for x in range(len(temp)):
    if(int(temp[x][2])%60 < 10):    
        tv.insert(parent='', index=x, iid=x, text='', values=(temp[x][3], temp[x][4], str(int(temp[x][2]/60)) + ':0' + str(int(temp[x][2])%60), int(temp[x][1])))
    else:
        tv.insert(parent='', index=x, iid=x, text='', values=(temp[x][3], temp[x][4], str(int(temp[x][2]/60)) + ':' + str(int(temp[x][2])%60), int(temp[x][1])))

tv.pack(fill = "x")

""" for x in range(len(temp)):
    lb.insert(x, temp[x][3])
    lb.insert(x, temp[x][3])
    lb.insert(x, temp[x][3]) """


root.mainloop()