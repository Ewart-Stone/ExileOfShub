#code written By and Owned by Ewart Stone
#started 6/7/2019, finished 7/4/2019
#purpose is to provide an entertaining and fun small game

#import modules
import pygame
import time
import os
import random

xWin = 0
yWin = 0

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (xWin,yWin)

#define screen size
d_height = 720
d_width = 1360


#define colours
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
white = (255, 255, 255)
bright_red = (255,0,0)
bright_green = (0,255,0)
bright_blue = (0,0,255)
grey = (141,141,141)
dark_grey = (50,50,50)


#define global variables
bgCount = 0

paused = False
noteState = False

#initialise pygame
pygame.init()

gameDisplay = pygame.display.set_mode((d_width, d_height)) #define screen

pygame.display.set_caption("Exile of Shub") #change caption

clock = pygame.time.Clock()

#define music and sounds
outdoorMusic = "Audio/Music/Outdoors/cicada.mp3" #pygame.mixer.music.set_volume(0.05)
houseAmbience = "Audio/Music/Indoors/ambience.mp3" #

babyGoatRawr = pygame.mixer.Sound("Audio/Sounds/babyGoat/rawrXD.wav")
doorOpen = pygame.mixer.Sound("Audio/Sounds/doors/door.wav")
footSteps = pygame.mixer.Sound("Audio/Sounds/player/footSteps.wav")
playerYell = pygame.mixer.Sound("Audio/Sounds/player/playerYell.wav")

class babyGoat(object): #define baby goat enemy class
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 1
        self.chaseVel = 2
        self.damage = 50
        self.left = False
        self.right = False
        self.walkCount = 0

    def search(self,player,bg): #function responsible for AI searching for player
        
        if self.x - 600 + bg.x < player.x < self.x + 600 + bg.x and player.hidden == False:
            if self.x + bg.x - player.x > 0:
                self.x -= self.chaseVel
            elif self.x + bg.x - player.x < 0:
                self.x += self.chaseVel
            else:
                if self.x + bg.x - 20 < player.x < self.x + bg.x + 400 and self.y - 150 < player.y < self.y + 200:
                    self.kill(player)
                    
        elif player.xyell != 0:
            if self.x + bg.x - player.xyell > 0:
                self.x -= self.chaseVel
            if self.x + bg.x - player.xyell < 0:
                self.x += self.chaseVel
        else:
            self.move()
    
    def move(self): #controls how the AI moves and whether it roars

        self.num = random.randrange(1,25)
        
        if self.num == 1:
            self.direction = "Left"
        elif self.num == 2:
            self.direction = "Right"
        else:
            self.direction = "None"
        
        if self.direction == "Left":
            for count in range(15):
                self.x -= self.vel
            
        if self.direction == "Right":
            for count in range(15):
                self.x += self.vel
            
        if self.direction == "None":
            
            self.roarQuery = random.randrange(1,1250)

            if self.roarQuery == 1:
                pygame.mixer.Sound.play(babyGoatRawr)
            
    def kill(self,player): #kills player
        #play kill animation
        #player die animation
        player.die()

class player(object): #define players
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        self.hidden = False
        self.inventory = []
        self.left = False
        self.right = False
        self.walkCount = 0
        player.xyell = 0

    def die(self): #player death function
        self.dead = True
        while self.dead:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        unpause()
                    
            gameDisplay.fill(grey)
            largeText = pygame.font.SysFont('arial', 115)
            textSurf, textRect = text_objects("You are dead", largeText)
            textRect.center = ((d_width/2),(d_height * 0.2))
            gameDisplay.blit(textSurf, textRect)
        

            button("Main Menu",580,310,200,100,red,bright_red,titleScreen)
            
            pygame.display.update()
            
    def boundary(self,bg): #sets boundaries for player
        
        if self.x < 0:
            self.x = 0
        elif self.x < 715 - self.width and bg.x < 0:
            self.x = 715 - self.width
        elif self.x > 1350 - self.width:
            self.x = 1350 - self.width
        elif self.x > 721 - self.width and bg.fin != True:
            self.x = 721 - self.width
            
        if self.y < 370:
            self.y = 370
        elif self.y > 521:
            self.y = 521

    def yell(self): #yell to lure enemy
        pygame.mixer.Sound.play(playerYell)
        self.xyell = self.x
        
    def endYell(self,goat,bg): #end yell so it doesn't last indefinitely
        if goat.x + bg.x == self.xyell:
            self.xyell = 0

        
    def hide(self, event, objHide,hidden,x,y): #hides the player in objects
        if event.key == pygame.K_UP and objHide == True:
            hidden = True
            x=0
            y=0
        return hidden,x,y
    
    def invAddItem(self,item,sprite):
        self.inventory.append([item,sprite])
        
    def removeItem(self,name): #removes a given item from the inventory
        deleted = False
        count = 0
        for item in self.inventory:
            if item[0] == name and deleted == False:
                del self.inventory[count]
                deleted = True
            count += 1
            
    def searchInv(self,name): #searches inventory for an item
        for item in self.inventory:
            if item[0] == name:
                return True
            else:
                return False
                
    def invDisplay(self): #displays inventory
        self.iX = 440
        self.iY = 120
        self.count = 1
        self.Continue = True

        while self.Continue:

            gameDisplay.blit(invBg, (230,60))

            for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_e:
                                self.Continue = False

            for item in self.inventory: #blits each item in inventory in a particular pattern
                gameDisplay.blit(item[1], [self.iX,self.iY])
                self.iX += 185
                self.count += 1
                if self.count == 4:
                    self.iY = 385
                    self.iX = 440
                    

            self.iX = 440
            self.iY = 120
            self.count = 1
                    
            pygame.display.update()
            
    def pickUp(self,x,y,itemName,sprite): #player picks up item

        if x + 100 > self.x > x and y + 100 > self.y > y - 100:

            self.invAddItem(itemName,sprite)

            msg = "You found" + itemName + "!"
            dialogueText = pygame.font.SysFont('arial', 20)

            textSurf, textRect = text_objects(msg,dialogueText)
            textRect.center = ((d_width/2),(600))

            dis = True
            
            while dis:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            dis = False

                dialogueBox = pygame.draw.rect(gameDisplay, white, (200,550,960,720))
                gameDisplay.blit(textSurf, textRect)
            
                pygame.display.update()



                                 
                                 
class item(object): #define items for inventory
    def __init__(self,name,sprite):
        self.name = name
        self.sprite = sprite
            
class Wardrobe(object): #define wardrobe
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.hideState = False

    def hideTestDraw(self,idleObject, fullObject, hidden,bg):
        
        if self.hideState == True and hidden == True:
            blitObject(fullObject, (self.x + bg.x, self.y))
        else:
            blitObject(idleObject, (self.x + bg.x,self.y))

class Desk(object): #define desk
    def __init__(self,x,y,note):
        self.x = x
        self.y = y
        self.note = note
        
    def noteRead(self,x,y,bg): #collision detection for note in desk
        if self.x + 100 + bg.x > x > self.x + bg.x and self.y + 200 > y > self.y - 200:
            
            global noteState
            noteState = True
            noteScreen(self.note)
            
class Safe(object): #define safe
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.locked = True
        self.empty = False
        self.code = [1,9,2,8]
        
    def unlock(self,x,y): #unlock screen for safe puzzle
        
        if self.x + 150 > x > self.x and self.y + 150 > y > self.y - 1505 and self.locked == True:
            
            unlocking = True

            lockGuess = []
            
            while unlocking:

                while len(lockGuess) != 4:
                    
                    blitObject(safeInterface, (0,0))

                    for event in pygame.event.get():
                        
                        if event.type == pygame.KEYDOWN:
                            #play beep noise
                            if event.key == pygame.K_RETURN:
                                unlocking = False

                            if event.key == pygame.K_1:
                                lockGuess.append(1)
                            if event.key == pygame.K_2:
                                lockGuess.append(2)
                            if event.key == pygame.K_3:
                                lockGuess.append(3)
                            if event.key == pygame.K_4:
                                lockGuess.append(4)
                            if event.key == pygame.K_5:
                                lockGuess.append(5)
                            if event.key == pygame.K_6:
                                lockGuess.append(6)
                            if event.key == pygame.K_7:
                                lockGuess.append(7)
                            if event.key == pygame.K_8:
                                lockGuess.append(8)
                            if event.key == pygame.K_9:
                                lockGuess.append(9)
                                
                    pygame.display.update()
                    
                self.count = 0
                self.num = 0
                for each in lockGuess:
                    if each == self.code[self.count]:
                        self.num += 1
                    self.count += 1
                    
                if self.num == 4: #verifies input from user
                    self.locked = False
                else:
                    #incorrect beep
                    pass
                unlocking = False
                    

                pygame.display.update()
            
class chalkboard(object): #chalkboard object
    def __init__(self,x,y): #main initialisation with x,y co-ords and covered status
        self.x = x
        self.y = y
        self.covered = True
        
    def uncover(self,x,y,bg): #lets player uncover the chalkboard item to reveal what it shows
        if self.x + 400 + bg.x > x > self.x + bg.x and self.y < y < self.y + 400:
            self.covered = False
            
class genericObject(object): #generic non-special objects
    def __init__(self,x,y,sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
            
class Door(object): #door object
    def __init__(self,x,y,room,locked):
        self.room = room
        self.x = x
        self.y = y
        self.width = 269
        self.height = 357
        self.locked = locked
        
    def use(self,player,bg,xEntry,leftSide,bgPos): #use door to change level/room
        
        if self.x + bg.x < player.x < self.x + bg.x + self.width:
            if self.y < player.y < self.y + self.height:
                pygame.mixer.Sound.play(doorOpen)
                self.room(player,xEntry,leftSide,bgPos)
        
class Background(object):
    def __init__(self,width,height,x,sprite):
        self.width = width
        self.height = height
        self.x = x
        self.sprite = sprite
        self.fin = False

    def scrollBg(self, playerPos,player):
        global bgCount
        
        if playerPos > 720 and self.x < self.width - 1360 and player.right == True and self.x > -1360:
            self.x -= 2
            bgCount = bgCount + 3
            self.fin = False
        elif playerPos < 720 and self.x < 0 and player.left == True:
            self.x += 2
            bgCount = bgCount - 3
            self.fin = False
        else:
            self.fin = True
    

def loadImage(img):
    return pygame.image.load(img).convert_alpha()


def unpause():
    global paused
    paused = False
    
def quitGame():
    pygame.quit()
    quit()

def text_objects(text, font): #defines text objects for text display. Source: Sentdex at pythonprogramming.net
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
    
def button(msg,x,y,w,h,i,a,action): #defines buttons Source: Sentdex at pythonprogramming.net
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, a, [x,y,w,h])
        if click[0] == 1:
            action()
    else:
        pygame.draw.rect(gameDisplay, i, [x, y, w, h])

    smallText = pygame.font.SysFont('arial',20)
    
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf, textRect)

def dialogueScreen(text): #screen to display dialogue
    
    dialoguePause = True
    
    with open(text, mode='r', encoding="utf-8") as dialogue:
        lines = dialogue.read().splitlines()
    dialogueText = pygame.font.SysFont('arial', 20)
    
    while dialoguePause:

        for each in lines:

            Continue = False

            while Continue == False:

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            Continue = True

                textSurf, textRect = text_objects(each, dialogueText)
                textRect.center = ((d_width/2),(600))
                
                dialogueBox = pygame.draw.rect(gameDisplay, white, (0,550,1360,720))
                gameDisplay.blit(textSurf, textRect)
                
                pygame.display.update()
                
        dialoguePause = False
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    dialoguePause = False

def noteScreen(note): #note screen to display notes in desks
    
    global noteState
    ix = 60
    
    with open(note, mode='r', encoding="utf-8") as dialogue:
        lines = dialogue.read().splitlines()
    noteFont = pygame.font.SysFont('arial', 20)
    
    while noteState:

            dialogueBox = pygame.draw.rect(gameDisplay, white, (300,0,760,720)) #replace with note sprite
            #gameDisplay.blit(noteSprite,(300,0))

            for each in lines:

                textSurf, textRect = text_objects(str(each), noteFont)
                textRect.center = ((d_width/2),(ix))
                ix += 60
                gameDisplay.blit(textSurf,textRect)

            ix = 60
            msg = ("Press P to continue")
            textSurf, textRect = text_objects(msg, noteFont)
            textRect.center = ((d_width/2), (660))
            
            gameDisplay.blit(textSurf, textRect)

            for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            noteState = False

            pygame.display.update()
        
def helpScreen(): #displays help menu
    helpState = True
    ix = 200

    with open("Dialogue/help.txt", mode='r', encoding="utf-8") as dialogue:
        lines = dialogue.read().splitlines()
    dialogueText = pygame.font.SysFont('arial', 40)

    while helpState:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    helpState = False
                    
                    
        gameDisplay.fill(grey)
        dialogueBox = pygame.draw.rect(gameDisplay, white, (300,0,760,720))
        largeText = pygame.font.SysFont('arial', 115)
        textSurf, textRect = text_objects("Help", largeText)
        textRect.center = ((d_width/2),(d_height * 0.15))
        gameDisplay.blit(textSurf, textRect)

        for each in lines:

            textSurf, textRect = text_objects(str(each), dialogueText)
            textRect.center = ((d_width/2),(ix))
            ix += 30
            gameDisplay.blit(textSurf,textRect)

        ix = 200
        msg = ("Press ESC to continue")
        textSurf, textRect = text_objects(msg, dialogueText)
        textRect.center = ((d_width/2), (660))
        
        gameDisplay.blit(textSurf, textRect)
        
        pygame.display.update()
        
def creditScreen(): #displays credits screen
    creditState = True
    ix = 200

    with open("Dialogue/credits.txt", mode='r', encoding="utf-8") as dialogue:
        lines = dialogue.read().splitlines()
    dialogueText = pygame.font.SysFont('arial', 40)

    while creditState:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    creditState = False
                    
                    
        gameDisplay.fill(grey)
        dialogueBox = pygame.draw.rect(gameDisplay, white, (300,0,760,720))
        largeText = pygame.font.SysFont('arial', 115)
        textSurf, textRect = text_objects("Credits", largeText)
        textRect.center = ((d_width/2),(d_height * 0.15))
        gameDisplay.blit(textSurf, textRect)

        for each in lines:

            textSurf, textRect = text_objects(str(each), dialogueText)
            textRect.center = ((d_width/2),(ix))
            ix += 30
            gameDisplay.blit(textSurf,textRect)

        ix = 200
        msg = ("Press ESC to continue")
        textSurf, textRect = text_objects(msg, dialogueText)
        textRect.center = ((d_width/2), (660))
        
        gameDisplay.blit(textSurf, textRect)

        pygame.display.update()
        
def pause_screen(): #displays pause screen
    
    global paused
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    unpause()
                    
        gameDisplay.fill(grey)
        largeText = pygame.font.SysFont('arial', 115)
        textSurf, textRect = text_objects("Paused", largeText)
        textRect.center = ((d_width/2),(d_height * 0.2))
        gameDisplay.blit(textSurf, textRect)
    

        button("Continue",400,250,200,100,green,bright_green,unpause)
        button("Exit",700,350,200,100,red,bright_red,quitGame)
        button("Help",400,450,200,100,green,bright_green,helpScreen)
        
        pygame.display.update()

def titleScreen(): #displays title screen

    time.sleep(1)

    pygame.mixer.Sound.stop(footSteps)
    
    title = True
    
    while title:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                
        gameDisplay.fill(grey)
        largeText = pygame.font.SysFont('arial', 115)
        textSurf, textRect = text_objects("Exile of Shub", largeText)
        textRect.center = ((d_width/2),(d_height/2))
        gameDisplay.blit(textSurf, textRect)
    

        button("Start",400,450,200,100,green,bright_green,main)
        button("Exit",800,450,200,100,red,bright_red,quitGame)
        button("Help",400,600,200,100,green,bright_green,helpScreen)
        button("Credits",800,600,200,100,green,bright_green,creditScreen)
        
        
        pygame.display.update()

def win(player):#player win scene

    pygame.mixer.Sound.stop(footSteps)
    
    winScreen = True
    
    while winScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                
        gameDisplay.fill(grey)
        largeText = pygame.font.SysFont('arial', 115)
        textSurf, textRect = text_objects("To Be", largeText)
        textRect.center = ((d_width/2),(240))
        gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = text_objects("Continued!!!", largeText)
        textRect.center = ((d_width/2),(d_height/2))
        gameDisplay.blit(textSurf, textRect)

        button("Title",400,450,100,50,green,bright_green,titleScreen)
        button("Exit",800,450,100,50,red,bright_red,quitGame)
        
        
        pygame.display.update()
def finale(player, a,b,c): #plays end cutscene

    pygame.mixer.music.stop()
    pygame.mixer.music.load(outdoorMusic)
    pygame.mixer.music.play(-1, 0.0) #do not have looping and lock activation between selections
    pygame.mixer.music.set_volume(0.25)

    blitObject(backgroundIntro,(0,0))
    blitObject(player_sprite, (1025,450))

    pygame.display.update()

    time.sleep(2)

    pygame.draw.rect(gameDisplay, white, (0,0,1360,720))

    pygame.display.update()
    
    time.sleep(1)
    blitObject(finBg,(0,0))
    blitObject(player_sprite, (1025,450))

    pygame.display.update()
               
    pygame.mixer.Sound.play(babyGoatRawr)
    
    time.sleep(2)
               
    win(player)
        
def quitGame(): #quits game
    pygame.quit()
    quit()


def blitObject(spriteBoi, coord):
    
    gameDisplay.blit(spriteBoi, coord)

def hideCheck(obj,objHide,x,y): #checks if player is hideable near wardrobes
    if obj[0]+85 > x > obj[0] and obj[1]+105 > y > obj[1]:
        objHide = True
    else:
        objHide = False
    return objHide






#load all sprites
player_sprite = loadImage("character/player/idle.png")

walkLeft = [loadImage("character/player/R1.png"),loadImage("character/player/R2.png"),loadImage("character/player/R3.png"),loadImage("character/player/R4.png")]
walkRight = [loadImage("character/player/L1.png"),loadImage("character/player/L2.png"),loadImage("character/player/L3.png"),loadImage("character/player/L4.png")]

babyGoat_sprite = loadImage("character/babyGoat/idle.png")

keySprite = loadImage("objects/key.png")

wardrobe = loadImage("objects/wardrobe.png")
wardrobeFULL = loadImage("objects/wardrobeHidden.png")

desk = loadImage("objects/desk.png")
deskBigSprite = loadImage("objects/bigDesk.png")
doorSprite = loadImage("objects/door.png")

safeSprite = loadImage("objects/deskSafe.png")
safeInterface = loadImage("objects/safeClose.png")

clockSprite = loadImage("objects/clock.png")

chalkboardSprite = loadImage("objects/chalkboard.png")
chalkboardCoveredSprite = loadImage("objects/chalkboardCovered.png")

r1 = loadImage("background/B1.png")
r2 = loadImage("background/B2.png")
r3 = loadImage("background/B3.png")
basementBg = loadImage("background/basement.png")
atticBg = loadImage("background/attic.png")
bathroomBg = loadImage("background/bathroom.png")
studyBg = loadImage("background/study.png")
bedroomBg = loadImage("background/bedroom.png")
backgroundIntro = loadImage("background/Bo1.png")
finBg = loadImage("background/fin.png")

dialogueBox = loadImage("background/dialogueBg.png")
invBg = loadImage("background/InvBg.png")

Simon = player(25,519,84,215)

#def room
def room1(Simon,xEntry,leftSide,bgPos):
# bjects and variables
    Simon.x = xEntry

    global bgCount

    running = True

    goatSpawn = False

    num = random.randrange(0,3)

    if num == 1:
        goat = babyGoat(random.randrange(900,1800),490,150,300)
        goatSpawn = True

    ward1 = Wardrobe(787,300)
    desk1 = Desk(1700,450,"Dialogue/bloodiedNote.txt")
    clock1 = genericObject(400,180,clockSprite)
    
    B1 = Background(2720,720,0,r1)
    
    door1 = Door(0,160,finale,True)
    door2 = Door(2485,160,room2,False)
    door3 = Door(1360,160,attic,False)
    
    x_move = 0
    y_move = 0
    
    if leftSide == True:
        bgCount = 0
    else:
        B1.x = 0 - bgPos

    pygame.mixer.music.stop() #stop previous music track and start a new one
    pygame.mixer.music.load(houseAmbience)
    pygame.mixer.music.play(-1, 0.0) #do not have looping and lock activation between selections
    pygame.mixer.music.set_volume(0.25)
    
    while running:

        clock.tick(120)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()



            if event.type == pygame.KEYDOWN: #controls

                if event.key == pygame.K_ESCAPE:
                    global paused
                    paused = True
                    pause_screen()
                    
                if event.key == pygame.K_a and Simon.x > Simon.vel and Simon.hidden == False:
                    x_move -= Simon.vel
                    Simon.left = True
                    pygame.mixer.Sound.play(footSteps)

                if event.key == pygame.K_d and Simon.x < 1360 - Simon.width and Simon.hidden == False:
                    x_move += Simon.vel
                    Simon.right = True
                    pygame.mixer.Sound.play(footSteps)

                Simon.hidden,x_move,y_move = Simon.hide(event, ward1.hideState,Simon.hidden,x_move,y_move)

                if event.key == pygame.K_RETURN:

                    keyInInv = Simon.searchInv("key")
                    
                    if keyInInv == True:
                        Simon.removeItem("Key")
                        door1.use(Simon,B1,0,False,0)
                    elif 0 + B1.x + 200 > Simon.x:
                        dialogueScreen("Dialogue/locked.txt")
                        
                    door2.use(Simon,B1,25,True,0)
                    door3.use(Simon,B1,0,False,0)

                    desk1.noteRead(Simon.x,Simon.y,B1)
                
                if event.key == pygame.K_e:
                    Simon.invDisplay()
                    
                if event.key == pygame.K_f:
                    Simon.yell()
                    
                if event.key == pygame.K_DOWN and Simon.hidden == True:
                    Simon.hidden = False
                    
                if event.key == pygame.K_w and Simon.y > 340 and Simon.hidden == False:
                    y_move -= Simon.vel
                    
                if event.key == pygame.K_s and Simon.y < 520 and Simon.hidden == False:
                    y_move += Simon.vel    

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d: 
                    x_move = 0
                    Simon.left = False
                    Simon.right = False
                    pygame.mixer.Sound.stop(footSteps)
                    
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    y_move = 0
                

        Simon.x += x_move #move players
        Simon.y += y_move
        Simon.boundary(B1)

        ward1.hideState = hideCheck((ward1.x + B1.x,ward1.y), ward1.hideState,Simon.x,Simon.y)        

        B1.scrollBg(Simon.x + Simon.width,Simon)#displays all sprites and objects
        blitObject(B1.sprite, (B1.x,0))

        ward1.hideTestDraw(wardrobe, wardrobeFULL, Simon.hidden,B1)

        blitObject(desk, (desk1.x + B1.x,desk1.y))
        blitObject(clock1.sprite, (clock1.x + B1.x,clock1.y))

        blitObject(doorSprite, (door1.x + B1.x,door1.y))
        blitObject(doorSprite, (door2.x + B1.x,door2.y))
        blitObject(doorSprite, (door3.x + B1.x,door3.y))

        if goatSpawn == True:
            blitObject(babyGoat_sprite, (goat.x + B1.x,goat.y))
            goat.search(Simon,B1)
            Simon.endYell(goat,B1)
        
        if Simon.hidden == False:

            if Simon.walkCount + 1 >= 120:
                Simon.walkCount = 0

            if Simon.left == True:
                gameDisplay.blit(walkLeft[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
                
            elif Simon.right == True:
                gameDisplay.blit(walkRight[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
            else:
                blitObject(player_sprite, (Simon.x,Simon.y))
            
        pygame.display.update()


def room2(Simon,xEntry,leftSide,bgPos): #same structure as room and and is same for all rooms

    Simon.x = xEntry

    global bgCount

    running = True

    goatSpawn = False

    num = random.randrange(0,3)

    if num == 1:
        goat = babyGoat(random.randrange(900,1800),490,150,300)
        goatSpawn = True

    ward1 = Wardrobe(500,300)
    ward2 = Wardrobe(1400,300)
    desk1 = Desk(1950,475,"Dialogue/cultistJournal.txt")
    
    B1 = Background(2720,720,0,r2)
    
    door1 = Door(0,160,room1,True)
    door2 = Door(2480,160,room3,False)
    door3 = Door(1060,160,basement,False)
    door4 = Door(1660,160,bathroom,False)
    
    x_move = 0
    y_move = 0

    if leftSide == True:
        bgCount = 0
    else:
        B1.x = 0 - bgPos
    
    while running:

        clock.tick(120)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()



            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    global paused
                    paused = True
                    pause_screen()
                    
                if event.key == pygame.K_a and Simon.x > Simon.vel and Simon.hidden == False:
                    x_move -= Simon.vel
                    Simon.left = True
                    pygame.mixer.Sound.play(footSteps)

                if event.key == pygame.K_d and Simon.x < 1360 - Simon.width and Simon.hidden == False:
                    x_move += Simon.vel
                    Simon.right = True
                    pygame.mixer.Sound.play(footSteps)

                Simon.hidden,x_move,y_move = Simon.hide(event, ward1.hideState,Simon.hidden,x_move,y_move)
                Simon.hidden,x_move,y_move = Simon.hide(event, ward2.hideState,Simon.hidden,x_move,y_move)

                if event.key == pygame.K_RETURN:
                    
                    desk1.noteRead(Simon.x,Simon.y,B1)
                    
                    door1.use(Simon,B1,2485,False,1360)
                    door2.use(Simon,B1,25,True,0)
                    door3.use(Simon,B1,0,True,0)
                    door4.use(Simon,B1,0,True,0)
                
                if event.key == pygame.K_e:
                    Simon.invDisplay()
                    
                if event.key == pygame.K_f:
                    Simon.yell()
                    
                if event.key == pygame.K_DOWN and Simon.hidden == True:
                    Simon.hidden = False
                    
                if event.key == pygame.K_w and Simon.y > 340 and Simon.hidden == False:
                    y_move -= Simon.vel
                    
                if event.key == pygame.K_s and Simon.y < 520 and Simon.hidden == False:
                    y_move += Simon.vel

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d: 
                    x_move = 0
                    Simon.left = False
                    Simon.right = False
                    pygame.mixer.Sound.stop(footSteps)
                    
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    y_move = 0
                

        Simon.x += x_move
        Simon.y += y_move
        Simon.boundary(B1)

        ward1.hideState = hideCheck((ward1.x + B1.x,ward1.y), ward1.hideState,Simon.x,Simon.y)
        ward2.hideState = hideCheck((ward2.x + B1.x,ward2.y), ward2.hideState,Simon.x,Simon.y)
        

        B1.scrollBg(Simon.x + Simon.width,Simon)
        blitObject(B1.sprite, (B1.x,0))

        ward1.hideTestDraw(wardrobe, wardrobeFULL, Simon.hidden,B1)
        ward2.hideTestDraw(wardrobe, wardrobeFULL, Simon.hidden,B1)

        blitObject(desk, (desk1.x + B1.x,desk1.y))

        blitObject(doorSprite, (door1.x + B1.x,door1.y))
        blitObject(doorSprite, (door2.x + B1.x,door2.y))
        blitObject(doorSprite, (door3.x + B1.x,door3.y))
        blitObject(doorSprite, (door4.x + B1.x,door4.y))

        if goatSpawn == True:
            blitObject(babyGoat_sprite, (goat.x + B1.x,goat.y))
            goat.search(Simon,B1)
            Simon.endYell(goat,B1)

        
        if Simon.hidden == False:

            if Simon.walkCount + 1 >= 120:
                Simon.walkCount = 0

            if Simon.left == True:
                gameDisplay.blit(walkLeft[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
                
            elif Simon.right == True:
                gameDisplay.blit(walkRight[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
            else:
                blitObject(player_sprite, (Simon.x,Simon.y))
            
        pygame.display.update()

def room3(Simon,xEntry,leftSide,bgPos):

    Simon.x = xEntry

    global bgCount

    if leftSide == True:
        bgCount = 0

    running = True

    goatSpawn = False

    num = random.randrange(0,3)

    if num == 1:
        goat = babyGoat(random.randrange(900,1800),490,150,300)
        goatSpawn = True

    ward1 = Wardrobe(300,300)
    desk1 = Desk(800,475,"Dialogue/darrelsNote.txt")
    clock1 = genericObject(2300,215,clockSprite)
    
    B1 = Background(2720,720,0,r3)
    
    door1 = Door(0,160,room2,True)
    door2 = Door(1060,160,study,False)
    door3 = Door(1660,160,bedroom,False)
    
    x_move = 0
    y_move = 0

    if leftSide == True:
        bgCount = 0
    else:
        B1.x = 0 - bgPos
    
    while running:

        clock.tick(120)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()



            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    global paused
                    paused = True
                    pause_screen()
                    
                if event.key == pygame.K_a and Simon.x > Simon.vel and Simon.hidden == False:
                    x_move -= Simon.vel
                    Simon.left = True
                    pygame.mixer.Sound.play(footSteps)

                if event.key == pygame.K_d and Simon.x < 1360 - Simon.width and Simon.hidden == False:
                    x_move += Simon.vel
                    Simon.right = True
                    pygame.mixer.Sound.play(footSteps)

                Simon.hidden,x_move,y_move = Simon.hide(event, ward1.hideState,Simon.hidden,x_move,y_move)
                

                if event.key == pygame.K_RETURN:
                    
                    door1.use(Simon,B1,2485,False,1360)
                    door2.use(Simon,B1,0,False,0)
                    door3.use(Simon,B1,0,False,0)

                    desk1.noteRead(Simon.x,Simon.y,B1)
                
                if event.key == pygame.K_e:
                    Simon.invDisplay()
                    
                if event.key == pygame.K_f:
                    Simon.yell()
                    
                if event.key == pygame.K_DOWN and Simon.hidden == True:
                    Simon.hidden = False
                    
                if event.key == pygame.K_w and Simon.y > 340 and Simon.hidden == False:
                    y_move -= Simon.vel
                    
                if event.key == pygame.K_s and Simon.y < 520 and Simon.hidden == False:
                    y_move += Simon.vel
                    

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d: 
                    x_move = 0
                    Simon.left = False
                    Simon.right = False
                    pygame.mixer.Sound.stop(footSteps)
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    y_move = 0
                

        Simon.x += x_move
        Simon.y += y_move
        Simon.boundary(B1)

        ward1.hideState = hideCheck((ward1.x,ward1.y), ward1.hideState,Simon.x,Simon.y)
        

        B1.scrollBg(Simon.x + Simon.width,Simon)
        blitObject(B1.sprite, (B1.x,0))

        ward1.hideTestDraw(wardrobe, wardrobeFULL, Simon.hidden,B1)

        blitObject(desk, (desk1.x + B1.x,desk1.y))
        blitObject(clock1.sprite, (clock1.x + B1.x,clock1.y))

        blitObject(doorSprite, (door1.x + B1.x,door1.y))
        blitObject(doorSprite, (door2.x + B1.x,door2.y))
        blitObject(doorSprite, (door3.x + B1.x,door3.y))

        if goatSpawn == True:
            blitObject(babyGoat_sprite, (goat.x + B1.x,goat.y))
            goat.search(Simon,B1)
            Simon.endYell(goat,B1)

        
        if Simon.hidden == False:

            if Simon.walkCount + 1 >= 120:
                Simon.walkCount = 0

            if Simon.left == True:
                gameDisplay.blit(walkLeft[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
                
            elif Simon.right == True:
                gameDisplay.blit(walkRight[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
            else:
                blitObject(player_sprite, (Simon.x,Simon.y))
            
        pygame.display.update()

def beginning(Simon):

    running = True

    B1 = Background(1320,720,0,backgroundIntro)

    door = Door(1000,225,room1,False)
    
    x_move = 0
    y_move = 0

    pygame.mixer.music.stop()
    pygame.mixer.music.load(outdoorMusic)
    pygame.mixer.music.play(-1, 0.0) #do not have looping and lock activation between selections
    pygame.mixer.music.set_volume(0.25)
    
    
    while running:

        clock.tick(120)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()



            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    global paused
                    paused = True
                    pause_screen()
                    
                if event.key == pygame.K_a and Simon.x > Simon.vel and Simon.hidden == False:
                    x_move -= Simon.vel
                    Simon.left = True
                    pygame.mixer.Sound.play(footSteps)

                if event.key == pygame.K_d and Simon.x < 1360 - Simon.width and Simon.hidden == False:
                    x_move += Simon.vel
                    Simon.right = True
                    pygame.mixer.Sound.play(footSteps)

                if event.key == pygame.K_RETURN:
                    door.use(Simon,B1,25,True,0)
                
                if event.key == pygame.K_e:
                    Simon.invDisplay()
                    
                if event.key == pygame.K_DOWN and Simon.hidden == True:
                    Simon.hidden = False
                    
                if event.key == pygame.K_w and Simon.y > 340 and Simon.hidden == False:
                    y_move -= Simon.vel
                    
                if event.key == pygame.K_s and Simon.y < 520 and Simon.hidden == False:
                    y_move += Simon.vel
                
    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d: 
                    x_move = 0
                    Simon.left = False
                    Simon.right = False
                    pygame.mixer.Sound.stop(footSteps)
                    
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    y_move = 0
                

        Simon.x += x_move
        Simon.y += y_move
        Simon.boundary(B1)        

        B1.scrollBg(Simon.x + Simon.width,Simon)
        blitObject(B1.sprite, (B1.x,0))

        blitObject(doorSprite, (door.x,door.y))

            
        if Simon.hidden == False:

            if Simon.walkCount + 1 >= 120:
                Simon.walkCount = 0

            if Simon.left == True:
                gameDisplay.blit(walkLeft[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
                
            elif Simon.right == True:
                gameDisplay.blit(walkRight[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
            else:
                blitObject(player_sprite, (Simon.x,Simon.y))
            
        pygame.display.update()

def attic(Simon,xEntry,leftSide,bgPos):

    running = True

    Simon.x = 0

    B1 = Background(1360,720,0,atticBg)

    door = Door(0,160,room1,False)
    chalkboard1 = chalkboard(500,300)
    
    x_move = 0
    y_move = 0

        
    while running:

        clock.tick(120)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()



            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    global paused
                    paused = True
                    pause_screen()
                    
                if event.key == pygame.K_a and Simon.x > Simon.vel and Simon.hidden == False:
                    x_move -= Simon.vel
                    Simon.left = True
                    pygame.mixer.Sound.play(footSteps)

                if event.key == pygame.K_d and Simon.x < 1360 - Simon.width and Simon.hidden == False:
                    x_move += Simon.vel
                    Simon.right = True
                    pygame.mixer.Sound.play(footSteps)

                if event.key == pygame.K_RETURN:
                    
                    door.use(Simon,B1,25,False,720)
                    
                    chalkboard1.uncover(Simon.x,Simon.y,B1)
                
                if event.key == pygame.K_e:
                    Simon.invDisplay()
                    
                if event.key == pygame.K_DOWN and Simon.hidden == True:
                    Simon.hidden = False
                    
                if event.key == pygame.K_w and Simon.y > 340 and Simon.hidden == False:
                    y_move -= Simon.vel
                    
                if event.key == pygame.K_s and Simon.y < 520 and Simon.hidden == False:
                    y_move += Simon.vel
    
    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d: 
                    x_move = 0
                    Simon.left = False
                    Simon.right = False
                    pygame.mixer.Sound.stop(footSteps)
                    
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    y_move = 0
                

        Simon.x += x_move
        Simon.y += y_move
        Simon.boundary(B1)        

        B1.scrollBg(Simon.x + Simon.width,Simon)
        blitObject(B1.sprite, (B1.x,0))

        blitObject(doorSprite, (door.x,door.y))

        if chalkboard1.covered == False:
            blitObject(chalkboardSprite, (chalkboard1.x,chalkboard1.y))
        elif chalkboard1.covered == True:
            blitObject(chalkboardCoveredSprite, (chalkboard1.x,chalkboard1.y))

            
        if Simon.hidden == False:

            if Simon.walkCount + 1 >= 120:
                Simon.walkCount = 0

            if Simon.left == True:
                gameDisplay.blit(walkLeft[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
                
            elif Simon.right == True:
                gameDisplay.blit(walkRight[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
            else:
                blitObject(player_sprite, (Simon.x,Simon.y))
            
        pygame.display.update()

def basement(Simon,xEntry,leftSide,bgPos):

    running = True

    Simon.x = 0

    B1 = Background(1360,720,0, basementBg)

    door = Door(35,165,room2,False)
    desk1 = Desk(450,476,"Dialogue/TheLastTest.txt")
    
    x_move = 0
    y_move = 0    
    
    while running:

        clock.tick(120)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()



            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    global paused
                    paused = True
                    pause_screen()
                    
                if event.key == pygame.K_a and Simon.x > Simon.vel and Simon.hidden == False:
                    x_move -= Simon.vel
                    Simon.left = True
                    pygame.mixer.Sound.play(footSteps)

                if event.key == pygame.K_d and Simon.x < 1360 - Simon.width and Simon.hidden == False:
                    x_move += Simon.vel
                    Simon.right = True
                    pygame.mixer.Sound.play(footSteps)

                if event.key == pygame.K_RETURN:
                    door.use(Simon,B1,25,False,420)
                    desk1.noteRead(Simon.x,Simon.y,B1)
                
                if event.key == pygame.K_e:
                    Simon.invDisplay()
                    
                if event.key == pygame.K_DOWN and Simon.hidden == True:
                    Simon.hidden = False
                    
                if event.key == pygame.K_w and Simon.y > 340 and Simon.hidden == False:
                    y_move -= Simon.vel
                    
                if event.key == pygame.K_s and Simon.y < 520 and Simon.hidden == False:
                    y_move += Simon.vel
                

    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d: 
                    x_move = 0
                    Simon.left = False
                    Simon.right = False
                    pygame.mixer.Sound.stop(footSteps)
                    
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    y_move = 0
                

        Simon.x += x_move
        Simon.y += y_move
        Simon.boundary(B1)        

        B1.scrollBg(Simon.x + Simon.width,Simon)
        blitObject(B1.sprite, (B1.x,0))

        blitObject(doorSprite, (door.x,door.y))
        blitObject(desk, (desk1.x,desk1.y))

            
        if Simon.hidden == False:

            if Simon.walkCount + 1 >= 120:
                Simon.walkCount = 0

            if Simon.left == True:
                gameDisplay.blit(walkLeft[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
                
            elif Simon.right == True:
                gameDisplay.blit(walkRight[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
            else:
                blitObject(player_sprite, (Simon.x,Simon.y))
            
        pygame.display.update()

def bathroom(Simon,xEntry,leftSide,bgPos):

    running = True

    Simon.x = 0

    B1 = Background(1360,720,0, bathroomBg)

    door = Door(15,162,room2,False)
    
    x_move = 0
    y_move = 0

   
    while running:

        clock.tick(120)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()



            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    global paused
                    paused = True
                    pause_screen()
                    
                if event.key == pygame.K_a and Simon.x > Simon.vel and Simon.hidden == False:
                    x_move -= Simon.vel
                    Simon.left = True
                    pygame.mixer.Sound.play(footSteps)

                if event.key == pygame.K_d and Simon.x < 1360 - Simon.width and Simon.hidden == False:
                    x_move += Simon.vel
                    Simon.right = True
                    pygame.mixer.Sound.play(footSteps)

                if event.key == pygame.K_RETURN:
                    door.use(Simon,B1,25,False,1020)
                
                if event.key == pygame.K_e:
                    Simon.invDisplay()
                    
                if event.key == pygame.K_DOWN and Simon.hidden == True:
                    Simon.hidden = False
                    
                if event.key == pygame.K_w and Simon.y > 340 and Simon.hidden == False:
                    y_move -= Simon.vel
                    
                if event.key == pygame.K_s and Simon.y < 520 and Simon.hidden == False:
                    y_move += Simon.vel

    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d: 
                    x_move = 0
                    Simon.left = False
                    Simon.right = False
                    pygame.mixer.Sound.stop(footSteps)
                    
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    y_move = 0
                

        Simon.x += x_move
        Simon.y += y_move
        Simon.boundary(B1)        

        B1.scrollBg(Simon.x + Simon.width,Simon)
        blitObject(B1.sprite, (B1.x,0))

        blitObject(doorSprite, (door.x,door.y))

            
        if Simon.hidden == False:

            if Simon.walkCount + 1 >= 120:
                Simon.walkCount = 0

            if Simon.left == True:
                gameDisplay.blit(walkLeft[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
                
            elif Simon.right == True:
                gameDisplay.blit(walkRight[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
            else:
                blitObject(player_sprite, (Simon.x,Simon.y))
            
        pygame.display.update()
        
def study(Simon,xEntry,leftSide,bgPos):

    running = True

    Simon.x = 0

    B1 = Background(1360,720,0, studyBg)

    desk1 = Desk(500,450,"Dialogue/TheLastTest.txt")

    door = Door(15,162,room3,False)
    
    x_move = 0
    y_move = 0

    
    while running:

        clock.tick(120)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()



            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    global paused
                    paused = True
                    pause_screen()
                    
                if event.key == pygame.K_a and Simon.x > Simon.vel and Simon.hidden == False:
                    x_move -= Simon.vel
                    Simon.left = True
                    pygame.mixer.Sound.play(footSteps)

                if event.key == pygame.K_d and Simon.x < 1360 - Simon.width and Simon.hidden == False:
                    x_move += Simon.vel
                    Simon.right = True
                    pygame.mixer.Sound.play(footSteps)

                if event.key == pygame.K_RETURN:
                    door.use(Simon,B1,25,False,420)

                    desk1.noteRead(Simon.x,Simon.y,B1)
                
                if event.key == pygame.K_e:
                    Simon.invDisplay()
                    
                if event.key == pygame.K_DOWN and Simon.hidden == True:
                    Simon.hidden = False
                    
                if event.key == pygame.K_w and Simon.y > 340 and Simon.hidden == False:
                    y_move -= Simon.vel
                    
                if event.key == pygame.K_s and Simon.y < 520 and Simon.hidden == False:
                    y_move += Simon.vel

    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d: 
                    x_move = 0
                    Simon.left = False
                    Simon.right = False
                    pygame.mixer.Sound.stop(footSteps)
                    
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    y_move = 0
                

        Simon.x += x_move
        Simon.y += y_move
        Simon.boundary(B1)        

        B1.scrollBg(Simon.x + Simon.width,Simon)
        blitObject(B1.sprite, (B1.x,0))

        blitObject(doorSprite, (door.x,door.y))
        blitObject(deskBigSprite, (desk1.x,desk1.y))

            
        if Simon.hidden == False:

            if Simon.walkCount + 1 >= 120:
                Simon.walkCount = 0

            if Simon.left == True:
                gameDisplay.blit(walkLeft[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
                
            elif Simon.right == True:
                gameDisplay.blit(walkRight[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
            else:
                blitObject(player_sprite, (Simon.x,Simon.y))
            
        pygame.display.update()

def bedroom(Simon,xEntry,leftSide,bgPos):

    running = True

    Simon.x = 0

    B1 = Background(1360,720,0, bedroomBg)

    key = item("key", keySprite)
    safe1 = Safe(1200,450)

    door = Door(15,162,room3,False)
    
    x_move = 0
    y_move = 0

    
    
    while running:

        clock.tick(120)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    global paused
                    paused = True
                    pause_screen()
                    
                if event.key == pygame.K_a and Simon.x > Simon.vel and Simon.hidden == False:
                    x_move -= Simon.vel
                    Simon.left = True
                    pygame.mixer.Sound.play(footSteps)

                if event.key == pygame.K_d and Simon.x < 1360 - Simon.width and Simon.hidden == False:
                    x_move += Simon.vel
                    Simon.right = True
                    pygame.mixer.Sound.play(footSteps)

                if event.key == pygame.K_RETURN:
                    
                    door.use(Simon,B1,25,False,1020)

                    safe1.unlock(Simon.x,Simon.y)

                    if safe1.locked == False and safe1.empty == False:
                        #send message that you pikced up key and found a note
                        Simon.pickUp(safe1.x + B1.x,safe1.y, key.name, key.sprite)
                        safe1.empty = True
                
                if event.key == pygame.K_e:
                    Simon.invDisplay()
                    
                if event.key == pygame.K_DOWN and Simon.hidden == True:
                    Simon.hidden = False
                    
                if event.key == pygame.K_w and Simon.y > 340 and Simon.hidden == False:
                    y_move -= Simon.vel
                    
                if event.key == pygame.K_s and Simon.y < 520 and Simon.hidden == False:
                    y_move += Simon.vel

    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d: 
                    x_move = 0
                    Simon.left = False
                    Simon.right = False
                    pygame.mixer.Sound.stop(footSteps)
                    
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    y_move = 0
                

        Simon.x += x_move
        Simon.y += y_move
        Simon.boundary(B1)        

        B1.scrollBg(Simon.x + Simon.width,Simon)
        blitObject(B1.sprite, (B1.x,0))

        blitObject(doorSprite, (door.x,door.y))
        blitObject(safeSprite, (safe1.x,safe1.y))

            
        if Simon.hidden == False:

            if Simon.walkCount + 1 >= 120:
                Simon.walkCount = 0

            if Simon.left == True:
                gameDisplay.blit(walkLeft[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
                
            elif Simon.right == True:
                gameDisplay.blit(walkRight[Simon.walkCount//30], (Simon.x,Simon.y))
                Simon.walkCount += 1
            else:
                blitObject(player_sprite, (Simon.x,Simon.y))
            
        pygame.display.update()


def main():
    beginning(Simon)
