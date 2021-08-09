from objects import thing

class Base(thing.Thing): #a slightly modified version of the Thing class

    def __init__(self,**kwargs):
        
        super().__init__(name='base',**kwargs)
        self.health = kwargs.get('health',100)
    
    def collisionAction(self, thing2):

        super().collisionAction(thing2)

        if thing2.name == 'ai' and self.debug:

            print('ai is colliding!!!')
