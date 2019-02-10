#!/usr/local/bin/python
from Tkinter import *
from math import *
from random import Random
import tkSimpleDialog, tkMessageBox
import os, sys
class Dialog(Toplevel):

    def __init__(self, parent, title, nby, xss, yss):
        Toplevel.__init__(self, parent)
        global nbyn, xs, ys
        nbyn = nby
        xs = xss
        ys = yss
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        Label(master,  text='Mean and Sigma').pack()
        canHere = Canvas(master, width=300, height=200, bg = 'white')
        canHere.pack()
        hereGraph = Graphs(canHere, 0.0, 1.0, 0.0, 1.0)
        hereGraph.setTransform( 0.0, 1.0, 0.0, 1.0, 300, 200)
        hereGraph.plotWave(nbyn, xs, ys)

#        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        
        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("&lt;Return>", self.ok)
        self.bind("&lt;Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override
	
class Graphs:
    def __init__(self,canva, xmin, xman, ymin, yman):
        global xmi, xma, ymi, yma, canvas
        canvas = canva
        xmi = xmin
        xma = xman
        ymi = ymin
        yma = yman
    def setTransform(self, xmin, xmax, ymin, ymax, winDelx, winDely):
        global a, b, c, d
        xmi = xmin
        xma = xmax
        ymi = ymin
        yma = ymax
        wnDelx = winDelx
        wnDely = winDely
        xoff = 30; yoff = 35
        delx = wnDelx  - 2*xoff    #must recompute if user changes window size.
        dely = wnDely - 2*yoff
        a = delx/( xma - xmi)
        b = -a * xmi + xoff
        c = dely/(ymi -  yma)
        d = -c * yma + yoff
    def plotWave(self,nbyns, xplt, yplt):
        nbins = nbyns
        xpl = xplt
        ypl = yplt
        labelOff = 15
        x0 = a * xmi + b
        x1 = a * xma + b
        y0 = c * ymi + d
        y1 = c * yma + d
        canvas.delete('lines')   #clear the screen. Everthing drawn is taged 'lines'
        canvas.create_line(x0,y0,x1,y0, width=1, tag='lines')
        canvas.create_line(b,y0,b,y1,  width=1, tag='lines')
        canvas.create_text(x1-labelOff, y1-labelOff, text='Step:%d'% count, tag='lines', font='Verdana 8 bold')
        canvas.create_text(x0-labelOff, y1, text='%4.1f'% yma, tag='lines', font='Verdana 8 bold')
        canvas.create_text(x0-labelOff, y0, text='%4.1f'% ymi, tag='lines', font='Verdana 8 bold')
        canvas.create_text(x0, y0+labelOff, text='%4.1f'% xmi, tag='lines', font='Verdana 8 bold')
        canvas.create_text(x1, y0+labelOff, text='%4.1f'%  xma, tag='lines', font='Verdana 8 bold')
        x0 = a*xpl[0] +b
        y0 = c* ypl[0] +d
        for i in range(1,nbins):
            x1 = a*xpl[i] + b
            y1 = c*ypl[i] + d
            canvas.create_line(x0,y0,x1,y1,tag='lines')
            x0 = x1
            y0 = y1
#	canvas.update()	#Seem to need this statement on Sun.

def setGrid():
	global nbin, stepIt
	if stepIt:
		runPause()
	mD = tkSimpleDialog.askinteger('Grid size', 'number of bins:',\
						initialvalue=nbin, minvalue=30, maxvalue=500)
	if  mD <> None:
		nbin = mD
		initWave()
	else:
		runPause()
	
def initWave():
	global stepIt, count, nbin, nbin1, plotBin1,root_delx
	global x, y, u1, u2, u3
	global xmin, xmax, ymin, ymax, xoff, yoff
	global winDelx, winDely
	global labelOff
	global g,  canv, mainGraph


	xmin = 0.0; xmax = 1.0; ymin = -1.5; ymax = 1.5
	mainGraph = Graphs(canv, xmin,xmax,ymin,ymax)
	xoff = 30; yoff = 35; labelOff = 15
	stepIt =0
	count = 0
	nbin1 = nbin+1
	delx = 1.0/nbin
	root_delx= sqrt(delx)
	waveStart = nbin/5
	waveEnd = 3*nbin/5
	x = [0.0]*nbin1; y = [0.0]*nbin1
	u1= [0.0]*nbin1; u2= [0.0]*nbin1; u3= [0.0]*nbin1	
	g = Random()
	for i in range(nbin1):
		u1[i] = g.gauss(0,1)
	delBin = 0.2
	plotBin =(xmax - xmin )/ delBin
	for i in range(nbin):
		x[i] = delx*i
	plotBin1 = plotBin - 1
	run = 0.0
	for j in range(nbin) :
		run = run + root_delx * g.gauss(0,1)
		u3[j] = run
		u1[j] = u1[j] + run
		u2[j] = u2[j] + run * run
	mainGraph.setTransform(xmin, xmax, ymin, ymax, winDelx, winDely)
	mainGraph.plotWave(nbin, x, u3)


def stepWave():
    global count, nbin
    if stepIt:
        run = 0.0
        for j in range(nbin) :
            run = run + root_delx * g.gauss(0,1)
            u3[j] = run
            u1[j] = u1[j] + run
            u2[j] = u2[j] + run * run

        mainGraph.plotWave(nbin, x, u3)
        canv.after(100, stepWave)            #The animation trick in Tk.
        count = count + 1

def showSigma():
    global ymin, ymax, stepIt
    runPause()
#    stepIt = 0
    ymin =0.
    ymax = 1.0
    for i  in range(nbin) :
        u2[i] = u2[i]/count
#    setTransform()
#    plotWave(nbin, x, u2)
    newWin = Dialog(root,"Mean & Sigma", nbin, x, u2)
#    stepIt = 1
    ymin = -1.5
    ymax = 1.5
    for i  in range(nbin) :
        u2[i] = u2[i]*count
    runPause()
#import sys; sys.exit()
	
def runPause():
	global ymin, ymax, stepIt
	if  stepIt:
		filemenu.entryconfig(0, label='Run  ') #Update menu on the fly. Index=0.
	else:
		filemenu.entryconfig(0, label='Pause')
	stepIt = not stepIt
	mainGraph.setTransform(xmin, xmax, ymin, ymax, winDelx, winDely)
	stepWave()

def onResize(event):
	global winDelx, winDely
	winDelx =event.width
	winDely =event.height
	mainGraph.setTransform(xmin, xmax, ymin, ymax, winDelx, winDely)
	mainGraph.plotWave(nbin, x, u3)

def printIt():
	ps = canvas.postscript()
	if (sys.platform == 'win32') :
		PS = open("prn:", 'w')        #Is there an equivalent under unix?
	else:
		PS = open("wavePlots",'w')
	PS.write(ps)
	PS.close()
	

def tellAbout():
	tkMessageBox.showinfo('Wave by Lasinski', \
						  ' Simple explicit algorithm\n version 0.9')


root = Tk()
root.title('Wave ')


menubar = Menu(root)            # create a toplevel menu
winDelx = 300; winDely = 300
canv = Canvas(root, width=winDelx, height=winDely, bg = 'white')
canv.pack(expand=YES, fill=BOTH)
canv.bind("<Configure>", onResize)  # Update screen if user resizes.


filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Run", command=runPause)  #This is index=0.
filemenu.add_command(label="Grid", command=setGrid)
filemenu.add_command(label="sigma", command=showSigma)
filemenu.add_command(label="Print", command=printIt)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Control", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About wave",command=tellAbout)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)         # display the menu

nbin=1000    # Set nbin here so user can set nbin during run and call initWave.
initWave()

root.mainloop()