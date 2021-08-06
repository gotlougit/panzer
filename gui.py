from tkinter import *
import design

def destroyFrameWindow(frame):

    for widget in frame.winfo_children():
        widget.destroy()

def getInputWindow(window, headings, func):

    Label(window, text=headings[0], font=(design.font,50),bg=design.bg, fg=design.tc1).grid(column=0,row=0)

    n = len(headings)
    
    outputs = []

    for i in range(1,n):
        
        outputs+=[StringVar()]

    for i in range(1,n):
        
        Label(window, text=headings[i] + ':', font = (design.font,20), bg = design.bg, fg=design.fg).grid(column=0, row = 1+i)
        
        if 'password' not in headings[i].lower():
            Entry(window, textvariable=outputs[i-1], width=20).grid(column=1, row=1+i)
        
        else:
            Entry(window, textvariable=outputs[i-1], width=20,show='*').grid(column=1, row=1+i)
    
    def execute():
        func(outputs)

    b = Button(window, text='Login', font=(design.font, 14), bg = design.bg, fg= design.fg, command= execute)
    b.grid(column=1, row= n+1)

def button_creator(window, labels, functions,s=0):
    
    for i in range(len(labels)):
        
        Button(window, text=labels[i], font = (design.font, 20), bg = design.fg , fg = design.bg, command = functions[i]).grid()
