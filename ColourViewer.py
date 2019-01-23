#!/usr/bin/python
#Colour visualiser
#Dependant on python2.7 and Tkinter to run
import sys
from Tkinter import *
if len(sys.argv)>2: print("Warning: expected only 1 argument. Others will be ignored")
if len(sys.argv)<2: 
	print("Usage:\nColourViewer.py col1,col2,...\nwhere col[n] are colours given by 3 or 6 place hexdecimal (with or without '#'), separated by a comma, no spaces\n\nExit\n\n")
	quit()
rt=Tk()
i=0
Laz=[]
for col in sys.argv[1].split(','):
	if col[0]!='#': col='#%s'%col
	Laz.append(Label(rt,text=col,bg=col))
	Laz[-1].grid(column=i//20,row=i%20,sticky='nesw')
	i+=1
def exit(*dmp): quit()
rt.bind('<Button-1>', exit)
cols=sys.argv[1].split(',')
while cols:
	cols=raw_input("New set of colours: ")
	for item in Laz: item.grid_forget()
	Laz=[]
	i=0
	for col in cols.split(','):
		if col[0]!='#': col='#%s'%col
		Laz.append(Label(rt,text=col,bg=col))
		Laz[-1].grid(column=i//20,row=i%20,sticky='nesw')
		i+=1
rt.mainloop()