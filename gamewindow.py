#this file takes all the elements of the game made and puts it all together
import pyglet, hud, random, score
from objects import player, ai, base, ammobox, speedboost
from assets import resources

class GameWindow: #this class controls game behaviour

    def __init__(self,mapChoice,mycon,playerSprite):

        self.mapChoice = mapChoice
        self.mycon = mycon
        self.playerSprite = playerSprite

        #these are just to reduce typing
        self.WIDTH = resources.WIDTH
        self.HEIGHT = resources.HEIGHT
        self.FRAMERATE = resources.FRAMERATE
        self.ZEROX = resources.ZEROX
        self.ZEROY = resources.ZEROY

        #add in names of moving objects; this list helps optimize collisionCheck()
        self.lst = ['player','ai']

        #controls maximum no of bots and ammoboxes on screen
        self.aiCount = 3
        self.ammoBoxCount = 2

        self.pointLimit = 100 #for rage mode to be activated
        
        if resources.DEBUG:
            self.pointLimit = 6
            print('\tWARNING: pointLimit for rage mode has been set to {}'.format(self.pointLimit))

        #pyglet window
        self.window = pyglet.window.Window(self.WIDTH,self.HEIGHT,caption=resources.TITLE)
        icon = resources.loadImg('icon')
        self.window.set_icon(icon)

        #display FPS counter on lower left hand corner when debugging is enabled
        if resources.DEBUG:
            self.fpsDisp = pyglet.window.FPSDisplay(window=self.window)

        #create batch and groups
        self.batch = pyglet.graphics.Batch() #this all important batch renders nearly all of the objects in the game
        self.groups = []
        for i in range(3):
            self.groups += [pyglet.graphics.OrderedGroup(i)] #use these groups in the lists to define priority of what to draw

        #load in map
        self.bg = resources.loadMap(self.mapChoice,batch=self.batch,group=self.groups[0])

        #create hud, player, and base
        self.hud = hud.HUD(self.batch, self.groups[1])
        self.player = player.Player(x=self.WIDTH//2 + self.ZEROX, y=self.HEIGHT-32)
        self.player.sprite = resources.loadSprite(self.player, name=self.playerSprite)
        self.base = base.Base(x=self.WIDTH//2 + self.ZEROX, y=self.HEIGHT//2 + self.ZEROY,batch=self.batch,group=self.groups[2])

        self.solidStuff = [self.player, self.base] #this is a list of all things in the game

        #these variables are used to take input and for pausing game
        self.pause = False
        self.pauseStatementRun = False
        self.t = 0

        #these variables control how power ups work
        self.powerUpTime = 0
        self.powerUp = False

        #these variables control how rage mode works
        self.rageModeTime = 0
        self.rageMode = False
        self.rageModeMusic = resources.loadMusic('ragemode')

        @self.window.event
        def on_draw(): #this function is responsible for the drawing of all the objects

            self.window.clear()
            self.window.push_handlers(self.player.key_handler)
            self.batch.draw()
            self.player.draw()
            if resources.DEBUG:
                self.fpsDisp.draw()

        #add loading code here
        self.loadingScreen = resources.loadImg('panzerposter')
        self.loadingScreen = pyglet.sprite.Sprite(img=self.loadingScreen, x = self.ZEROX, y = self.ZEROY, batch=self.batch, group=self.groups[0])
        print('loading game...')

        self.explodeSound = resources.loadMusic('explode')
        
        startSound = resources.loadMusic('CarStart')
        startSound.play()

        self.musicPlayer = pyglet.media.Player()

    def dontAddCollidingThing(self,x):
    
        for thing in self.solidStuff: #we make sure this thing does not collide with another thing already on screen
        
            if x.collisionCheck(thing):
                if resources.DEBUG:
                    print('this {} is NOT being added!'.format(x.name))
                del x
                break
            
        else:

            if resources.DEBUG:
                print('this {} IS being added!'.format(x.name))
            x.checkPos()
            return x

    def generateAI(self):

        r1 = random.randint(0,1)
        r2 = random.randint(0,1)

        img = resources.loadImg('ai')
        width = img.width//2
        height = img.height//2

        del img

        #code which randomly generates coordinates near the corners of screen
        if r1:
            a = random.randint(self.ZEROX + width, self.ZEROX + self.WIDTH//10)
        else:
            a = random.randint(9*(self.WIDTH//10), self.WIDTH - width)

        if r2:
            b = random.randint(self.ZEROY + height, self.ZEROY + self.HEIGHT//10)
        else:
            b = random.randint(9*(self.HEIGHT//10),self.HEIGHT - height)

        del width, height

        #make an AI object using the randomly generated coordinates
        x = ai.AI(x=a, y=b, batch=self.batch, group =self.groups[2])
  
        #some chance of spawing a more deadly bot
        r3 = random.randint(0,3)

        if not r3:
            x.speed = 2*x.speed
            x.sprite = resources.loadSprite(x,name='bot2')

        if self.rageMode:
            x.sprite = resources.loadSprite(x,name='ragebot')
    
        return self.dontAddCollidingThing(x)

    def powerup(self,name='ammobox'):

        img = resources.loadImg(name)
        width = img.width//2
        height = img.height//2
        del img
        rx = random.randint(self.ZEROX+width,self.WIDTH-width)
        ry = random.randint(self.ZEROY+height,self.HEIGHT-height)

        if name == 'ammobox':
            x = ammobox.AmmoBox(x=rx, y=ry, batch=self.batch, group =self.groups[2])
        elif name == 'speedboost':
            x = speedboost.SpeedBoost(x=rx, y=ry, batch=self.batch, group=self.groups[2])

        return self.dontAddCollidingThing(x)

    def countThings(self,name):

        count = 0
        for i in self.solidStuff:
            if i.name == name:
                count+=1
        return count

    def rageModeCode(self,dt):

        if self.player.rageModeMeter >= self.pointLimit and not self.rageMode and self.player.key_handler[pyglet.window.key.R] and self.t > 0.1:
            #remove all powerups
            for i in self.solidStuff:
                if i.name == 'speedboost':
                    self.solidStuff.remove(i)
            #toggle rage mode on
            self.rageMode = True
            self.t = 0
            #add rage mode effects
            self.player.sprite = resources.loadSprite(self.player,name='darktank')
            self.player.speed = 500
            self.player.unlimAmmo = True
            self.aiCount = 5
            #change the map to ragemap
            self.bg.delete()
            self.bg = resources.loadMap('ragemap',self.batch,self.groups[0])
            #play rage music
            self.musicPlayer = pyglet.media.Player()
            self.musicPlayer.queue(self.rageModeMusic)
            self.musicPlayer.play()

        elif self.rageMode:
            #keep track of rage mode time
            self.rageModeTime += dt
            if self.rageModeTime > 30:
                #toggle rage mode off
                self.rageMode = False
                self.player.rageModeMeter = 0
                self.player.sprite = resources.loadSprite(self.player,name=self.playerSprite)
                self.player.speed = 200
                self.player.unlimAmmo = False
                self.rageModeTime = 0
                self.aiCount = 3
                #reset map
                self.bg.delete()
                self.bg = resources.loadMap(self.mapChoice,self.batch,self.groups[0])
                del self.musicPlayer

    def powerUpCode(self,dt):

        if self.player.points > 3 and not self.powerUp and not self.rageMode:
            for i in self.solidStuff:
                if i.name == 'speedboost':
                    self.solidStuff.remove(i)
            self.powerUp = True
            randomSpeedBoost = self.powerup(name='speedboost')
            if randomSpeedBoost is not None:
                self.solidStuff.append(randomSpeedBoost)
                if resources.DEBUG:
                    print('powerup added!')
    
        elif self.powerUp and not self.rageMode:
            self.powerUpTime += dt
            if self.powerUpTime > 10:
                self.powerUp = False
                self.powerUpTime = 0
                self.player.speed = 200
                for i in self.solidStuff:
                    if i.name == 'ai':
                        i.dmgRate = i.oldDmgRate

    def addAI(self):

        currentAiCount = self.countThings('ai')

        if currentAiCount < self.aiCount:
    
            randomAI = self.generateAI()
            if randomAI is not None:
                self.solidStuff.append(randomAI)
            del randomAI

    def addAmmoBoxes(self):

        currentAmmoBox = self.countThings('ammobox')

        if self.player.ammo == 0 and currentAmmoBox < self.ammoBoxCount:
    
            randomAmmoBox = self.powerup()
            if randomAmmoBox is not None:
                self.solidStuff.append(randomAmmoBox)
            del randomAmmoBox

    def update(self,dt): #this function updates the objects

        if self.base.health <= 0: #add game over code here

            self.window.close()
            score.Score(self.player.points,self.mycon)
            quit()
    
        else:

            self.t += dt

            if resources.DEBUG:
                print('FRAMERATE: {}'.format(1/dt))

            if self.t > 0.1 and self.player.key_handler[pyglet.window.key.P]:
        
                self.t = 0 #reset the t variable to count the delay
                self.pause = not self.pause #toggle pause variable
            
            #this variable controls when the R symbol will be showed
            ragemodeIndicator = False
            if self.player.rageModeMeter >= self.pointLimit and not self.rageMode:
                ragemodeIndicator = True
    
            #update the hud
            self.hud.update(self.base.health, self.player.points, self.player.ammo, ragemodeIndicator, self.pause)
            if not self.pause: #add main game loop code here
        
                if self.rageMode and self.pauseStatementRun:
                    self.musicPlayer.play()

                self.pauseStatementRun = False
                self.collisionCheck()
            
                #update all the objects we need to update
                self.player.update(dt)
        
                for i in self.solidStuff:
                    if i.name == 'ai':
                        i.update(self.base,dt)

                #count the no. of things of specific names being rendered
                currentAmmoBox = self.countThings('ammobox')
                currentAiCount = self.countThings('ai')

                if resources.DEBUG:
                    print('ai on screen: {}'.format(currentAiCount))
                    print('ammoboxes on screen: {}'.format(currentAmmoBox))

                #rage mode code
                self.rageModeCode(dt)

                #add powerups randomly based on conditions given and remove them as well
                self.powerUpCode(dt)

                #add required no of ammoboxes
                self.addAmmoBoxes()

                #add the required no of ai objects to the list
                self.addAI()

            elif not self.pauseStatementRun: #add paused code here
                
                self.pauseStatementRun = True
                if self.rageMode:
                    self.musicPlayer.pause()

    def collisionCheck(self): #this important function checks for collisions using 2 loops and optimizations
   
        for i in self.player.projectiles: #this loop adds in all of the projectiles spawned by player
            if i not in self.solidStuff:
                self.solidStuff.append(i)
  
        if resources.DEBUG:
            print('solidStuff: {}'.format(self.solidStuff))

        for i in range(len(self.solidStuff)): #first loop; this is the main stuff

            if not self.solidStuff[i].dead and self.solidStuff[i].name in self.lst: #only certain moving objects are checked against for collisions

                if resources.DEBUG:
                    print('loop 1 started for thing1={}'.format(self.solidStuff[i]))

                for j in range(len(self.solidStuff)): #second loop
                    
                    if not self.solidStuff[i].dead and j != i:
                        if resources.DEBUG:
                            print('collision being checked with thing2={}'.format(self.solidStuff[j]))
                        if self.solidStuff[i].collisionCheck(self.solidStuff[j]):
                            if resources.DEBUG:
                                print('collision with thing2={} detected!'.format(self.solidStuff[j]))
                            self.solidStuff[j].collisionAction(self.solidStuff[i])
                            if not self.solidStuff[i].dead and not self.solidStuff[j].dead: #makes sure both collision statements are run if both are still alive
                                if resources.DEBUG:
                                    print('second collision being run b/w {} and {}'.format(self.solidStuff[i], self.solidStuff[j]))
                                self.solidStuff[i].collisionAction(self.solidStuff[j])

        for thing in self.solidStuff: #this loop removes all of the dead objects from the game
    
            if thing.dead:
        
                thing.sprite.delete()
                if resources.DEBUG:
                    print('sprite deleted!')
                self.solidStuff.remove(thing)
        
                if thing in self.player.projectiles: #add points of projectile to player and remove from projectiles list
                    self.player.points += thing.points
                    self.player.rageModeMeter += thing.points
                    self.player.projectiles.remove(thing)
        
                if thing.name == 'ai': #play the explosion sound
                    self.explodeSound.play()
                del thing

    def runGame(self):

        #these lines actually run the pyglet code and ensure update() is run periodically
        pyglet.clock.schedule_interval(self.update,1/self.FRAMERATE)
        #add loading completed message here
        print('loading completed')
        self.loadingScreen.delete()
        #run game
        pyglet.app.run()
