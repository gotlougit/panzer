from objects import thing
from assets import resources

class AmmoBox(thing.Thing):
    
    def __init__(self,**kwargs):

        super().__init__(name='ammobox',**kwargs)

    def collisionAction(self,thing2):

        if thing2.name == 'player':

            thing2.ammo += 5
            if self.debug:
                print('ammo gained from ammobox by player')
            resources.playMusic('ammobox')
            self.destroy()

        elif thing2.name == 'ai':

            thing2.speed = 2*thing2.speed
            thing2.oldspeed = 2*thing2.oldspeed
            thing2.sprite = resources.loadSprite(thing2, name='bot2')
            resources.playMusic('bot2spawn')
            if self.debug:
                print('projectile transformed!')
            self.destroy()
