import mysql.connector as con
from tkinter import *
from assets import db
import design

def Score(score,mycon):
    
    windowsc = Tk()
    windowsc.title("Score")
    windowsc.configure(bg = design.bg)
    
    Label(windowsc, text='GAME OVER', font=(design.font, 25), bg=design.fg, fg=design.bg).grid(column=0,row=0)
    lb = Label(windowsc, text="Your Score is {}".format(score), font=(design.font,20),bg=design.bg, fg=design.fg)
    lb.grid(column=0,row = 1)

    lb2 = Label(windowsc, text="Enter Name:", font=(design.font,20),bg=design.bg, fg=design.fg)
    lb2.grid(column=0,row = 2)

    outputuser = StringVar()
    txtsc = Entry(windowsc,width=20,textvariable=outputuser)
    txtsc.grid(column=2,row=2)

    def clicked():

        db.createtable(mycon)
        db.addscore(mycon,outputuser.get(),score)
        windowsc.destroy()

    def Quit():
        print('quitting...')
        quit()

    btn= Button(windowsc, text="Save", bg=design.bg, fg=design.fg, command=clicked)
    btn.grid(column=1,row=4)
    
    Button(windowsc, text='Quit', bg=design.bg,fg=design.fg,command=Quit).grid(column=2,row=4)

    windowsc.mainloop()

def showHighScores(window, mycon):

    data = db.getHighScores(mycon)
    Label(window, text='High Scores', font=(design.font,25), bg=design.fg, fg=design.bg).grid()
    for x,y in data:
        index = data.index((x,y)) + 1
        Label(window, text=f'{index}. {x} \t {y}', font=(design.font,20), bg=design.bg, fg=design.fg).grid()
