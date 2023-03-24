import pygame
from random import randint
import math

pygame.init() #initialize pygame

#some quality of life stuff
width = 1024
height = 600
clock = pygame.time.Clock()
pygame.display.set_caption("Doodle Jump")
pygame.display.set_icon(pygame.image.load('Project/Doodle Jump/jumpDude.png'))
screen = pygame.display.set_mode((1024, 600),0,32) #screen size


fontLarge = pygame.font.Font(None,64)
fontSmall = pygame.font.Font(None,32)
def getCenter(thing,dx=0,dy=0): return width/2-(thing.get_width()/2)+dx, height/2-(thing.get_height()/2)+dy


#BACKGROUND
class Background():
	def __init__(self):
		self.image = pygame.image.load('Project/Doodle Jump/graph bg.png')
		self.x, self.y = 0,0
		screen.blit(self.image,(self.x,self.y))
		self.scroll = 0
		self.tiles = math.ceil(height / self.image.get_height()) + 2
	def update(self,focusY=0):
		for i in range(0,self.tiles): #three tiles
			screen.blit(self.image, (0,(self.image.get_height()*i+self.scroll)-height)) #show those tiles
		self.scroll += focusY #change center tile position
		if(abs(self.scroll)>self.image.get_height()): self.scroll = 0 #loop tiles
bg = Background()

#JUMPER
class Jumper(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.right = pygame.image.load('Project/Doodle Jump/jumpDude.png') #load in the image
		self.left = pygame.image.load('Project/Doodle Jump/jumpDudeL.png') #load in the image
		self.image = self.right
		self.rect = self.image.get_rect()
		self.x, self.y = getCenter(self.image)
		self.velX = 0 #velocity X
		self.velY = 0 #velocity Y
		self.otherY = 0
		self.update()
	def collisions(self,group):
		return pygame.sprite.spritecollide(self,group,False)
	def update(self):
		self.x += self.velX #update x
		if(self.y-self.velY>0): self.y += (self.velY)*-1 #update y

		if(self.velX>0): self.velX-=1; self.image=self.right #decrease velocity
		if(self.velX<0): self.velX+=1; self.image=self.left #so that you can stop

		if(self.x<5): self.x = 0 #stay in bounds (left)
		if(self.rect.right>width): self.x = width-self.rect.width #stay in bounds (right)

		self.rect.x, self.rect.y = self.x, self.y #update collision box
		screen.blit(self.image, (self.x,self.y)) #draw the dude
	def reset(self):
		self.x, self.y = getCenter(self.image)
		self.velX = 0 #velocity X
		self.velY = 0 #velocity Y
		self.update()
guy = Jumper()


plats = pygame.sprite.Group()
class Platform(pygame.sprite.Sprite):
	def __init__(self,x=450,y=height-100):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Project/Doodle Jump/greenPlatform.png') #load in the image
		self.rect = self.image.get_rect()
		self.startX, self.startY = x,y
		self.x, self.y = x,y
		self.isBroken = False

		self.update()
	def update(self,focusY=0):
		self.y += focusY
		self.rect.x, self.rect.y = self.x, self.y
		screen.blit(self.image, (self.x,self.y))
	def reset(self):
		self.y = self.startY
		self.x = self.startX
		self.update()

class BrokenPlatform(Platform):
	def __init__(self,x=450,y=height-100):
		Platform.__init__(self)
		self.image = pygame.image.load('Project/Doodle Jump/brownPlatform.png')
		self.rect = self.image.get_rect()
		self.startX, self.startY = x,y
		self.x, self.y = x,y
		self.stage = [self.image,pygame.image.load('Project/Doodle Jump/BrPlatAnim/BrPlat1.png'),
						pygame.image.load('Project/Doodle Jump/BrPlatAnim/BrPlat2.png'),
						pygame.image.load('Project/Doodle Jump/BrPlatAnim/BrPlat3.png'),
						pygame.image.load('Project/Doodle Jump/BrPlatAnim/BrPlat4.png'),
						pygame.image.load('Project/Doodle Jump/BrPlatAnim/BrPlat5.png')]
		#plats.add(self)
		

		self.update()
	def update(self,focusY=0):
		self.y += focusY
		self.rect.x, self.rect.y = self.x, self.y
		screen.blit(self.image, (self.x,self.y))
		if(self.isBroken): self.removePlat()
	def removePlat(self):
		index = self.stage.index(self.image) #find what stage it's at
		if(index<5): #if it isn't at the end stage
			self.image = self.stage[index+1] #increase the stage (aka next frame in animation)
			self.y+=10
		else: self.kill() #if we're at the last stage, die

plat1 = Platform(); plats.add(plat1)
plat2 = Platform(600,400); plats.add(plat2)
plat3 = Platform(300,200); plats.add(plat3)
plat4 = Platform(400,0); plats.add(plat4)



class Score():
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

def recyclePlatforms(lowPlat,highPlat):
	lowPlat.kill() #remove it from the group
	lowPlat.y = (highPlat.y-90)
	lowPlat.x = randint(0,width-lowPlat.rect.width)
	lowPlat.isBroken = False
	return lowPlat





alive = True
while True: #game loop
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
	##################################INPUT##########################################
	#################################################################################
		
		keys = pygame.key.get_pressed() #keys
		if(keys[pygame.K_a]): #move left in bounds
			if(guy.x>0): guy.velX-=2
			else: guy.velX = 0
		if(keys[pygame.K_d]): #move right in bounds
			if((guy.x+guy.image.get_width())<width): guy.velX+=2
			else: guy.velX = 0
		

	#################################################################################
	##################################UPDATE#########################################
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
						plat.isBroken = True
					elif(isinstance(plat,Platform)): #normal platform
						guy.velY = 10 #jump
		
		#SCORE
		if(int((plat1.y-guy.y)/10) > score.value): score.value = int((plat1.y-guy.y)/10)


			
		
		#honestly im not really sure, but it messes up without this
		guy.otherY = guy.velY
		if(guy.y-guy.velY<50):
			guy.otherY+= 10

		#recycle plats
		if(plats.sprites()[1].y > 1000): #if a platform is way off screen
			plats.add(recyclePlatforms(plats.sprites()[1],plats.sprites()[-1]))

		



	#################################################################################
	##################################RENDER#########################################
	#################################################################################
		pygame.display.flip()
		clock.tick(60)
		screen.fill((0,0,0))
		bg.update(guy.otherY)
		plats.update(guy.otherY)
		guy.update()
		score.update()





	#end game loop
	else:
		#DEATH
		pygame.display.flip()
		clock.tick(60)
		screen.fill((0,0,0))
		
		scoreText = fontLarge.render("Score: {}".format(score.value),True,(255,255,255),None)
		highScoreText = fontSmall.render("High Score: {}".format(score.high),True,(255,255,255),None)
		resetText = fontSmall.render("Press space to reset",True,(255,255,255),None)
		screen.blit(scoreText,getCenter(scoreText,0,-50))
		screen.blit(highScoreText,getCenter(highScoreText,0,0))
		screen.blit(resetText,(getCenter(resetText,0,50)))
		

		keys = pygame.key.get_pressed() #keys
		#RESET
		if(keys[pygame.K_SPACE]):
			alive=True
			guy.reset()
			for plat in plats.sprites():
				plat.reset()
			score.reset()
			
