from Tkinter import *
import random
import time

tk = Tk()

Height = 500
Width = 500

canvas = Canvas(tk, width = Width, height = Height)
tk.title("Graphics")
canvas.pack()

ball =canvas.create_oval(75,75,100,100,fill="red")
xspeed = 10
yspeed = 10

while True:
	canvas.move(ball, xspeed, yspeed)
	pos = canvas.coords(ball) # [left, top, right,bottom]
	
	if pos[2]>=Width or pos[0] <= 0:
		xspeed = -xspeed
	if pos[3] >= Height or pos[1] <=0:
		yspeed = - yspeed
	
	tk.update()
	time.sleep(0.1)