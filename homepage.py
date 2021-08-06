import mysql.connector as con
from tkinter import *
from PIL import ImageTk, Image
import design
import gui
import gamewindow
import score
from assets import resources, db

window = Tk()
window.title(design.title)
window.configure(bg=design.bg)

frame = Frame(window)
frame.configure(bg=design.bg)
frame.grid(column=0, row=0)

headings = ['Login', 'MySQL Username', 'MySQL Password']

def backButton(outputs):
    def backFunc():
        makeLoginWindow(outputs)

    Button(frame,
           text='<-- Back',
           font=(design.font, 14),
           fg=design.bg,
           bg=design.fg,
           command=backFunc).grid()

def poster(outputs):

    gui.destroyFrameWindow(frame)
    imgPath = resources.getPath('panzerposter.png')
    global img
    img = ImageTk.PhotoImage(Image.open(imgPath))
    panel = Label(frame, image=img)
    panel.grid()

    def continueFunc():
        makeLoginWindow(outputs)

    Button(frame, text='Continue',font=(design.font,14), fg=design.bg, bg=design.fg, command =continueFunc).grid()

def chooseTank(mycon, outputs):

    gui.destroyFrameWindow(frame)

    labels = ['Modern', 'Classic']

    def modern():
        chooseMap(mycon, outputs, 'player')

    def classic():
        chooseMap(mycon, outputs, 'player1')

    functions = [modern, classic]

    Label(frame,
          text='Choose tank style:',
          font=(design.font, 20),
          bg=design.bg,
          fg=design.fg).grid()
    gui.button_creator(frame, labels, functions, s=1)

    backButton(outputs)


def chooseMap(mycon, outputs, playersprite):

    gui.destroyFrameWindow(frame)

    labels = ['Snow', 'Desert', 'Jungle']

    def snow():
        startNewGame('snowmap', mycon, playersprite)

    def desert():
        startNewGame('desertmap', mycon, playersprite)

    def jungle():
        startNewGame('junglemap', mycon, playersprite)

    functions = [snow, desert, jungle]

    Label(frame,
          text='Choose the map:',
          font=(design.font, 20),
          bg=design.bg,
          fg=design.fg).grid()
    gui.button_creator(frame, labels, functions, s=1)

    backButton(outputs)


def tutorial(outputs):

    gui.destroyFrameWindow(frame)
    imgPath = resources.getPath('howtoplay.png')
    global img
    img = ImageTk.PhotoImage(Image.open(imgPath))
    panel = Label(frame, image=img)
    panel.grid()

    backButton(outputs)


def startNewGame(mapchoice, mycon, playersprite):

    window.destroy()

    gamewin = gamewindow.GameWindow(mapchoice, mycon, playersprite)
    gamewin.runGame()


def Quit():

    window.destroy()
    print('Quitting...')
    quit()


def showScores(mycon, outputs):

    gui.destroyFrameWindow(frame)
    score.showHighScores(frame, mycon)

    backButton(outputs)


def makeLoginWindow(outputs):

    mycon = db.signup(outputs[0].get(), outputs[1].get(), 'panzerdb')

    if mycon.is_connected():

        gui.destroyFrameWindow(frame)

        Label(frame,
              text='{} version {}'.format(resources.TITLE, resources.VERSION),
              font=(design.font, 20),
              bg=design.bg,
              fg=design.fg).grid(column=0, row=1)
        Label(frame,
              text=' The mission is to save the base from the AI Bots. ',
              font=16,
              bg=design.bg,
              fg='grey').grid(column=0, row=2)
        Label(frame,
              text=' Destroy them by either colliding or shooting. ',
              font=16,
              bg=design.bg,
              fg='grey').grid(column=0, row=3)

        def score():
            showScores(mycon, outputs)

        def mapselector():
            chooseTank(mycon, outputs)

        def tut():
            tutorial(outputs)

        functions = [mapselector, score, tut, Quit]
        headings = ['New Game', 'Scores', 'View Controls', 'Quit']

        gui.button_creator(frame, headings, functions, s=2)

gui.getInputWindow(frame, headings, poster)
window.mainloop()
