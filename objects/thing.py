from assets import resources

class Thing: #the basic building block of the world

    def __init__(self,**kwargs): #this somewhat large __init__ method will take care of setting up many variables for us

        self.name = kwargs.get('name',False)
        self.x = kwargs.get('x',resources.ZEROX)
        self.y = kwargs.get('y',resources.ZEROY)
        self.oldx = self.x
        self.oldy = self.y
        self.batch = kwargs.get('batch',None)
        self.group = kwargs.get('group',None)
        self.dead = False
        self.debug = resources.DEBUG

        self.colX = self.colY = False #initally, nothing will collide; setup code takes care of this

        if self.name:
            self.sprite = resources.loadSprite(self)
        
    def draw(self):
        
        self.sprite.x = self.x
        self.sprite.y = self.y
        
        self.sprite.draw()

    def destroy(self):

        self.dead = True

    def collisionAction(self,thing2): #the statement that will be run when collision occurs; doing it this way we can modify it easily for many objects

        if not self.colX:
            thing2.x = thing2.oldx

        if not self.colY:
            thing2.y = thing2.oldy

    def collisionCheckX(self,thing2): #checks for the distance between two objects with respect to the sum of 1/2 their widths

        return ((self.sprite.width + thing2.sprite.width)/2 <= abs((self.x - thing2.x)))

    def collisionCheckY(self,thing2): #same as collisionCheckX() but for y axis
        
        return ((self.sprite.height + thing2.sprite.height)/2 <= abs((self.y - thing2.y)))

    def collisionCheck(self,thing2): #combine both of the functions and return an answer

        self.colX = self.collisionCheckX(thing2)
        self.colY = self.collisionCheckY(thing2)

        return not (self.colX or self.colY)

    def checkPos(self,func=False): #makes sure objects don't disappear off of the screen

        self.x = round(self.x)
        self.y = round(self.y)

        minx, miny = self.sprite.width/2 + resources.ZEROX, self.sprite.height/2 + resources.ZEROY

        maxx = resources.WIDTH - self.sprite.width/2
        maxy = resources.HEIGHT - self.sprite.height/2

        flag = False

        if self.x < minx:
            self.x = minx
            flag = True
        elif self.x > maxx:
            self.x = maxx
            flag = True
        if self.y < miny:
            self.y = miny
            flag = True
        elif self.y > maxy:
            self.y = maxy
            flag = True
    
        if flag:
            if not func:
                pass
            else:
                func()
    
    def update(self, dt): #sample update function

        self.checkPos()
        
        if self.debug:
            print('{} pos: x={},y={}'.format(self.name,self.x,self.y))
