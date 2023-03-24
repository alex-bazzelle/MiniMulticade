import pygame
from random import randint
import math

#setup window
pygame.init() #initialize pygame
pygame.display.set_caption("Doodle Jump") #window title
pygame.display.set_icon(pygame.image.load('Project/Doodle Jump/jumpDude.png')) #window icon

#quality of life
width = 1024 #width of the screen
height = 600 #height of the screen
clock = pygame.time.Clock() #clock for managing framerate
screen = pygame.display.set_mode((width, height),0,32) #give you a screen to play on
fontLarge = pygame.font.Font(None,64) #big boy font
fontSmall = pygame.font.Font(None,32) #small boy font
def getCenter(thing,dx=0,dy=0): #get the center of objects. dx and dy are to change it
	return width/2-(thing.get_width()/2)+dx, height/2-(thing.get_height()/2)+dy


##############
#-BACKGROUND-#
##############
class Background():
	def __init__(self): #make the background
		self.image = pygame.image.load('Project/Doodle Jump/graph bg.png') #background image
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
#---JUMPER---#
##############
class Jumper(pygame.sprite.Sprite):
	def __init__(self): #make the sprite
		pygame.sprite.Sprite.__init__(self) #it is a sprite
		self.right = pygame.image.load('Project/Doodle Jump/jumpDude.png') #load in the image
		self.left = pygame.image.load('Project/Doodle Jump/jumpDudeL.png') #load in the image
		self.image = self.right #looking right by default
		self.rect = self.image.get_rect() #give it a rect for collisions
		self.x, self.y = getCenter(self.image) #give it an x and y
		self.velX = 0 #velocity X
		self.velY = 0 #velocity Y
		self.otherY = 0 #if you can explain this i'll give you a dollar
		self.update() #update it :)
	def collisions(self,group): #shorthand for collisions
		return pygame.sprite.spritecollide(self,group,False)
	def update(self): #update every frame
		self.x += self.velX #update x
		if(self.y-self.velY>0): self.y += (self.velY)*-1 #update y

		if(self.velX>0): self.velX-=1; self.image=self.right #decrease velocity
		if(self.velX<0): self.velX+=1; self.image=self.left #so that you can stop

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
#--PLATFORMS--#
###############
plats = pygame.sprite.Group() #group for all of them
class Platform(pygame.sprite.Sprite): #main class for platforms
	def __init__(self,x=450,y=height-100): #default is bottom center of screen
		pygame.sprite.Sprite.__init__(self) #it's a sprite
		self.image = pygame.image.load('Project/Doodle Jump/greenPlatform.png') #load in the image
		self.rect = self.image.get_rect() #give it a rect for collisions
		self.startX, self.startY = x,y #gotta know how to reset it
		self.x, self.y = x,y #give it x and y
		self.isBroken = False #used for broken platforms

		self.update() #make it happen!
	def update(self,focusY=0): #focusY is the jumper guy
		self.y += focusY #move it down when jumper moves up
		self.rect.x, self.rect.y = self.x, self.y #stupid collision stuff
		screen.blit(self.image, (self.x,self.y)) #show it on the screen
	def reset(self): #reset when you lose
		self.y = self.startY #reset y
		self.x = self.startX #reset x
		self.update() #update it
class BrokenPlatform(Platform): #subclass for broken platforms
	def __init__(self,x=450,y=height-100): #same as normal platform
		Platform.__init__(self)
		self.image = pygame.image.load('Project/Doodle Jump/brownPlatform.png')
		self.rect = self.image.get_rect()
		self.startX, self.startY = x,y
		self.x, self.y = x,y
		#stages are the animation cycle
		self.stage = [self.image,pygame.image.load('Project/Doodle Jump/BrPlatAnim/BrPlat1.png'),
						pygame.image.load('Project/Doodle Jump/BrPlatAnim/BrPlat2.png'),
						pygame.image.load('Project/Doodle Jump/BrPlatAnim/BrPlat3.png'),
						pygame.image.load('Project/Doodle Jump/BrPlatAnim/BrPlat4.png'),
						pygame.image.load('Project/Doodle Jump/BrPlatAnim/BrPlat5.png')]
		
		self.update()
	def update(self,focusY=0):
		self.y += focusY
		self.rect.x, self.rect.y = self.x, self.y
		screen.blit(self.image, (self.x,self.y))
		if(self.isBroken): self.removePlat() #if you break, do that action as well
	def removePlat(self): #when you break the platform
		index = self.stage.index(self.image) #find what stage it's at
		if(index<5): #if it isn't at the end stage
			self.image = self.stage[index+1] #increase the stage (aka next frame in animation)
			self.y+=10 #fall down
		else: self.kill() #if we're at the last stage, die

#the default platforms. you always start the same way.
plat1 = Platform(); plats.add(plat1)
plat2 = Platform(600,400); plats.add(plat2)
plat3 = Platform(300,200); plats.add(plat3)

#SPAWNS PLATFORMS
def spawnPlatforms():
	for i in range(0,100): #makes 100 normal platforms
		platY = -1*i*90 #the spacing between platforms
		plats.add(Platform(randint(0,width-plat1.rect.width),platY)) #adds the platform
		if(randint(0,100)<30): # 30% chance to add a broken platform
			newPlat = BrokenPlatform(randint(0,width-plat1.rect.width),platY+randint(plat1.rect.height+20,200)) #randomize height
			if(len(pygame.sprite.spritecollide(newPlat,plats,False))==0): #if it isn't colliding with a platform
				plats.add(newPlat) #add it!
spawnPlatforms()
#RECYCLING PLATFORMS
def recyclePlatforms(lowPlat,highPlat):
	lowPlat.kill() #remove it from the group
	lowPlat.y = (highPlat.y-randint(90,110)) #y is the highest y value plus 90ish
	lowPlat.x = randint(0,width-lowPlat.rect.width) #x is anywhere
	lowPlat.isBroken = False #not broken
	return lowPlat


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

	if(alive):
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


	#################################################################################
	####----------------------------------UPDATE---------------------------------####
	#################################################################################

		#FALLING
		if(guy.velY>=-10): guy.velY -= 0.5 #don't fall too fast

		#DEATH
		if(guy.rect.bottom>height):
			alive = False
			guy.x, guy.y = getCenter(guy.image)

		#COLLIDE
		if(len(guy.collisions(plats))>0 and guy.velY<-0.5): #did you collide with a plat and are you falling
			for plat in guy.collisions(plats): #check that your feet are touching a platform
				if(guy.rect.bottom<plat.rect.bottom and guy.rect.bottom>plat.rect.top):
					if(isinstance(plat,BrokenPlatform)): #broken platform
						plat.isBroken = True #start broken animation
					elif(isinstance(plat,Platform)): #normal platform
						guy.velY = 10 #jump
		
		#SCORE
		if(int((plat1.y-guy.y)/10) > score.value): score.value = int((plat1.y-guy.y)/10)

		#honestly im not really sure, but it messes up without this
		guy.otherY = guy.velY
		if(guy.y-guy.velY<50):
			guy.otherY+= 10

		#RECYCLE PLATFORMS
		if(plats.sprites()[1].y > 1000): #if a platform is way off screen
			plats.add(recyclePlatforms(plats.sprites()[1],plats.sprites()[-1])) #move it to the top


	#################################################################################
	####----------------------------------RENDER---------------------------------####
	#################################################################################
		pygame.display.flip()
		clock.tick(60)
		screen.fill((0,0,0))
		bg.update(guy.otherY)
		plats.update(guy.otherY)
		guy.update()
		score.update()


	#################################################################################
	####----------------------------------DEATH----------------------------------####
	#################################################################################
	else:
		#fill screen
		pygame.display.flip()
		clock.tick(60)
		screen.fill((0,0,0))
		
		#make text
		scoreText = fontLarge.render("Score: {}".format(score.value),True,(255,255,255),None)
		highScoreText = fontSmall.render("High Score: {}".format(score.high),True,(255,255,255),None)
		resetText = fontSmall.render("Press space to reset",True,(255,255,255),None)
		#show text
		screen.blit(scoreText,getCenter(scoreText,0,-50))
		screen.blit(highScoreText,getCenter(highScoreText,0,0))
		screen.blit(resetText,(getCenter(resetText,0,50)))
		
		#when you want to reset
		keys = pygame.key.get_pressed()
		if(keys[pygame.K_SPACE]): #reset key
			alive=True #woah, you are alive
			guy.reset() #reset the guy
			for plat in plats.sprites(): plat.reset() #reset the sprites
			score.reset() #reset your score
