import pygame
import os.path
import pytweening as tween


WHITE2 =  (252,252,238)
LEMON = (249,215,0)
GREEN = (140,196,51)

ruta_base =  os.path.abspath("")
ruta_base += "/image/"
ruta_sound = os.path.abspath("")
ruta_sound += "/sound/"

class Block(pygame.sprite.Sprite):
	def __init__(self,x,y,scale):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(ruta_base +"pasto.png")	
		self.image = pygame.transform.scale(self.image,(scale[0],scale[0]))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vly = 0
		self.vlx = 0
		self.x = x
		self.y = y

class Trap(pygame.sprite.Sprite):
	def __init__(self,x,y,game,sentido = "top"):
		pygame.sprite.Sprite.__init__(self)
		self.trap = pygame.image.load(ruta_base + "spikes.png")
		self.frames = 8
		self.sentido  = sentido

		self.image = self.trap.subsurface((0,0),(32,32))
		
		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y 
		self.mask = pygame.mask.from_surface(self.image)
		self.game = game
		
		self.activate = False
		self.activate_spike = False
		self.cont = 0
		self.position = 0

		if self.sentido == "top":
			pass

		elif self.sentido == "right":
			self.image = pygame.transform.rotate(self.image,-90)

		elif self.sentido == "left":
			self.image = pygame.transform.rotate(self.image,90)

		elif self.sentido == "bottom":
			self.image = pygame.transform.rotate(self.image,180)



	def update(self):
		self.animation()

		colision = pygame.sprite.collide_mask(self.game.player,self)
		if colision != None and self.activate_spike == True:
			self.game.player.dead = True
		colision = pygame.sprite.collide_mask(self.game.player,self)
		if colision != None and self.activate_spike == True:
			self.game.player.dead = True
		for enemy in self.game.enemies:
			colision_enemies = pygame.sprite.collide_mask(enemy,self)
			if colision_enemies != None and self.activate_spike == True:
				enemy.kill()


	def animation(self):
		if self.activate == False:
			self.activate_spike = False
			self.image = self.trap.subsurface((32*self.position,0),(32,32)) 
			if self.sentido == "right":
				self.image = pygame.transform.rotate(self.image,-90)	
			self.mask = pygame.mask.from_surface(self.image)			
			self.position +=1
			if self.position == self.frames:
				self.activate = True

		else:
			if self.position != 6 and self.position > 0:
				self.position -=1
				self.step = 0

			elif self.position == 6:
				self.step +=1
				if self.step == 55:
					self.position -=1	
			
			elif self.position == 0:
				self.step +=1
				self.activate_spike = True
				if self.step == 55:
					self.activate = False

			
			self.image = self.trap.subsurface((32*self.position,0),(32,32)) 
			if self.sentido == "right":
				self.image = pygame.transform.rotate(self.image,-90)	

			elif self.sentido == "left":
				self.image = pygame.transform.rotate(self.image,90)

			elif self.sentido == "bottom":
				self.image = pygame.transform.rotate(self.image,-180)
				
			self.mask = pygame.mask.from_surface(self.image)	
			
class Key(pygame.sprite.Sprite):
	def __init__(self,x,y,game):
		pygame.sprite.Sprite.__init__(self)
		self.image =pygame.transform.scale( pygame.image.load(ruta_base + "key.png"),(8,15))	
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.game = game
		self.tween = tween.easeInOutSine
		self.bob_range = 20
		self.bob_speed = 0.6
		self.step = 0
		self.dir = 1
		self.posy = y
		
	def update(self):
		if self.rect.colliderect(self.game.player.rect):
			#print(self.game.player.keys['KEY_YELLOW'])
			self.game.player.keys['KEY_YELLOW'] = True
			#print(self.game.player.keys['KEY_YELLOW'])
			self.game.sound.sound_object.play()
			self.kill()

		offset = self.bob_range *  (self.tween(self.step / self.bob_range) - 0.5)
		self.rect.centery = self.posy + offset * self.dir
		self.step += self.bob_speed
		
		if self.step > self.bob_range:
			self.step = 0
			self.dir *=-1

class Trampoline(pygame.sprite.Sprite):
	def __init__(self,x,y,game):
		pygame.sprite.Sprite.__init__(self)
		self.frames = [(0,0),(21,0),(41,0),(58,0),(76,0),(21,20),(39,20),(56,20),(76,20)]
		
		self.tramp = pygame.image.load( ruta_base + "trampoline.png")
		self.image = self.tramp.subsurface(self.frames[0],(13,9))
		self.image = pygame.transform.scale(self.image,(32,32))

		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y 
		
		self.frame = len(self.frames)
		self.position = 0

		self.game = game
		self.activate = False

	def update(self):
		if self.rect.colliderect(self.game.player.rect):
			if self.game.player.rect.top < self.rect.top:
				self.game.sound.sound_jump.stop()
				self.game.sound.sound_jump.play()
				self.activate = True
				self.jump()

		self.animation()

	def animation(self):
		
		if self.activate == True:
			self.image = self.tramp.subsurface(self.frames[self.position],(13,9)) 			
			self.image = pygame.transform.scale(self.image,(32,32))
			self.position +=1
			
			if self.position >= self.frame:
				self.activate = False
			
				 
		else:
			
			self.position = 0
			self.image = self.tramp.subsurface(self.frames[self.position],(13,9)) 			
			self.image = pygame.transform.scale(self.image,(32,32))

				
	def jump(self, vl = -15):
		self.game.player.cont_jump = 0
		self.game.player.direcciony = -1
		self.game.player.vly = vl

class Door(pygame.sprite.Sprite):
	def __init__(self,x,y,game,Type):
		pygame.sprite.Sprite.__init__(self)
		self.position = 1
		if Type == "YELLOW":
			self.image = pygame.image.load(ruta_base + "door1.png")
		
		self.image = pygame.transform.scale(self.image,(62,64))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y 
		self.game = game
		
		self.open = False
		self.step = 0
		self.delay = 10

		self.next = None

	def update(self):
		if self.rect.colliderect(self.game.player.rect):
			if self.game.player.keys['KEY_YELLOW'] == True:
				self.open = True

		if self.open == True: 			
			self.image = self.OpenDoor()

	def OpenDoor(self):
		self.step += 2.5
		if self.step > self.delay:
			if self.position < 5:					
				self.image = pygame.image.load(ruta_base + "door{}.png".format(self.position)) 			
				self.image = pygame.transform.scale(self.image,(62,64))
				self.position +=1
			elif self.position >= 4:
				self.next = True
				self.position =1

			self.step = 0 

		return self.image
		
class Lemon(pygame.sprite.Sprite):
	def __init__(self,x,y,game):
		pygame.sprite.Sprite.__init__(self)
		self.image =pygame.transform.scale2x( pygame.image.load(ruta_base + "lemon.png"))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y 
		self.game = game
		self.tween = tween.easeInOutSine
		#self.tween = tween.easeOutElastic
		self.bob_range = 20
		self.bob_speed = 0.5
		self.step = 0
		self.dir = 1
		self.posy = y

	def update(self):
		if self.rect.colliderect(self.game.player.rect):
				self.game.sound.sound_object.play()
				self.kill()

		offset = self.bob_range *  (self.tween(self.step / self.bob_range) - 0.5)
		self.rect.centery = self.posy + offset * self.dir
		self.step += self.bob_speed
		
		if self.step > self.bob_range:
			self.step = 0
			self.dir *=-1

class Fire_Cannon(pygame.sprite.Sprite):
	def __init__(self,x,y,game,sentido = "right"):
		pygame.sprite.Sprite.__init__(self)
		self.fireball = []
		self.limite = 1
		self.game = game
		self.rect = pygame.Rect(x,y,20,20)
		self.sentido = sentido
		self.step = 0
	def update(self):
		if len(self.fireball) < self.limite:
			self.step +=1
			if self.step == 20:
				self.fireball.append(Fireball(self.rect.centerx,self.rect.centery,self.sentido))
				self.step = 0

		for fireball in self.fireball:
			colision = pygame.sprite.collide_mask(self.game.player,fireball)
			if colision != None:
				self.game.player.dead = True

			colision_pared = pygame.sprite.spritecollide(fireball,self.game.plataform,False)
			
			if len(colision_pared) > 0:
				
				self.fireball.remove(fireball)
				
			
			fireball.update()

class Fireball(pygame.sprite.Sprite):

	def __init__(self,x,y,sentido):
		pygame.sprite.Sprite.__init__(self)
		self.frames = [	pygame.image.load(ruta_base + "ball.png"),
						pygame.image.load(ruta_base + "ball2.png"),
						pygame.image.load(ruta_base + "ball3.png"),]
		self.image = self.frames[0]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.mask = pygame.mask.from_surface(self.image)
		self.vlx = 3 if sentido == "right" else -3
		
		self.frame = len(self.frames)
		self.position = 0
		self.cont = 0
	def update(self):

		self.rect.x += self.vlx
		self.animation()

	def animation(self):
		
		self.image = self.frames[self.position] 	
		self.cont +=1	
				 
		if self.cont == 10:
			self.position +=1
			self.cont = 0	

		if self.position >= self.frame:
			self.position = 0
