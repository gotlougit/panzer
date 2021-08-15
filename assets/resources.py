#a script dealing with all resources
import pyglet
pyglet.resource.path = ['assets/maps','assets/audio','assets/sprites'] #RELATIVE TO ROOT DIRECTORY OF PROJECT
pyglet.resource.reindex()

#declare the constants for the game
VERSION = '1.1.2'
HEIGHT = 720
WIDTH = 1000
DEBUG = False
FRAMERATE = 120
TITLE = 'Project Panzer'
ZEROX = 0
ZEROY = 90

def loadMusic(name):
    
    return pyglet.resource.media(name+'.wav',streaming=False)

def playMusic(name): #only use this to play music one time

    m = loadMusic(name)
    m.play()

def getPath(name): #gets the location of a specific resource

    loader = pyglet.resource.Loader(path=pyglet.resource.path)
    pyglet.resource.reindex()
    from os import path
    return path.join(loader.location(name).path,name)

def loadImg(name):
    
    img = pyglet.resource.image(name+'.png')
    return img

def loadMap(name,batch,group):
    
    img = loadImg(name)
    return pyglet.sprite.Sprite(img=img,x=ZEROX,y=ZEROY,batch=batch,group=group)

def loadSprite(thing,name=False):

    if not name:
        name = thing.name
    
    img = loadImg(name)
    img.anchor_x = img.width//2
    img.anchor_y = img.height//2

    try:
        sprite = pyglet.sprite.Sprite(img=img,x=thing.x,y=thing.y,batch=thing.batch,group=thing.group)
    except AttributeError:
        sprite = pyglet.sprite.Sprite(img=img, x=thing.x, y=thing.y)
    finally:
        return sprite
