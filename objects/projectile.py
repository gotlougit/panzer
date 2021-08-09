from objects import thing
import math

class Projectile(thing.Thing): #a modified version of Thing that is designed to go along a straight line

    def __init__(self,**kwargs):

        super().__init__(name='projectile',**kwargs)
        
        self.points = 0
        self.speed = 400
        self.angle = kwargs.get('angle',0)
        self.damage = 100
        self.sprite.rotation =  -1 * math.degrees(self.angle)

    def movingFunc(self,dt): #this function calculates the distance needed to be moved in both x and y using trigonometry

        dx = math.cos(self.angle) * self.speed * dt
        dy = math.sin(self.angle) * self.speed * dt

        if self.debug:
            print('angle of projectile (radians): {}'.format(self.angle))

        return dx, dy

    def destroy(self): #add more effects here when dead

        super().destroy()

    def update(self,dt):

        dx, dy = self.movingFunc(dt)

        self.x += dx
        self.y += dy

        self.checkPos(func=self.destroy)

    def collisionAction(self,thing2):

        if thing2.name == 'ai':
            
            thing2.health -= self.damage
            self.points += 3 #change this value to change how many points player gets from projectile kill
            
            if self.debug:
                print('points added to projectile!')
                print('projectile did damage {} to {}'.format(self.damage,thing2.name))

            self.destroy()
