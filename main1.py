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
from PIL import Image, ImageTk
import os


def on_closing():
    """ player.stop()
    root.destroy()
    cancelAll() """
    quit()

#function for passing data to Stack/playlist
def addToStack(source):
    player.__init__()
    songStack.__init__()
    for x in range(len(source)):
        if(int(source[x][2])%60 < 10):
           if(source[x][3] == None):
              songDir[source[x][0]] = source[x][0]
              tv.insert(parent='', index=x, iid=x, text='', values=(source[x][0], source[x][4], str(int(source[x][2]/60)) + ':0' + str(int(source[x][2])%60), int(source[x][1])))
           else:
              songDir[source[x][3]] = source[x][0]
              tv.insert(parent='', index=x, iid=x, text='', values=(source[x][3], source[x][4], str(int(source[x][2]/60)) + ':0' + str(int(source[x][2])%60), int(source[x][1])))
        else:
           if(source[x][3] == None):
              songDir[source[x][0]] = source[x][0]
              tv.insert(parent='', index=x, iid=x, text='', values=(source[x][0], source[x][4], str(int(source[x][2]/60)) + ':' + str(int(source[x][2])%60), int(source[x][1])))
           else:
              songDir[source[x][3]] = source[x][0]
              tv.insert(parent='', index=x, iid=x, text='', values=(source[x][3], source[x][4], str(int(source[x][2]/60)) + ':' + str(int(source[x][2])%60), int(source[x][1])))

#Puts focus on the song that is playing
def putFocus():
    tempArr = songStack.getCurrentItems()
    for child in tv.get_children():
        if(tempArr[0] in tv.item(child)['values']):
            tv.focus(child)
            tv.selection_set(child)
            break

#function to get data from song_data1.py (emotion-based playlist)
def getSpecific():
    with open("song_data1.py", "rb") as fp:
        tempArr2 = pickle.load(fp)

    return tempArr2

#function to write data to song_data1.py (emotion-based playlist)
def writeSpecific(source):
    with open("song_data1.py", "wb") as fp:
        pickle.dump(source, fp)

#function to get data from song_data.py (bare data from directory)
def getData():
    with open("song_data.py", "rb") as fp:
        tempArr = pickle.load(fp)

    return tempArr

#Main function for generating playlist for detect emotion function
def generatePlaylist(bpmfloor, bpmceiling):
    songDir.clear()
    tempGen = []
    hold = []
    for x in range(len(songData)):
        if (int(songData[x][1]) >= bpmfloor and int(songData[x][1]) <= bpmceiling):
            tempGen.append(songData[x])

    #Sorts playlist according to BPM, Ascending order
    hold = sorted(tempGen, key=lambda x: x[1])
    tempGen = hold
    addToStack(tempGen)
    writeSpecific(tempGen)
    songEmoData = tempGen

    tv.pack(fill = "x")
    temp = [tempGen[0][3], tempGen[0][2]]
    print(temp);
    songStack.add([temp[0], temp[1]])
    player.add(songDir[temp[0]]) #idadagdag yung song directory ng <title> sa playlist
    #[song directory, tempo, duration, title, artist] po
    for x in range(len(songEmoData)):
        if(x == 0):
            continue
        if(songDir[tempGen[x][3]] in songEmoData[x]):
            songStack.add([tempGen[x][3], tempGen[x][2]])
            player.add(tempGen[x][0])

    player.play()
    playButton.configure(image=stopImage)
    playButton.image = stopImage
    playButton.configure(command = lambda: playSongEmotion(tv.focus()))
    nextButton['state'] = NORMAL
    hehe.setFlag(True)

    putFocus()

    progressBarFunc(int(tempGen[0][2]*.01*1000))

#Takes emotion from detectEmotionFunc in order to create a playlist
def createPlaylist(emotion):
     if emotion == 'sad':
        generatePlaylist(0, 80)
     elif emotion == 'happy':
        generatePlaylist(81, 129)
     elif emotion == 'angry':
        generatePlaylist(130, 250)
     else:
        generatePlaylist(0, 1015)

#Eto yung big countdown pag pinindot yung detect emotion
def countdown():
    guard = hehe.getFlag()
    if guard == True:
        messagebox.showwarning("Warning!", "Stop the music first to access this feature")
    else:
        wnd = Toplevel()
        wnd.title("Smile!")

        x = root.winfo_x()
        y = root.winfo_y()
        wnd.minsize(300, 300)
        wnd.geometry("+%d+%d" % (x + 400, y + 200))
        smileLabel = Label(wnd, text = "Ready in", font = 'Helvetica 45 bold')
        smileLabel.place(x = 30, y = 5)
        countLabel = Label(wnd, text = "3", font = 'Helvetica 92 bold')
        countLabel.place(x = 115, y = 80)
        wnd.after(1000, lambda: changeLabel(countLabel, '2'))
        wnd.after(2000, lambda: changeLabel(countLabel, '1'))
        wnd.after(3000, lambda: changeLabel(countLabel, '0'))
        wnd.after(4000, detectEmotionFunc)
        wnd.after(5000, wnd.destroy)


#After nung countdown, ico-call to para magcapture ng image tapos makita yung emotion ni user
#CHECK MO YUNG AI.PY PARA DUN SA IMG_CAPTURE() SAKA DETECT_EMOTION()
def detectEmotionFunc():
    num = ai.img_capture()
    emotion = ai.detect_emotion()
    if(emotion == 0):
        messagebox.showwarning("Warning!", "No face detected")

    """ messagebox.showinfo("Hi", "You are " + str(emotion)) """
    emoWnd = Toplevel()
    emoWnd.title("EmoWind!")

    x = root.winfo_x()
    y = root.winfo_y()
    emoWnd.minsize(500, 500)
    emoWnd.geometry("+%d+%d" % (x + 400, y + 200))

    rel = "\\test.jpg"
    rel = str(os.getcwd()) + rel
    print(rel)
    img = Image.open(rel)
    img = img.resize((400, 400), Image.ANTIALIAS)
    img1 = ImageTk.PhotoImage(img)

    wndImage = Label(emoWnd, image = img1)
    wndImage.img = img1


    wndLabel = Label(emoWnd, text = "You are " + emotion, font = 'Helvetica 32 bold')

    wndBtn = Button(emoWnd, text = "Ok", command = lambda: emoWnd.destroy())

    wndLabel.pack()
    wndImage.pack()
    wndBtn.pack()

    #Ipapasa niya yung emotion sa cP function para makapagDISPLAY
    tv.delete(*tv.get_children())  #para madelete yung nakadisplay na playlist
    createPlaylist(emotion)

#Function para palitan yung text ng isang label
def changeLabel(lbl, txt):
    lbl['text'] = txt

#Function para mag previous song
def prevSong():
    songStack.subIteration()
    if(nextButton['state'] == DISABLED):
        nextButton['state'] = NORMAL
    if(songStack.getIteration() == 0):
        previousButton['state'] = DISABLED
    putFocus()
    tempArr = songStack.getCurrentItems()
    player.previous()
    cancelAll()
    progressBarFunc(getInterval(tempArr[1]))


#Function para sa next button
def nextSong():
    songStack.addIteration()
    if(previousButton['state'] == DISABLED):
        previousButton['state'] = NORMAL
    if(songStack.getIteration() + 1 == songStack.length()):
        nextButton['state'] = DISABLED
    putFocus()
    tempArr = songStack.getCurrentItems()
    player.next()
    cancelAll()
    progressBarFunc(getInterval(tempArr[1]))


# Function pag pinindot yung play button.
def playSong(song):

    #If may pinapatugtog na yung player and pinindot yung stop button, dito siya pupunta sa if statement na to para mastop
    if(hehe.getFlag() == True):
        global songData
        playButton.configure(image=playImage)
        playButton.image = playImage
        player.stop()
        previousButton['state'] = DISABLED
        nextButton['state'] = DISABLED
        hehe.setFlag(False)
        songData = getData()
        player.__init__()
        songStack.__init__()
        cancelAll()
        return

    #If wala pang pinapatugtog yung player, dito siya
    playButton.configure(image=stopImage)
    playButton.image = stopImage
    nextButton['state'] = NORMAL
    hehe.setFlag(True)
    temp = tv.item(song, 'values')
    timeArr = temp[2].split(':')
    timeArr = int(int(timeArr[0])*60) + int(timeArr[1])
    progressBarFunc(int(timeArr*.01*1000))

    #player = playlist na tunay talaga
    #songstack = focus (highlight ng title na nagpeplay) and progress bar

    #temp = array of values. 0 = title, 1 artist, 2 duration, 3 bpm
    player.add(songDir[temp[0]]) #idadagdag yung song directory ng <title> sa playlist
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

#Eto version ko ng playsong function

def playSongEmotion(song):
    #stop button pressed
    if(hehe.getFlag() == True):
        global songEmoData
        playButton.configure(image=playImage)
        playButton.image = playImage
        previousButton['state'] = DISABLED
        nextButton['state'] = DISABLED
        player.stop()
        hehe.setFlag(False)
        songData = getSpecific()
        songStack.goBack()
        putFocus()
        cancelAll()
        return

    #If wala pang pinapatugtog yung player, dito siya
    playButton.configure(image=stopImage)
    playButton.image = stopImage
    nextButton['state'] = NORMAL
    hehe.setFlag(True)
    temp = tv.item(song, 'values')
    timeArr = temp[2].split(':')
    timeArr = int(int(timeArr[0])*60) + int(timeArr[1])
    progressBarFunc(int(timeArr*.01*1000))
    tempArr = songStack.getCurrentItems()
    for child in tv.get_children():
        if(tempArr[0] in tv.item(child)['values']):
            tv.focus(child)
            tv.selection_set(child)
            break

    #player = playlist na tunay talaga
    #songstack = focus (highlight ng title na nagpeplay) and progress bar

    #temp = array of values. 0 = title, 1 artist, 2 duration, 3 bpm
    player.play()
    return

#Function para makuha yung interval kung ilang seconds bago madagdagan yung progress bar
def getInterval(duration):
    return int(duration*.01*1000)


#Function para mastop yung progress bar pag pinindot ni user yung stop button
def cancelAll():
    arr = hehe.getId()
    for x in arr:
        root.after_cancel(x)

#Function para maupdate yung progress bar
def progressBarFunc(time, x = 0):
    if(x+1) < 100:
        temp = PhotoImage(file = "./res/progBars/"+ str(x) +"-progBar.png")
        progressBar.configure(image=temp)
        progressBar.image = temp
        root.after_id = root.after(time, lambda: progressBarFunc(time, x+1))
        hehe.add(root.after_id)
    else:
        if(songStack.getIteration() + 1 == songStack.length()):
            playSongEmotion()
            return
        temp = PhotoImage(file = "./res/progBars/0-progBar.png")
        progressBar.configure(image=temp)
        progressBar.image = temp
        nextSong()

#Initialize ng variable
#Yung hehe wag mo pansinin yan HAHAHAHA HINDI KO DIN ALAM PANO GUMAGANA YAN
hehe = cancelId()

#eto yung vlc player. bale gumawa siya ng object ng vlc. Check mo yung playlist.py para sa methods saka functions niya.
player = VLC()

#Eto is stack lang siya xd. Wala kasing stack sa python kaya gumawa lang ako. Same lang sa java, check mo din yung stack.py para sa methods.
songStack = stack()
songDir = {}


#Initialize ng tkinter
root = Tk()
root.geometry("1000x650")
root.title("MoodSic")
fnt = font.Font(size = 12)


#Initialize ng mga subwindow sa loob ng tkinter. Yung w yung para sa song list, yung control panel yung mga buttons.
w = PanedWindow(root)
controlPanel = PanedWindow(root)

#tv yung listahan ng kanta na nasa gui
tv = ttk.Treeview(w, height = 25, selectmode = "browse")

#Scollbar para sa treeview
scrollBar = ttk.Scrollbar(root, orient ="vertical", command = tv.yview)
scrollBar.pack(side = 'right', fill = 'y')
tv.configure(yscrollcommand = scrollBar.set)

#Initialize lang ng label and buttons.
lbl = Label(root, text = "My Music", font = 'Helvetica 18 bold')
detectEmotion = Button(root, text = "DETECT EMOTION", font = 'Arial 11 bold', background = "#AED5C0", command = countdown)

#Initialize ng mga images para sa buttons and progressbars.
playImage = PhotoImage(file = "./res/playButton.png")
nextImage = PhotoImage(file = "./res/nextButton.png")
prevImage = PhotoImage(file = "./res/prevButton.png")
stopImage = PhotoImage(file = "./res/stopButton.png")
progBar = PhotoImage(file = "./res/progBars/0-progBar.png")
progressBar = Label(root, image = progBar, borderwidth=0)


#Initialize ng mga buttons.
playButton = Button(controlPanel, image = playImage, font = fnt, command = lambda: playSong(tv.focus()))
nextButton = Button(controlPanel, image = nextImage, font = fnt, command = lambda: nextSong(), state = DISABLED)
previousButton = Button(controlPanel, image = prevImage, font = fnt, command = lambda: prevSong(), state = DISABLED)

#Placement ng buttons sa controlpanel.
previousButton.grid(row = 0, column = 0)
playButton.grid(row = 0, column = 1, padx = 30)
nextButton.grid(row = 0, column = 2)


#placements ng mga widgets
lbl.place(x = 170, y = 0)
w.place(x = 170, y = 40)
progressBar.place(x = 315, y = 615)
detectEmotion.place(x = 12, y = 490)
controlPanel.place(x = 465, y = 573)


#Andito yung songdata na nakuha sa main.py
songData = getData()
songEmoData = getSpecific()


#Tree view lang ito
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

#call every new instance ng app para makapagdisplay ng playlist.
addToStack(songData);


#
#      tv.pack(fill = "x")
tv.pack(fill = "x")

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
