import pyglet
from assets import resources

class HUD: #this object is in charge of the HUD on the bottom of the screen

    def __init__(self,batch=None,group=None):

        self.batch, self.group = batch, group

        self.debug = resources.DEBUG

        self.sprites = []

        #this dictionary stores all the different labels
        self.textDict = {}

        self.fontName = 'Times New Roman'
        self.fontSize = 18

        self.W = 11.5
        self.H = 6

        self.x = self.oldx = resources.ZEROX + self.W
        self.y = self.oldy = resources.ZEROY - 6*self.H

        if resources.DEBUG:
            self.x += 100
            self.oldx += 100

    def drawImg(self,imgname,scale=1,angle=0,shiftY=True): #a shorthand to reduce typing considerably
        
        img = resources.loadImg(imgname)

        sprite = pyglet.sprite.Sprite(img=img,x=self.x,y=self.y,batch=self.batch,group=self.group)
        sprite.scale = scale
        sprite.rotation = angle
        self.sprites += [sprite]

        if shiftY:
            self.y -= img.height * scale

    def writeText(self,heading,text):

        try:
            self.textDict[heading].text = heading + ' {}'.format(text)
        except:
            self.textDict[heading] = pyglet.text.Label(heading + ' {}'.format(text),font_size = self.fontSize, font_name=self.fontName, x=self.x, y=self.y, batch=self.batch,group=self.group)
        finally:
            self.y -= self.fontSize

    def update(self,health,points,ammo,ragemode,pause): #modify this function as required for custom behaviour
        
        #reset position coordinates to default values
        
        self.x = self.oldx
        self.y = self.oldy

        #this deletes the sprites present to 'clear' the HUD
        
        for i in self.sprites:
            self.sprites.remove(i)
        
        #code to display a health bar, points etc

        healthPicNo = 20
        while healthPicNo < health:
            healthPicNo += 20

        #this code writes all the relavent data

        #ragemode
        if ragemode:
            self.x += 200
            self.y -= 25
            self.drawImg('ragehud',shiftY=False)
            self.x -= 200
            self.y += 25

        #health
        filename = 'health.{}'.format(healthPicNo)
        self.drawImg(filename)

        #ammo
        if not ammo:
            ammo = 'NO AMMO'
        self.writeText('Ammo:',ammo)
        self.writeText('Points:',points)

        #pause
        if pause:
            self.x += 500
            self.y += self.fontSize
            self.writeText('Paused','')
        else:
            try:
                self.textDict['Paused'].delete()
                del self.textDict['Paused']
            except:
                pass
