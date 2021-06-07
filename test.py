from tkinter import *
from tkinter import ttk
import pickle

with open("song_data.py", "rb") as fp:
    temp = pickle.load(fp)

ws = Tk()
ws.title('PythonGuides')
ws.geometry('400x300')
ws['bg']='#fb0'

tv = ttk.Treeview(ws)
tv['columns']=('Title', 'Artist', 'Duration', 'Tempo')
tv.column('#0', width=0, stretch=NO)
tv.column('Title', anchor=CENTER, width=160)
tv.column('Artist', anchor=CENTER, width=80)
tv.column('Duration', anchor=CENTER, width=80)
tv.column('Tempo', anchor=CENTER, width=80)

tv.heading('#0', text='', anchor=CENTER)
tv.heading('Title', text='Title', anchor=CENTER)
tv.heading('Artist', text='Artist', anchor=CENTER)
tv.heading('Duration', text='Duration', anchor=CENTER)
tv.heading('Tempo', text='Tempo', anchor=CENTER)

for x in range(len(temp)):    
    tv.insert(parent='', index=x, iid=x, text='', values=(temp[x][3],'Mama mo', str(int(temp[x][2]/60)) + ':' + str(int(temp[x][2])%60), int(temp[x][1])))

tv.pack()


ws.mainloop()