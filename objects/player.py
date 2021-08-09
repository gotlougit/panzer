from objects import thing, projectile
import pyglet, math
from assets import resources
from pyglet.window import key

class Player(thing.Thing): #the all important player class

    def __init__(self,**kwargs):

        self.speed = kwargs.get('speed',200)
        self.rspeed = self.speed
        self.points = 0
        self.rageModeMeter = 0
        self.timer = 0

        super().__init__(name='player',**kwargs)
        
        self.key_handler = key.KeyStateHandler()
       
        self.nozzle = resources.loadSprite(self,name='nozzle')
        
        self.angle = -90
        
        self.health = kwargs.get('health',120)
        self.projectiles = []
        self.direction = 'up'
        self.olddirection = self.direction

        self.ammo = 10
        self.maxammo = 20

        self.unlimAmmo = False

    def collisionAction(self,thing2): #slightly modified so that bots die when colliding with player
    
        if thing2.name != 'ai':
            super().collisionAction(thing2)
        else:
            thing2.dead = True
            self.points += 3
            self.rageModeMeter += 3

    def draw(self): #draws the projectiles, nozzle and tank

        super().draw()

        self.nozzle.x = self.x
        self.nozzle.y = self.y

        self.nozzle.draw()

        if len(self.projectiles) != 0:

            for i in self.projectiles:
                if not i.dead:
                    i.draw()

    def checkAmmo(self):

        if self.ammo > self.maxammo and not self.unlimAmmo:
            self.ammo = self.maxammo
            if self.debug:
                print('ammo is at max!')

    def sync(self,raw=False): #this method changes angle of nozzle with the change in direction of tank

        d = {
        'left':1,
        'up':2,
        'right':3,
        'down':4
                }
        
        if not raw:
            n = d[self.direction] - d[self.olddirection]
        else:
            n = d[self.direction]
        return n*90

    def update(self,dt): #huge function which deals with keyboard input and also changes the position, rotation etc.

        self.checkAmmo()

        self.oldx, self.oldy = self.x,self.y
    
        self.timer += dt

        if resources.DEBUG:
            print('player projectiles: {}'.format(self.projectiles))

        if self.key_handler[key.W]: #up
            self.y += self.speed * dt
            self.direction = 'up'

        elif self.key_handler[key.S]: #down 
            self.y -= self.speed * dt
            self.direction = 'down'
        
        elif self.key_handler[key.A]: #left
            self.x -= self.speed * dt
            self.direction = 'left'
        
        elif self.key_handler[key.D]: #right
            self.x += self.speed * dt
            self.direction = 'right'

        if self.key_handler[key.Q]: #left rotate
            self.angle -= self.rspeed * dt
        
        elif self.key_handler[key.E]: #right rotate
            self.angle += self.rspeed * dt

        if self.key_handler[key.SPACE] and self.timer > 0.1: #fire projectile

            if self.ammo > 0:
                oname = 'Gunfire'
                o = resources.loadMusic(oname)
                o.play()
                self.timer = 0
            
                theta = math.radians(-1 * self.angle)
                if self.debug:
                    print('theta {}'.format(theta))
                
                x = (self.sprite.width) * math.cos(theta)
                y = (self.sprite.height) * math.sin(theta)
                
                if not self.unlimAmmo:
                    self.ammo -= 1

                p = (projectile.Projectile(angle=theta, x=self.x + x, y=self.y + y))
                if self.unlimAmmo:
                    p.speed = 800
                self.projectiles.append(p)

        self.angle += self.sync()
        self.olddirection = self.direction
        self.sprite.rotation = self.sync(raw=True)
        self.nozzle.rotation = self.angle

        if len(self.projectiles) != 0:
            
            for i in self.projectiles:
                i.update(dt)

        if self.debug:
            print('player points: {}'.format(self.points))
            print('player rageModeMeter: {}'.format(self.rageModeMeter))

        self.checkPos()
