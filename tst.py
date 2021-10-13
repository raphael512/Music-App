from tkinter import *

root = Tk()
root.geometry("800x800")
def changeThis():
    temp = PhotoImage(file="./res/progBars/50-progBar.png")
    txt.configure(image=temp)
    txt.image = temp

img = PhotoImage(file="./res/progBars/0-progBar.png")

txt = Label(root, image=img)
txt.grid(row=0, column=0, pady=100)

btn = Button(root, text = "Click me!", command=changeThis)
btn.grid(row=1, column=0)


root.mainloop()