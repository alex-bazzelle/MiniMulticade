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

def getCenter(thing): return width/2-(thing.get_width()/2), height/2-(thing.get_height()/2)


#BACKGROUND
class Background():
	def __init__(self):
		self.bgT = pygame.image.load('Project/Doodle Jump/graph bg.png')
		self.bgTx, self.bgTy = 0,0
		screen.blit(self.bgT,(self.bgTx,self.bgTy))
		self.bgB = self.bgT
		self.bgBx, self.bgBy = 0,-1*height
		screen.blit(self.bgB,(self.bgBx,self.bgBy))
		self.scroll = 0
		self.tiles = math.ceil(height / self.bgT.get_height()) + 1
	def scroll(self, value=1):
		self.bgTy += value
		self.bgBy += value
		if(self.bgTy>height-10): self.bgTy *=-1
		if(self.bgBy>height-10): self.bgBy *=-1
	def update(self,focus):
		#self.bgTy += -1*focus.velY
		#self.bgBy += -1*focus.velY

		for i in range(0,self.tiles):
			screen.blit(self.bgT, (0,self.bgT.get_height()*i-self.scroll))
			screen.blit(self.bgB, (0,-1*(self.bgB.get_height()*i-self.scroll)))
		self.scroll += focus.velY
		if(abs(self.scroll)>self.bgT.get_height()): self.scroll = 0
		#if(abs(self.bgTy)>height)
		# if(self.bgTy>height-10): self.bgTy *= -1
		# if(self.bgBy>height-10): self.bgBy *= -1
		# if(self.bgTy<-10+height*-1): self.bgTy *= -1
		# if(self.bgBy<-10+height*-1): self.bgBy *= -1
		#if(self.bgTy>height-10 or self.bgTy<(height*-1)-10): self.bgTy *=-1
		#if(self.bgBy>height-10 or self.bgBy<(height*-1)-10): self.bgBy *=-1
		#screen.blit(self.bgT, (self.bgTx,self.bgTy))
		#screen.blit(self.bgB, (self.bgBx,self.bgBy))
bg = Background()

#JUMPER
class Jumper(pygame.sprite.Sprite):
	def __init__(self, pic):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(pic) #load in the image
		self.rect = self.image.get_rect()
		self.x, self.y = getCenter(self.image)
		screen.blit(self.image, (self.x,self.y)) #plop it on the screen
		self.velX = 0 #velocity X
		self.velY = 0 #velocity Y
	def isCollide(self,group):
		return pygame.sprite.spritecollide(self,group,False)
	def update(self):
		self.x += self.velX
		self.y += (self.velY)*-1
		if(self.velX>0): self.velX-=1
		if(self.velX<0): self.velX+=1
		self.rect.x, self.rect.y = self.x, self.y
		screen.blit(self.image, (self.x,self.y))
guy = Jumper('Project/Doodle Jump/jumpDude.png')



class Platform(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Project/Doodle Jump/greenPlatform.png') #load in the image
		self.rect = self.image.get_rect()
		self.x, self.y = getCenter(self.image)
		self.y += 200
		screen.blit(self.image, (self.x,self.y)) #plop it on the screen
	def update(self):
		self.rect.x, self.rect.y = self.x, self.y
		screen.blit(self.image, (self.x,self.y))
plat1 = Platform()
plat2 = Platform()
plat2.x += 100
plats = pygame.sprite.Group()
plats.add(plat1)
plats.add(plat2)



 
isFalling = True
guy.update()
plats.update()
while True: #game loop

#################################################################################
##################################INPUT##########################################
#################################################################################
	for event in pygame.event.get(): #events
		match event.type:
			case pygame.QUIT:
				pygame.quit()
				print("\n\n\n GAME QUIT\n\n\n")
				exit()
			case _:
				pass
	keys = pygame.key.get_pressed() #keys
	
	if(keys[pygame.K_SPACE]): #if space, move bg
		bg.scroll()
	if(keys[pygame.K_a]): #move left in bounds
		if(guy.x>0): guy.velX-=2
	if(keys[pygame.K_d]): #move right in bounds
		if((guy.x+guy.image.get_width())<width): guy.velX+=2
	

#################################################################################
##################################UPDATE#########################################
#################################################################################
	
	if(isFalling): #FALLING
		if(guy.velY>-5): guy.velY -= 1 #don't fall too fast
	if(guy.rect.bottom>height): #DEATH
		guy.x, guy.y = getCenter(guy.image)

	if(len(guy.isCollide(plats))>0): #COLLIDE
		guy.velY = 30

	



#################################################################################
##################################RENDER#########################################
#################################################################################
	pygame.display.flip()
	clock.tick(60)
	screen.fill((0,0,0))
	bg.update(guy)
	guy.update()
	plats.update()