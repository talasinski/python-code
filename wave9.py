#!/usr/bin/env python3
from Tkinter import *
from math import *
import tkSimpleDialog, tkMessageBox
import os, sys
	
def setGrid():
	global nbin, stepIt
	if stepIt:
		runPause()
	mD = tkSimpleDialog.askinteger('Grid size', 'number of bins:',\
						initialvalue=nbin, minvalue=30, maxvalue=500)
	if  mD != None:
		nbin = mD
		initWave()
	else:
		runPause()
	
def initWave():
	global stepIt, count, nbin, nbin1
	global x, y, u1, u2, u3
	global xmin, xmax, ymin, ymax, xoff, yoff
	global winDelx, winDely
	global labelOff
	xmin = 0.0; xmax = 1.0; ymin = -1.0; ymax = 1.0
	xoff = 30; yoff = 35; labelOff = 15
	stepIt =0
	count = 0
	nbin1 = nbin+1
	delx = 1.0/nbin
	waveStart = nbin/5
	waveEnd = 3*nbin/5
	x = [0.0]*nbin1; y = [0.0]*nbin1
	u1= [0.0]*nbin1; u2= [0.0]*nbin1; u3= [0.0]*nbin1	
	for i in range(nbin1):
		x[i] = i*delx
		y[i] =0.0
		if (i>=waveStart) and (i<=waveEnd):
			y[i] = sin(5*pi*(i-waveStart)*delx)
		u1[i]=y[i]
	u2[0]=0.0
	u3[0] = 0.0
	for i in range(1, nbin):
		u2[i] = 0.5*(y[i+1]+y[i-1])	
	u2[nbin]=y[nbin-1]
	for i in range(nbin):
		u3[i] = u2[i]
	u3[nbin]=0.0
	setTransform()
	plotWave()

def setTransform():
	global a, b, c, d
	delx = winDelx  - 2*xoff     #must recompute if user changes window size.
	dely = winDely - 2*yoff
	a = delx/( xmax - xmin)
	b = -a * xmin + xoff
	c = dely/(ymin -  ymax)
	d = -c * ymax + yoff
	
def plotWave():
	x0 = a * xmin + b
	x1 = a * xmax + b
	y0 = c * ymin + d
	y1 = c * ymax + d
	canvas.delete('lines')   #clear the screen. Everthing drawn is taged 'lines'
	canvas.create_line(x0,y0,x1,y0, width=1, tag='lines')
	canvas.create_line(b,y0,b,y1,  width=1, tag='lines')
	canvas.create_text(x1-labelOff, y1-labelOff, text='Step:%d'% count, tag='lines', font='Verdana 8 bold')
	canvas.create_text(x0-labelOff, y1, text='%4.1f'% 1.0, tag='lines', font='Verdana 8 bold')
	canvas.create_text(x0-labelOff, y0, text='%4.1f'% -1.0, tag='lines', font='Verdana 8 bold')
	canvas.create_text(x0, y0+labelOff, text='%4.1f'%  0.0, tag='lines', font='Verdana 8 bold')
	canvas.create_text(x1, y0+labelOff, text='%4.1f'%  1.0, tag='lines', font='Verdana 8 bold')
	x0 = a*x[0] +b
	y0 = c* u3[0] +d
	for i in range(1,nbin1):
		x1 = a*x[i] + b
		y1 = c* u3[i] + d
		canvas.create_line(x0,y0,x1,y1,tag='lines')
		x0 = x1
		y0 = y1
	canvas.update()	#Seem to need this statement on Sun.
def stepWave():
	global count, nbin
	for i in range(1,nbin):
		u3[i] = u2[i-1]+u2[i+1] - u1[i]
	u3[nbin] = 2.0*u2[nbin-1] - u1[nbin]
	for i in range(1,nbin1):
		u1[i]=u2[i]
		u2[i]=u3[i]		
	plotWave()
	if stepIt:
		canvas.after(1, stepWave)            #The animation trick in Tk.
		count = count + 1

def runPause():
	global stepIt
	if  stepIt:
		filemenu.entryconfig(0, label='Run  ') #Update menu on the fly. Index=0.
	else:
		filemenu.entryconfig(0, label='Pause')
	stepIt = not stepIt
	stepWave()

def onResize(event):
	global winDelx, winDely
	winDelx =event.width
	winDely =event.height
	setTransform()
	plotWave()

def printIt():
	ps = canvas.postscript()
	if (sys.platform == 'win32') :
		PS = open("prn:", 'w')        #Is there an equivalent under unix?
	else:
		PS = open("wavePlots",'w')
	PS.write(ps)
	PS.close()
	

def tellAbout():
	tkinter.messagebox.showinfo('Wave by Lasinski', \
						  ' Simple explicit algorithm\n version 0.9')


root = Tk()
root.title('Wave ')

winDelx = 300; winDely = 300
canvas = Canvas(root, width=winDelx, height=winDely, bg = 'white')
canvas.pack(expand=YES, fill=BOTH)
canvas.bind("<Configure>", onResize)  # Update screen if user resizes.

menubar = Menu(root)            # create a toplevel menu

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Run", command=runPause)  #This is index=0.
filemenu.add_command(label="Grid", command=setGrid)
filemenu.add_command(label="Print", command=printIt)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Control", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About wave",command=tellAbout)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)         # display the menu

nbin=100    # Set nbin here so user can set nbin during run and call initWave.
initWave()

root.mainloop()
