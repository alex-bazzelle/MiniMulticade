#pokemon!!!
import pygame
import os
from time import sleep
from random import randint

DEBUG = False
activePOKEMON = True
###############################################################
#  TODO:
# - redraw move box
# - redraw platforms
# - player can change pokemon at end of battle and restart the battle
###############################################################




pygame.init() #initialize pygame


assetPath = "Project/Pokemon" #path for all of the images

#quality of life
width = 1024 #width of the screen
height = 600 #height of the screen
clock = pygame.time.Clock() #clock for managing framerate
screen = pygame.display.set_mode((width, height),0,32) #give you a screen to play on
def image(value:str): #function to add the directory to image file names
	return os.path.join(assetPath,value)
def getCenter(thing,dx=0,dy=0): #get the center of objects. dx and dy are to change it
	return width/2-(thing.get_width()/2)+dx, height/2-(thing.get_height()/2)+dy
fontLarge = pygame.font.Font(image("pokeFont.ttf"),12) #big boy font
fontSmall = pygame.font.Font(image("pokeFont.ttf"),10) #small boy font
fontExtraLarge = pygame.font.Font(image("pokeFont.ttf"),48) #biggest boy font

#window
pygame.display.set_caption("TechyMon") #window title
pygame.display.set_icon(pygame.image.load(image("pokeball.png"))) #window icon



#TEXT WRAPPING
def textWrap(string:str, maxLength:int):
    words = string.split() #split string into words
    lines = [] #list of lines
    line = "" #individual lines
    for word in words:
        if(len(line + word)>=maxLength): #first, check if you can add a word
            lines.append(line) #if not, the line is done.
            line = "" #reset line.

        line += (word + " ") #add word to line

    lines.append(line) #add the last line to the lines

    return lines #a list of strings. each string is, a most, the specified max length

##############
#---LAYOUT---#
##############
class HealthBar():
    def __init__(self,xPos,yPos):
        self.image = pygame.image.load(image("healthbar.png"))
        self.x = xPos
        self.y = yPos

class StaticBackground():
    def __init__(self):
        self.textBar = pygame.image.load(image("blankbg.png"))
        self.menuBar = pygame.image.load(image("textbg.png"))
        self.moveBar = pygame.image.load(image("movebg.png"))
        self.bottomBar = self.menuBar
        healthBar = pygame.image.load(image("healthbar.png"))
        self.playerHealthBar = HealthBar(width-healthBar.get_width(), height-self.bottomBar.get_height()-healthBar.get_height())
        self.opponentHealthBar = HealthBar(0, healthBar.get_height()-healthBar.get_height()/2)
        self.platformOpponent = pygame.image.load(image("platformOpponent.png"))
        self.platformPlayer = pygame.image.load(image("platformPlayer.png"))
        self.opponentPokemon = pygame.image.load(image("ladyMist.png"))
        self.playerPokemon = pygame.image.load(image("techy.png"))
    def update(self):
        screen.blit(self.bottomBar,(0,height-self.bottomBar.get_height()))
        screen.blit(self.playerHealthBar.image,(self.playerHealthBar.x,self.playerHealthBar.y))
        screen.blit(self.opponentHealthBar.image,(self.opponentHealthBar.x,self.opponentHealthBar.y))
        screen.blit(self.platformOpponent,getCenter(self.platformOpponent,width/4,-height/7))
        screen.blit(self.platformPlayer,(145,height-self.bottomBar.get_height()-self.platformPlayer.get_height()))
        #screen.blit(self.opponentPokemon,getCenter(self.opponentPokemon,width/4,-height/4))
        #screen.blit(self.playerPokemon,(145+self.platformPlayer.get_width()/2-self.playerPokemon.get_width()/2,height-self.bottomBar.get_height()-self.playerPokemon.get_height()))
    
    def setMenu(self):
        self.bottomBar = self.menuBar
    def setText(self):
        self.bottombar = self.textBar
    def setMoves(self):
        self.bottombar = self.moveBar
bg = StaticBackground()

healthBars = [bg.playerHealthBar,bg.opponentHealthBar]




class characterSelect():
    def __init__(self):
        self.techy = [pygame.image.load(image("charTechy1.png")),pygame.image.load(image("charTechy2.png"))]
        self.ladyMist = [pygame.image.load(image("charLadyMist1.png")),pygame.image.load(image("charLadyMist2.png"))]
        self.image = self.techy[0]
        self.hover = "techy"
        self.delay = 0
        self.maxDelay = 20
        self.text = fontExtraLarge.render("Select Your Starter",True,(0,0,0))
    def update(self):
        if(self.delay>self.maxDelay):
            if(self.hover == "techy" and self.image == self.techy[0]): self.image = self.techy[1]
            elif(self.hover == "techy"): self.image = self.techy[0]
            elif(self.hover == "ladyMist" and self.image == self.ladyMist[0]): self.image = self.ladyMist[1]
            elif(self.hover == "ladyMist"): self.image = self.ladyMist[0]
            self.delay = 0

        self.delay += 1

        screen.blit(self.image,(0,0))
        screen.blit(self.text,getCenter(self.text,0,height/2-self.text.get_height()))
        

introbg = characterSelect()

##############
#----MOVE----#
##############
class MonMove():
    def __init__(self,title="moveName",type="moveType",desc="moveDesc",pp=20,accuracy=100,power=10):
        self.title = title
        self.type = type
        self.desc = desc
        self.totalPP = pp
        self.currentPP = pp
        self.accuracy = accuracy
        self.power = power
        
#MOVE BANK
drool = MonMove("Drool","normal","Splashes drool onto opponent, dealing lingering damage for 3 turns.",20,70,5)
offering = MonMove("Offering","normal","Give Techy an offering, increasing his attack by 20 percent.",4,100,0)
goodNap = MonMove("Good Nap","normal","Takes a nap, healing HP.",10,100,10)
goDawgs = MonMove("Go Dawgs","normal","Bark at the opponent while making the bulldog hand symbol.",20,90,10)
sealStep = MonMove("Seal Step","normal","Cuts the opponent's health in half.",5,40,50)
squirt = MonMove("Squirt","water","Blast the opponent with a mist of cold water.",20,100,8)
meditation = MonMove("Meditation","psychic","Meditates for two turns, healing a large amount of HP.",5,100,30)

damagingMoves = [drool,goDawgs,sealStep,squirt]
healingMoves = [goodNap,meditation]


##############
#----MONS----#
##############
class Pokemon():
    def __init__(self,name="MISSINGNO",front="pokeball.png",back="pokeball.png",owner="player",frames=[HealthBar(0,0),HealthBar(0,0)]):
        self.name = name
        self.front = pygame.image.load(image(front))
        self.back = pygame.image.load(image(back))
        self.owner = owner
        self.lvl = 24
        self.frames = frames

        self.title = fontLarge.render("{}    Lvl {}".format(self.name,self.lvl),True,(0,0,0))
        
        if(self.owner == "player"):
            self.image = self.back
            self.pos = (145+bg.platformPlayer.get_width()/2-self.image.get_width()/2,height-bg.bottomBar.get_height()-self.image.get_height())
            self.frame = self.frames[0]
        if(self.owner == "opponent"):
            self.image = self.front
            self.pos = getCenter(self.image,width/4,-height/4)
            self.frame = self.frames[1]

        self.totalHP = 100
        self.currentHP = 100
        self.hpBar = pygame.Rect(0,0,196*2,14*2)
        self.hpBar.left = self.frame.x+(4*2)
        self.hpBar.top = self.frame.y+(26*2)

        self.hpText = fontSmall.render("{}/{}".format(self.currentHP,self.totalHP),True,(0,0,0))

        self.status = [False,False]
        self.statusDuration = [0,0]

        self.moves = [MonMove(),MonMove(),MonMove(),MonMove()]
    def update(self):
        screen.blit(self.image,self.pos)

        if(self.status[0]==False): self.statusDuration[0] = 0
        if(self.status[1]==False): self.statusDuration[1] = 0
        if(self.statusDuration[0]<=0): self.status[0] = False
        if(self.statusDuration[1]<=0): self.status[1] = False

        #hp bar
        if(self.currentHP/self.totalHP < 0.2): pygame.draw.rect(screen,(255,128,128),self.hpBar) #red
        elif(self.currentHP/self.totalHP < 0.5): pygame.draw.rect(screen,(255,255,128),self.hpBar) #yellow
        else: pygame.draw.rect(screen,(148,255,128),self.hpBar) #green

        #mon name
        screen.blit(self.title,(self.hpBar.left,self.hpBar.top-10-self.title.get_height()))

        #current hp
        if(self.owner=="player"):
            self.hpText = fontSmall.render("{}/{}".format(self.currentHP,self.totalHP),True,(0,0,0))
            screen.blit(self.hpText,(self.hpBar.left+(192*2)-self.hpText.get_width(),self.hpBar.top-10-self.hpText.get_height()))
    
    def updateHealth(self,deltaHP):
        self.currentHP += deltaHP
        if(self.currentHP<0): self.currentHP=0 #min hp is 0
        if(self.currentHP>self.totalHP): self.currentHP = self.totalHP #max hp
        if(self.currentHP>0): self.hpBar.width = (196*2)*((self.currentHP)/self.totalHP) #only draw hp if you have hp
        else: self.hpBar.width = 0
    
    def makePlayer(self):
        self.owner = "player"
        self.image = self.back
        self.pos = (145+bg.platformPlayer.get_width()/2-self.image.get_width()/2,height-bg.bottomBar.get_height()-self.image.get_height())
        self.frame = self.frames[0]
        self.hpBar.left = self.frame.x+(4*2)
        self.hpBar.top = self.frame.y+(26*2)
        return self
    def makeOpponent(self):
        self.owner = "opponent"
        self.image = self.front
        self.pos = getCenter(self.image,width/4,-height/4)
        self.frame = self.frames[1]
        self.hpBar.left = self.frame.x+(4*2)
        self.hpBar.top = self.frame.y+(26*2)
        return self
        


techy = Pokemon("TECHY","techyFront.png","techyBack.png","player",healthBars)
techy.moves = [drool,offering,goodNap,goDawgs]

ladyMist = Pokemon("LADY MIST","ladyMist.png","ladyMistBack.png","opponent",healthBars)
ladyMist.moves = [sealStep,squirt,meditation,goDawgs]

playerMon = ladyMist.makePlayer()
oppMon = techy.makeOpponent()


def performMove(move:MonMove,user=playerMon,victim=oppMon):
    global missed
    if(move.accuracy>randint(0,99) and move.currentPP>0 and not user.status[1]):
        match move.title:
            case "Drool":
                victim.status[0] = True #acid
                victim.statusDuration[0] = 3
                victim.updateHealth(-int((move.power*(1+user.lvl/100))))
            case "Offering":
                for m in user.moves:
                    if(m.power > 0): m.power = int(m.power*1.20)
            case "Good Nap":
                user.updateHealth(move.power)
            case "Seal Step":
                victim.updateHealth(-int(victim.currentHP/2))
            case "Meditation":
                user.status[1] = True #asleep
                user.statusDuration[1] = 2
            case _: #other moves (Squirt and Go Dawgs)
                victim.updateHealth(-int((move.power*(1+user.lvl/100))))
        move.currentPP -= 1
        missed = False
    else:
        missed = True

    return "{} used {}!".format(user.name,move.title)

def opponentTurn(move:MonMove,user=oppMon,victim=playerMon):
    return performMove(move,user,victim)



##############
#----TEXT----#
##############
class MainText():
    def __init__(self):
        self.words = ""
        self.goal = "Sample Text"
        self.textbox = fontLarge.render(self.words,False,(0,0,0),(255,255,255))
        self.x = 20
        self.y = height-bg.bottomBar.get_height()+30
    def update(self):
        if(self.words!=self.goal): self.words = self.newText() #if not at goal phrase, add a letter
        self.textbox = fontLarge.render("{}".format(self.words),False,(0,0,0),None)
        screen.blit(self.textbox,(self.x,self.y))
    def newText(self):
        strLen = len(list(self.goal))
        wrdLen = len(list(self.words))
        if(wrdLen<strLen): #ensures that, in case something fucks up, this will eventually stop adding text
            self.words += list(self.goal)[wrdLen]
            return self.words
        else: return "ERROR: SOMETHING WENT INCREDIBLY WRONG"
    def setText(self,newText="Sample Text"):
        self.words = ""
        self.goal = newText
        sleep(0.25)
text = MainText()



##############
#---CLICKS---#
##############
class Pointer():
    def __init__(self):
        self.stages = [pygame.image.load(image("pointerWhite.png")),pygame.image.load(image("pointerBlack.png"))]
        self.image = self.stages[0]

        self.show = True

        self.blinkDelay = 20

        self.menuPos()
        self.pos = self.tl
    def update(self):
        if(self.blinkDelay<0):
            if(self.image == self.stages[0]): self.image=self.stages[1]
            else: self.image=self.stages[0]
            self.blinkDelay=20
        if(self.show): screen.blit(self.image,self.pos)
        self.blinkDelay -= 1
    def moveLeft(self):
        if(self.pos == self.tr): self.pos = self.tl
        elif(self.pos == self.br): self.pos = self.bl
    def moveRight(self):
        if(self.pos == self.tl): self.pos = self.tr
        elif(self.pos == self.bl): self.pos = self.br
    def moveUp(self):
        if(self.pos == self.bl): self.pos = self.tl
        elif(self.pos == self.br): self.pos = self.tr
    def moveDown(self):
        if(self.pos == self.tr): self.pos = self.br
        elif(self.pos == self.tl): self.pos = self.bl
    
    def menuPos(self):
        self.show = True
        self.tl = (width/8*4+90-self.image.get_width(), height/9*7-20) #top left
        self.tr = (width/8*4+280, height/9*7-20) #top right
        self.bl = (width/8*4+90-self.image.get_width(), height/9*7-30+(self.image.get_height()*2)) #bottom left
        self.br = (width/8*4+280, height/9*7-30+(self.image.get_height()*2)) #bottom right
    def movePos(self):
        self.show = True
        self.tl = ((10*2),height/9*7-20)
        self.tr = ((125*2), height/9*7-20) #top right
        self.bl = ((10*2), height/9*7-30+(self.image.get_height()*2)) #bottom left
        self.br = ((125*2), height/9*7-30+(self.image.get_height()*2)) #bottom right

pointer = Pointer()



##############
#----SLOT----#
##############
class SlotText():
    def __init__(self,position=0):
        self.words = "slot"
        self.position = position
        self.textbox = fontLarge.render(self.words,False,(0,0,0),None)
        self.menuPos()
    def update(self):
        self.textbox = fontLarge.render(self.words,False,(0,0,0),None)
        screen.blit(self.textbox,self.pos)
    def movePos(self):
        match self.position:
            case 0: self.pos = (35*2,height/9*7)
            case 1: self.pos = (150*2,height/9*7)
            case 2: self.pos = (35*2,height-30*2)
            case 3: self.pos = (150*2,height-30*2)
    def menuPos(self):
        match self.position:
            case 0: self.pos = (width/8*4+120, height/9*7) #top left
            case 1: self.pos = (width/8*6+100, height/9*7) #top right
            case 2: self.pos = (317*2, height-30*2) #bottom left
            case 3: self.pos = (width/8*6+100, height-30*2) #bottom right

slots = [SlotText(0),SlotText(1),SlotText(2),SlotText(3),"Menu"]
def updateSlots(slots:list):
    for i in range(0,4): slots[i].update()


def setMenu(slots:list):
    #bg.bottomBar = bg.menuBar

    bg.setMenu()
    pointer.menuPos()
    pointer.pos = pointer.tl

    slots[0].words = "Moves"
    slots[1].words = "TODO" #pokemon
    slots[2].words = "TODO" #items
    slots[3].words = "Exit"
    slots[4] = "Menu"
    for i in range(0,4): slots[i].menuPos()

def setMoves(slots:list):

    bg.bottomBar = bg.moveBar
    pointer.movePos()
    pointer.pos = pointer.tl
    text.setText("")

    for i in range(0,4):
        slots[i].words = playerMon.moves[i].title
    slots[4] = "Moves"
    for i in range(0,4): slots[i].movePos()

def setBlank(slots:list):
    bg.bottomBar = bg.textBar
    pointer.show = False

    for i in range(0,4): slots[i].words = ""
    slots[4] = "Blank"

#show move info on side
def showMoveInfo():
    match pointer.pos:
        case pointer.tl: move = playerMon.moves[0]
        case pointer.tr: move = playerMon.moves[1]
        case pointer.bl: move = playerMon.moves[2]
        case pointer.br: move = playerMon.moves[3]
    screen.blit(fontSmall.render(getMoveInfo(move),True,(0,0,0)),(287*2,220*2))

    words = textWrap(move.desc,len(getMoveInfo(move)))
    for word in words:
        screen.blit(fontSmall.render("{}".format(word),True,(0,0,0)),(287*2,240*2+(fontSmall.get_height()*words.index(word))))

    

def getMoveInfo(move:MonMove):
    powerPoints = "PP: {}/{}".format(move.currentPP,move.totalPP)
    power = "Power: {}".format(move.power)
    accuracy = "Accuracy: {}".format(move.accuracy)
    return "{}    {}    {}".format(powerPoints,power,accuracy)

setMenu(slots)




#################################################################################
####--------------------------------GAME LOOP--------------------------------####
#################################################################################
stage = 0 #the phase of the game (player turn, opp turn, etc)
cooldown = 0 #tracks time spent on each stage
minCD = 30 #min time spent on each stage
currentMove = MonMove() #the current move being used
missed = False
intro = True




while(activePOKEMON):
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                print("\n\n GAME QUIT \n\n")
                exit()
            case _:
                pass
    keys = pygame.key.get_pressed()

    if(intro):
        #intro=False
        if(keys[pygame.K_a]): introbg.hover = "techy"
        if(keys[pygame.K_d]): introbg.hover = "ladyMist"

        if(keys[pygame.K_SPACE]):
            if(introbg.hover == "techy"):
                playerMon = techy.makePlayer()
                oppMon = ladyMist.makeOpponent()
            if(introbg.hover == "ladyMist"):
                playerMon = ladyMist.makePlayer()
                oppMon = techy.makeOpponent()
            intro = False





        pygame.display.flip()
        clock.tick(60)
        screen.fill((200,200,200)) #default bg color is light gray.
        introbg.update()
        



    if(not intro):
        if(stage == 0): #player selects move
            if(cooldown==0):
                text.setText("What will {} do?".format(playerMon.name))
                setMenu(slots)
                
            cooldown += 1


            keys = pygame.key.get_pressed()
            if(keys[pygame.K_w]): pointer.moveUp()
            if(keys[pygame.K_a]): pointer.moveLeft()
            if(keys[pygame.K_d]): pointer.moveRight()
            if(keys[pygame.K_s]): pointer.moveDown()


            if(keys[pygame.K_SPACE] and cooldown>50):
                match pointer.pos:
                    case pointer.tl:
                        if(slots[-1]=="Menu"): setMoves(slots); sleep(0.25) #moves
                        elif(slots[-1]=="Moves"): currentMove = playerMon.moves[0]; stage=1; cooldown=0
                    case pointer.tr:
                        if(slots[-1]=="Menu"): text.setText("Pokemon List"); sleep(0.25) #pokemon
                        elif(slots[-1]=="Moves"): currentMove = playerMon.moves[1]; stage=1; cooldown=0
                    case pointer.bl:
                        if(slots[-1]=="Menu"): print("items"); sleep(0.25) #items
                        elif(slots[-1]=="Moves"): currentMove = playerMon.moves[2]; stage=1; cooldown=0
                    case pointer.br:
                        if(slots[-1]=="Menu"): pygame.quit(); exit() #exit
                        elif(slots[-1]=="Moves"): currentMove = playerMon.moves[3]; stage=1; cooldown=0
                    case _: print("\n\nERROR: Pointer is in unknown position {}!!\n\n".format(pointer.pos))
            if(keys[pygame.K_ESCAPE]): setMenu(slots)

            if(slots[-1]=="Moves"): showMoveInfo()
            
        if(stage == 1): #player performs move
            if(cooldown == 0):
                if(currentMove.currentPP<=0): stage = 0 #if you don't have pp
                    
                else: #if you do have PP
                    text.setText(performMove(currentMove,playerMon,oppMon))
                    if(missed): text.setText("{} missed!".format(currentMove.title))
                    elif(playerMon.status[1]): text.setText("{} is asleep.".format(playerMon.name))
                    missed = False
                    setBlank(slots)
                
            cooldown += 1

            keys = pygame.key.get_pressed()
            if(keys[pygame.K_SPACE] and cooldown>minCD):
                if(currentMove in healingMoves): stage = 6
                else: stage = 2
                #lose conditions
                if(playerMon.currentHP <= 0): stage = 98; cooldown = 0
                if(oppMon.currentHP <= 0): stage = 99; cooldown = 0
                cooldown = 0
        
        if(stage == 2): #opponent performs move
            
            if(cooldown==0):
                if(oppMon.status[1]): #asleep
                    text.setText("{} is asleep.".format(oppMon.name))
                else:
                    currentMove = None
                    while currentMove==None:
                        n = randint(0,3) #ensure move has pp
                        if(oppMon.moves[n].currentPP>0): currentMove = oppMon.moves[n]
                    text.setText(opponentTurn(currentMove,oppMon,playerMon))

            cooldown += 1

            if(keys[pygame.K_SPACE] and cooldown>minCD):
                stage = 3
                #lose conditions
                if(playerMon.currentHP <= 0): stage = 98; cooldown = 0
                if(oppMon.currentHP <= 0): stage = 99; cooldown = 0
                cooldown = 0
        
        if(stage == 3): #player takes damage


            if(cooldown == 0):
                if(missed):
                    text.setText("{} missed!".format(currentMove.title))
                    missed = False
                else:
                    if(currentMove in damagingMoves):
                        if(currentMove == sealStep): text.setText("{}'s HP was cut in half.".format(playerMon.name))
                        else: text.setText("{} took {}HP damage.".format(playerMon.name,int(currentMove.power*(1+oppMon.lvl/100))))
                    elif(currentMove in healingMoves):
                        if(currentMove == meditation): text.setText("{} fell asleep.".format(oppMon.name))
                        else: text.setText("{} healed some HP.".format(oppMon.name))
                    else: cooldown = 998

            cooldown += 1

            if((keys[pygame.K_SPACE] and cooldown>minCD) or cooldown == 999):
                if(True in playerMon.status): stage = 4
                elif(True in oppMon.status): stage = 5
                else: stage = 0; playerMon.status = [False,False]; oppMon.status = [False,False]
                cooldown = 0
        
        if(stage == 4): #player has status effect
            if(cooldown == 0):
                if(playerMon.status[0]): #acid
                    if(playerMon.currentHP>=5): damage = 5
                    else: damage = playerMon.currentHP
                    playerMon.statusDuration[0] -= 1
                    text.setText("{} took {}HP damage from the drool! Drool ends in {} turn(s).".format(playerMon.name,damage,playerMon.statusDuration[0]))
                    playerMon.updateHealth(-5)
                if(playerMon.status[1]): #asleep
                        playerMon.statusDuration[1] -= 1
                        if(playerMon.statusDuration[1]==0):
                            if(playerMon.currentHP+30<=playerMon.totalHP): damage = 30
                            else: damage = playerMon.totalHP - playerMon.currentHP
                            playerMon.updateHealth(damage)
                            text.setText("{} woke up and healed {}HP!".format(playerMon.name,damage))
                        else: text.setText("{} will wake up in {} turn(s)".format(playerMon.name,playerMon.statusDuration[1]))
            
            cooldown += 1

            if(keys[pygame.K_SPACE] and cooldown>minCD):
                if(True in oppMon.status): stage = 5
                else: stage = 0
                cooldown = 0

        if(stage == 5): #opponent has status effect
            if(cooldown == 0):
                if(oppMon.status[1]): #asleep
                        oppMon.statusDuration[1] -= 1
                        if(oppMon.statusDuration[1]==0):
                            if(oppMon.currentHP+30<=oppMon.totalHP): damage = 30
                            else: damage = oppMon.totalHP - oppMon.currentHP
                            oppMon.updateHealth(damage)
                            text.setText("{} woke up and healed a lot of HP!".format(oppMon.name))
                        else: text.setText("{} will wake up in {} turn(s)".format(oppMon.name,oppMon.statusDuration[1]))
                if(oppMon.status[0]): #acid
                    if(oppMon.currentHP>=5): damage = 5
                    else: damage = oppMon.currentHP
                    oppMon.statusDuration[0] -= 1
                    text.setText("{} took damage from the drool! Drool ends in {} turn(s).".format(oppMon.name,oppMon.statusDuration[0]))
                    oppMon.updateHealth(-5)
            
            cooldown += 1

            if(keys[pygame.K_SPACE] and cooldown>minCD):
                stage = 0
                if(oppMon.status == [True,True]): stage = 5.5
                cooldown = 0
        
        if(stage == 5.5): #opp is both asleep and drooled
            if(cooldown == 0):
                if(oppMon.statusDuration[1]==0): text.setText("{} woke up and healed a lot of HP!".format(oppMon.name))
                else: text.setText("{} will wake up in {} turn(s)".format(oppMon.name,oppMon.statusDuration[1]))

            cooldown += 1
            
            if(keys[pygame.K_SPACE] and cooldown>minCD):
                stage = 0
                cooldown = 0


        if(stage == 6): #player used a healing move
            if(cooldown == 0):
                text.setText("{} healed {}HP".format(playerMon.name,currentMove.power))
            cooldown += 1
            
            if(keys[pygame.K_SPACE] and cooldown>minCD):
                stage = 2
                cooldown = 0


        

        if(stage==98): #player loses
            if(cooldown==0):
                bg.bottomBar = bg.textBar
                text.setText("{} fainted!".format(playerMon.name))

            cooldown += 1
        if(stage==99): #opponent loses
            if(cooldown==0):
                bg.bottomBar = bg.textBar
                text.setText("{} fainted!".format(oppMon.name))

            cooldown += 1
            


        #################################################################################
        ####----------------------------------RENDER---------------------------------####
        #################################################################################
        pygame.display.flip()
        clock.tick(60)
        screen.fill((200,200,200)) #default bg color is light gray.
        bg.update()
        text.update()
        updateSlots(slots)
        pointer.update()
        playerMon.update()
        oppMon.update()