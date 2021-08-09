from objects import thing
from assets import resources

class SpeedBoost(thing.Thing):

    def __init__(self,**kwargs):

        super().__init__(name='speedboost',**kwargs)

    def collisionAction(self,thing2):

        if thing2.name == 'player':

            thing2.speed = 300
            self.destroy()

        elif thing2.name == 'ai':

            thing2.dmgRate = 2*thing2.dmgRate
            thing2.speed = 2*thing2.speed
            thing2.sprite = resources.loadSprite(thing2,name='bot2')
            self.destroy()
