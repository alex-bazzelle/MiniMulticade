import pygame
from random import randint
import math
import os

DEBUG = False

pygame.init() #initialize pygame
assetPath = "Project/Doodle Jump" #path for all of the images

#quality of life
width = 1024 #width of the screen
height = 600 #height of the screen
clock = pygame.time.Clock() #clock for managing framerate
screen = pygame.display.set_mode((width, height),0,32) #give you a screen to play on
fontLarge = pygame.font.Font(None,64) #big boy font
fontSmall = pygame.font.Font(None,32) #small boy font
def image(value): #function to add the directory to image file names
	return os.path.join(assetPath,value)
def getCenter(thing,dx=0,dy=0): #get the center of objects. dx and dy are to change it
	return width/2-(thing.get_width()/2)+dx, height/2-(thing.get_height()/2)+dy

#window
pygame.display.set_caption("Doodle Jump") #window title
pygame.display.set_icon(pygame.image.load(image("jumpDude.png"))) #window icon

##############
#-BACKGROUND-#
##############
class Background():
	def __init__(self): #make the background
		self.playing = pygame.image.load(image("graph bg.png")) #background image
		self.gameOver = pygame.image.load(image("gameOver.png")) #gameover image
		self.image = self.playing #start with playing
		self.x, self.y = 0,0 #plop it in the top right
		screen.blit(self.image,(self.x,self.y)) #show it!
		self.scroll = 0 #some scrolling
		self.tiles = math.ceil(height / self.image.get_height()) + 2 #some tiles for scrolling
	def update(self,focusY=0): #focus is what it scrolls based on
		for i in range(0,self.tiles): #three tiles
			screen.blit(self.image, (0,(self.image.get_height()*i+self.scroll)-height)) #show those tiles
		self.scroll += focusY #change center tile position
		if(abs(self.scroll)>self.image.get_height()): self.scroll = 0 #loop tiles
bg = Background()


##############
#PAUSE SCREEN#
##############
class Pause():
	def __init__(self):
		self.blank = pygame.image.load(image("pausedBlank.png"))
		self.buttonPos = self.blank.get_width()/4
		self.resume = pygame.image.load(image("resume.png"))
		self.resumePos = getCenter(self.resume,-1*self.buttonPos,40)
		self.exit = pygame.image.load(image("exit.png"))
		self.exitPos = getCenter(self.exit,self.buttonPos,40)
		self.overlay = pygame.image.load(image("selectOverlay.png"))
		self.selected = "resume"

		self.cooldown = 0
	def update(self):
		screen.blit(self.blank, getCenter(self.blank))
		screen.blit(self.resume,(self.resumePos))
		screen.blit(self.exit,(self.exitPos))
		if(self.selected == "resume"): screen.blit(self.overlay,self.resumePos)
		if(self.selected == "exit"): screen.blit(self.overlay,self.exitPos)
		if(DEBUG): print("pause update")
	
	def cooldownReset(self):
		self.cooldown = 200

pauseScreen = Pause()
##############
#---JUMPER---#
##############
class Jumper(pygame.sprite.Sprite):
	def __init__(self): #make the sprite
		pygame.sprite.Sprite.__init__(self) #it is a sprite
		self.right = pygame.image.load(image("jumpDude.png")) #load in the image
		self.left = pygame.image.load(image("jumpDudeL.png")) #load in the image
		self.image = self.right #looking right by default
		self.direction = 1 #looking right
		self.rect = self.image.get_rect() #give it a rect for collisions
		self.x, self.y = getCenter(self.image) #give it an x and y
		self.velX = 0 #velocity X
		self.velY = 0 #velocity Y
		self.otherY = 0 #if you can explain why this works, i'll give you a dollar
		self.currentPower = 0 #track powerups
		self.update() #update it :)
	def collisions(self,group): #shorthand for collisions
		return pygame.sprite.spritecollide(self,group,False)
	def update(self): #update every frame
		self.x += self.velX #update x
		if(self.y-self.velY>50): self.y += (self.velY)*-1 #update y

		if(self.velX>0): self.velX-=1; self.image=self.right; self.direction=1 #decrease velocity
		if(self.velX<0): self.velX+=1; self.image=self.left; self.direction=0 #so that you can stop

		if(self.x<5): self.x = 0 #stay in bounds (left)
		if(self.rect.right>width): self.x = width-self.rect.width #stay in bounds (right)

		self.rect.x, self.rect.y = self.x, self.y #update collision box
		screen.blit(self.image, (self.x,self.y)) #draw the dude
	def reset(self): #reset when you lose
		self.x, self.y = getCenter(self.image)
		self.velX = 0 #velocity X
		self.velY = 0 #velocity Y
		self.update()
guy = Jumper()

###############
#--POWER UPS--#
###############
class PowerUp(pygame.sprite.Sprite): #default powerup setup
	def __init__(self,spawnPlatform): #x is left side, y is bottom side
		pygame.sprite.Sprite.__init__(self) #it is a sprite
		self.platform = spawnPlatform
		self.image = pygame.image.load(image("missingTexture.png")) #no texture yet
		self.rect = self.image.get_rect() #give it a rect for collisions
		self.x = randint(spawnPlatform.rect.left,spawnPlatform.rect.right-self.rect.width) #x is on the new platform
		self.y = spawnPlatform.y - self.rect.height #y is on top of the new platform
		self.isActive = False
		self.isDying = False
	def update(self,focusY=0,focusRect=pygame.Rect(1,1,1,1),direction=1): #focusY is the jumper guy
		self.y += focusY #move it down when jumper moves up
		self.rect.x, self.rect.y = self.x, self.y #stupid collision stuff
		screen.blit(self.image, (self.x,self.y)) #show it on the screen
	def isCollide(self,focus):
		#default is collide is with feet
		if(focus.rect.bottom<self.rect.bottom and focus.rect.bottom>self.rect.top and focus.velY>0):
			return True
		else: return False
	def newImage(self,value):
		self.image = pygame.image.load(image(value))
		self.rect = self.image.get_rect()
		self.y = self.platform.y - self.rect.height

class Spring(PowerUp):
	def __init__(self,spawnPlatform):
		PowerUp.__init__(self,spawnPlatform) #make the powerup using superclass
		self.newImage("spring.png") #this is a spring
		self.rect = self.image.get_rect() #give it a rect for collisions
		self.stage = [self.image,pygame.image.load(image("springSquish.png"))]
		self.type = 2
		self.currentTime = 0 #not active at start
		self.activeTime = 50 #how long it's active.
	def update(self,focusY=0,focusRect=pygame.Rect(1,1,1,1),direction=1): #focusY is the jumper guy
		self.y += focusY #move it down when jumper moves up
		self.rect.x, self.rect.y = self.x, self.y #stupid collision stuff
		screen.blit(self.image, (self.x,self.y)) #show it on the screen
		if(self.isActive): self.active()
		if(self.isDying): self.dying()
	def active(self):
		self.image = self.stage[1]
		self.currentTime+=1
		if(self.currentTime>=self.activeTime):
			self.isActive = False
			self.isDying = True
	def dying(self):
		self.kill()

class Hat(PowerUp):
	def __init__(self,spawnPlatform): #x is left side, y is bottom side
		PowerUp.__init__(self,spawnPlatform) #make the powerup using superclass
		self.image = pygame.image.load(image("hat.png")) #this is a hat
		self.rect = self.image.get_rect() #give it a rect for collisions
		self.stage = [self.image,pygame.image.load(image("hatAnim/hatAnim1.png")),
						pygame.image.load(image("hatAnim/hatAnim2.png"))]
		self.type = 1 #track what type this is
		self.currentTime = 0 #not active at start
		self.activeTime = 100 #how long it's active. must be >50
	def update(self,focusY=0,focusRect=pygame.Rect(1,1,1,1),direction=1): #focusY is the jumper guy
		self.y += focusY #move it down when jumper moves up
		self.rect.x, self.rect.y = self.x, self.y #stupid collision stuff
		screen.blit(self.image, (self.x,self.y)) #show it on the screen
		if(self.isActive): self.active(focusRect,direction)
		if(self.isDying): self.dying()
	def isCollide(self,focus): #collides if hits head, not nose
		if(((focus.direction==1) and (focus.rect.right-26>self.rect.left)) or #guy looking right
     		((focus.direction==0) and (focus.rect.left+26<self.rect.right))): #guy looking left
			return True #a real collision :)
		else: return False #a fake collision >:(
	def active(self,focusRect,direction):
		#POSITION
		self.y = focusRect.y-self.rect.height #stay on head
		if(direction==1): self.x = focusRect.left #change x based on
		else: self.x = focusRect.right-self.rect.width #player direction
		#ANIMATION
		if(self.currentTime%2): self.image = self.stage[2]
		else: self.image = self.stage[1]
		#ENDING
		self.currentTime+=1
		if(self.currentTime>=self.activeTime):#time to stop
			self.isActive = False
			self.isDying = True
			self.image = self.stage[0]
			self.currentTime = self.activeTime-50 #die for 50 frames
	def dying(self):
		self.y += 10
		self.currentTime += 1
		if(self.currentTime >= self.activeTime):
			self.isDying = False
			self.kill()

	
def spawnPowerup(spawnPlatform):
	powerupTypes = ["hat","spring"] #pool of powerups to pick from
	currentType = powerupTypes[randint(0,len(powerupTypes)-1)] #the type for this powerup
	match currentType:
		case "hat": return Hat(spawnPlatform)
		case "spring": return Spring(spawnPlatform)
		case _: return PowerUp(spawnPlatform)


###############
#--PLATFORMS--#
###############

class Platform(pygame.sprite.Sprite): #main class for platforms
	def __init__(self,x=450,y=height-100): #default is bottom center of screen
		pygame.sprite.Sprite.__init__(self) #it's a sprite
		self.image = pygame.image.load(image("greenPlatform.png")) #load in the image
		self.rect = self.image.get_rect() #give it a rect for collisions
		self.startX, self.startY = x,y #gotta know how to reset it
		self.x, self.y = x,y #give it x and y
		self.isBroken = False #used for broken platforms
		self.isDead = False

		self.update() #make it happen!
	def update(self,focusY=0): #focusY is the jumper guy
		self.y += focusY #move it down when jumper moves up
		self.rect.x, self.rect.y = self.x, self.y #stupid collision stuff
		screen.blit(self.image, (self.x,self.y)) #show it on the screen
	def reset(self): #reset when you lose
		self.isBroken = False
		self.isDead = False
		self.y = self.startY #reset y
		self.x = self.startX #reset x
		self.rect.x, self.rect.y = self.x, self.y #stupid collision stuff
		screen.blit(self.image, (self.x,self.y)) #show it on the screen
class BrokenPlatform(Platform): #subclass for broken platforms
	def __init__(self,x=450,y=height-100): #same as normal platform
		Platform.__init__(self)
		self.image = pygame.image.load(image("brownPlatform.png"))
		self.rect = self.image.get_rect()
		self.startX, self.startY = x,y
		self.x, self.y = x,y
		#stages are the animation cycle
		self.stage = [self.image,pygame.image.load(image("BrPlatAnim/BrPlat1.png")),
						pygame.image.load(image("BrPlatAnim/BrPlat2.png")),
						pygame.image.load(image("BrPlatAnim/BrPlat3.png")),
						pygame.image.load(image("BrPlatAnim/BrPlat4.png")),
						pygame.image.load(image("BrPlatAnim/BrPlat5.png"))]
		
		self.update()
	def update(self,focusY=0):
		self.y += focusY
		self.rect.x, self.rect.y = self.x, self.y
		if(not self.isDead): screen.blit(self.image, (self.x,self.y))
		if(self.isBroken): self.removePlat() #if you break, do that action as well
	def removePlat(self): #when you break the platform
		index = self.stage.index(self.image) #find what stage it's at
		if(index<len(self.stage)-1): #if it isn't at the end stage
			self.image = self.stage[index+1] #increase the stage (aka next frame in animation)
			self.y+=10 #fall down
		else: self.isDead = True #if we're at the last stage, die

plats = pygame.sprite.Group() #group for all platforms


powers = pygame.sprite.Group() #group for all powerups
#SPAWNS PLATFORMS
def spawnPlatforms():
	#the default platforms. you always start the same way.
	plat1 = Platform(); plats.add(plat1)
	plat2 = Platform(600,400); plats.add(plat2)
	plat3 = Platform(300,200); plats.add(plat3)
	for i in range(0,100): #(makes 100 normal platforms + 30ish broken platforms)
		platY = -1*i*90 #the spacing between platforms
		newPlat = Platform(randint(0,width-plat1.rect.width),platY) #make platform
		plats.add(newPlat) #adds the platform

		# #LOGIC FOR POWERUP HAT
		if(randint(0,100)<10 and (len(powers.sprites())==0 or powers.sprites()[-1].y-500>newPlat.y)):
			#5% chance per plat, only if 500px away from last powerup
			newPU = spawnPowerup(newPlat) #make new power up on top of the new platform
			if(len(pygame.sprite.spritecollide(newPU,plats,False))==0): #if it isn't colliding with a platform
				powers.add(newPU)

		#LOGIC FOR BROKEN PLATFORMS
		if(randint(0,100)<30): # 30% chance to add a broken platform
			newPlat = BrokenPlatform(randint(0,width-plat1.rect.width),platY+randint(plat1.rect.height+20,200)) #randomize height
			if(len(pygame.sprite.spritecollide(newPlat,plats,False))==0): #if it isn't colliding with a platform
				plats.add(newPlat) #add it!
spawnPlatforms()
if(DEBUG): print("Highest (after spawning): {}".format(plats.sprites()[-1].y))

#RECYCLING PLATFORMS
def recyclePlatforms(lowPlat,highPlat):
	if(DEBUG): print("Highest platform: {}".format(highPlat.y))
	lowPlat.kill() #remove it from the group
	lowPlat.y = (highPlat.y-randint(90,110)) #y is the highest y value plus 90ish
	lowPlat.x = randint(0,width-lowPlat.rect.width) #x is anywhere
	lowPlat.isBroken = False #not broken
	lowPlat.update()
	#MAYBE SPAWN POWERUP ON IT?
	if(randint(0,100)<5 and not isinstance(plat,BrokenPlatform)): #5% chance for a power up to spawn with it
		newPU = spawnPowerup(lowPlat) #powerup is based on lowPlat
		powers.add(newPU) #add it to the set
	if(DEBUG): print("New highest: {}".format(lowPlat.y))
	return lowPlat

if(DEBUG): print("plat[0] y: {}\nplat[1] y: {}\nplat[-1] y: {}\n".format(plats.sprites()[0].y,plats.sprites()[1].y,plats.sprites()[-1].y))

###############
#----SCORE----#
###############
class Score(): #makes the score stuff easier
	def __init__(self):
		self.value = 0
		self.high = 0
		self.scoreText = fontSmall.render("Score: {}".format(self.value),True,(0,0,0),None)
		screen.blit(self.scoreText,(width-self.scoreText.get_width(),0))
	def update(self):
		if(self.value>self.high): self.high = self.value
		self.scoreText = fontSmall.render("Score: {}".format(self.value),True,(0,0,0),None)
		screen.blit(self.scoreText,(width-self.scoreText.get_width(),0))
	def reset(self):
		self.value = 0
score = Score()


#################################################################################
####--------------------------------GAME LOOP--------------------------------####
#################################################################################
alive = True
activePower = False
paused = False
while True:
	#always check if you want to quit
	for event in pygame.event.get(): #events
		match event.type:
			case pygame.QUIT:
				pygame.quit()
				print("\n\n\n GAME QUIT\n\n\n")
				exit()
			case _:
				pass

	if(alive and not paused):
	#################################################################################
	####----------------------------------INPUT----------------------------------####
	#################################################################################
		
		keys = pygame.key.get_pressed() #keys
		if(keys[pygame.K_a]): #LEFT KEY
			if(guy.x>0): guy.velX-=2 #move left, in bounds
			else: guy.velX = 0 #if out of bounds, stop
		if(keys[pygame.K_d]): #RIGHT KEY
			if((guy.x+guy.image.get_width())<width): guy.velX+=2 #move right, in bounds
			else: guy.velX = 0 #if out of bounds, stop
		if(keys[pygame.K_ESCAPE] and pauseScreen.cooldown<0):
			pauseScreen.cooldownReset()
			paused = True
			if(DEBUG): print("pause start")
		pauseScreen.cooldown -= 1


	#################################################################################
	####----------------------------------UPDATE---------------------------------####
	#################################################################################
		#POWERUPS
		activePower = False #default no powers
		for power in powers.sprites(): #see if any powers are active
			if(power.isActive and (not power.isDying)): guy.currentPower = power.type; activePower = True
		if(not activePower): guy.currentPower = 0 #if they aren't, unpower guy


		#FALLING
		if(guy.velY>=-10): guy.velY -= 0.5 #don't fall too fast, but always fall
		if(guy.currentPower == 1): guy.velY = 7 #hat powerup stops falling
		if(guy.currentPower == 2): guy.velY = 8 #spring

		#DEATH
		if(guy.rect.bottom>height):
			alive = False
			guy.x, guy.y = getCenter(guy.image)

		#COLLIDE
		#platform collide
		if(len(guy.collisions(plats))>0 and guy.velY<-1 and guy.y>50): #if collide with a platform, falling, and not at top
			for plat in guy.collisions(plats): #check that your feet are touching a platform
				if(guy.rect.bottom<plat.rect.bottom and guy.rect.bottom>plat.rect.top):
					if(isinstance(plat,BrokenPlatform)): #broken platform
						plat.isBroken = True #start broken animation
					elif(isinstance(plat,Platform)): #normal platform
						guy.velY = 10 #jump
		#powerup collide
		if(len(guy.collisions(powers))>0 and guy.y>50 and guy.currentPower == 0):
			#if touching a powerup, not at top, and no current powerup
			for power in guy.collisions(powers): #find the powerup being touched
				if(power.isCollide(guy) and (not power.isDying) and (not power.isActive)): #if powerup-specific collision conditions
					power.isActive = True #activate the powerup
					

		
		#SCORE
		if(int((plats.sprites()[0].y-guy.y)/10) > score.value): #score is determined by first platform
			score.value = int((plats.sprites()[0].y-guy.y)/10)

		#STAY ON SCREEN
		guy.otherY = guy.velY #i wish i knew why this works
		if(guy.y-guy.velY<100): #but sadly i do not
			guy.otherY+= 5
			guy.y+=1
		#if(DEBUG): print("Number of platforms: {}".format(len(plats.sprites())))

		#RECYCLE PLATFORMS
		if(plats.sprites()[1].y > 1000): #if a platform is way off screen
			plats.add(recyclePlatforms(plats.sprites()[1],plats.sprites()[-1])) #move it to the top
			if(DEBUG): print("After recycling, highest: {}\n".format(plats.sprites()[-1].y))

		
	#################################################################################
	####----------------------------------RENDER---------------------------------####
	#################################################################################
		pygame.display.flip()
		clock.tick(60)
		screen.fill((210,180,140)) #default bg color is tan.
		bg.update(guy.otherY)
		plats.update(guy.otherY)
		guy.update()
		powers.update(guy.otherY,guy.rect,guy.direction)
		score.update()


	#################################################################################
	####----------------------------------PAUSE----------------------------------####
	#################################################################################
	elif(alive and paused):
		keys = pygame.key.get_pressed() #keys
		if(keys[pygame.K_a]): #LEFT KEY
			if(pauseScreen.selected == "exit"): pauseScreen.selected = "resume"
		if(keys[pygame.K_d]): #RIGHT KEY
			if(pauseScreen.selected == "resume"): pauseScreen.selected = "exit"
		if(keys[pygame.K_SPACE] and pauseScreen.selected == "exit"):
			pygame.quit()
			exit()
		if((keys[pygame.K_SPACE] and pauseScreen.selected == "resume") or (keys[pygame.K_ESCAPE]) and pauseScreen.cooldown<0):
			if(DEBUG): print("pause escape")
			paused = False
			pauseScreen.cooldownReset()

		pygame.display.flip()
		pauseScreen.update()
		pauseScreen.cooldown -= 1
		



	#################################################################################
	####----------------------------------DEATH----------------------------------####
	#################################################################################
	else:
		#fill screen
		pygame.display.flip()
		clock.tick(60)
		screen.fill((0,0,0))
		screen.blit(bg.gameOver,(0,0))
		
		#make text
		scoreText = fontLarge.render("Score: {}".format(score.value),True,(0,0,0),None)
		highScoreText = fontSmall.render("High Score: {}".format(score.high),True,(0,0,0),None)
		resetText = fontSmall.render("(press space to reset)",True,(0,0,0),None)
		#show text
		screen.blit(scoreText,getCenter(scoreText,-100,-50))
		screen.blit(highScoreText,getCenter(highScoreText,-100,0))
		screen.blit(resetText,(getCenter(resetText,-100,30)))
		screen.blit(guy.left,(getCenter(guy.left,150,-50)))
		
		#when you want to reset
		keys = pygame.key.get_pressed()
		if(keys[pygame.K_SPACE]): #reset key
			alive=True #woah, you are alive
			guy.reset() #reset the guy
			plats.empty()
			powers.empty()
			spawnPlatforms()
			if(DEBUG): print("plat[0] y: {}\nplat[1] y: {}\nplat[-1] y: {}\n".format(plats.sprites()[0].y,plats.sprites()[1].y,plats.sprites()[-1].y))
			score.reset() #reset your score
