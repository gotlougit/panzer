from objects import thing
from assets import resources
import random

class AI(thing.Thing): #this class creates an AI character

    def __init__(self,**kwargs):
        
        super().__init__(name='ai',**kwargs)
        self.speed = 50
        self.oldspeed = self.speed
        self.health = 100
        self.lim = 64
        self.dmgRate = 1/20
        self.oldDmgRate = self.dmgRate

    def attractThing(self,thing2):

        sx, sy = 0, 0


        conditionX = not 0 < abs(self.x - thing2.x) < self.lim
        conditionY = not 0 < abs(self.y - thing2.y) < self.lim

        if conditionX:
            if self.x > thing2.x:
                sx =-1
            elif self.x < thing2.x:
                sx = 1
        if conditionY:
            if self.y > thing2.y:
                sy = -1
            elif self.y < thing2.y:
                sy = 1

        if not conditionX and not conditionY:
            self.still = True
            self.defStill = True

        return sx,sy

    def collisionAction(self,thing2):

        super().collisionAction(thing2)

        if thing2.name == 'base':
            thing2.health -= self.dmgRate

        elif thing2.name == 'player':

            if random.randint(0,1) and not thing2.unlimAmmo:
                thing2.ammo += 1
                if self.debug:
                    print('Ammo randomly spawned from collision with enemy!')

    def update(self, thing2, dt):

        if self.health <= 0:
            self.dead = True

        self.oldx, self.oldy = self.x, self.y

        sx, sy = self.attractThing(thing2)

        self.x += sx * self.speed * dt
        self.y += sy * self.speed * dt

        self.checkPos()
        
        self.sprite.x = self.x
        self.sprite.y = self.y
        
        if self.debug:
            print('ai id: {} health: {} x: {}, y: {}'.format(id(self),self.health,self.x, self.y))
