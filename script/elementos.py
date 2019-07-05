import pygame as pg 
import pytweening as tween


from script import *

class plataform_m(pg.sprite.Sprite):
	def __init__(self,x,y,vl):
		pg.sprite.Sprite.__init__(self)
		self.image = image["plataform_movil"]	
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.step = 0
		self.vlx = int(vl)

	def update(self):
		
		self.step += 1
		self.rect.x += self.vlx
		if self.step > 80:
			self.vlx *=-1
			self.step = 0 

class Trap(pg.sprite.Sprite):
	def __init__(self,x,y,game,sentido = "top"):
		pg.sprite.Sprite.__init__(self)
		self.trap = image["spikes"]
		self.frames = 8
		self.sentido  = sentido

		self.image = self.trap.subsurface((0,0),(32,32))
		
		self.activate = False
		self.activate_spike = False
		self.cont = 0
		self.position = 0

		if self.sentido == "right": self.image = pg.transform.rotate(self.image,-90)
		elif self.sentido == "left": self.image = pg.transform.rotate(self.image,90)
		elif self.sentido == "bottom": self.image = pg.transform.rotate(self.image,180)

		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y 
		self.mask = pg.mask.from_surface(self.image)
		self.game = game

	def update(self):
		self.animation()

		colision = pg.sprite.collide_mask(self.game.player,self)
		if colision != None and self.activate_spike == True:
			self.game.player.dead = True
		colision = pg.sprite.collide_mask(self.game.player,self)
		if colision != None and self.activate_spike == True:
			self.game.player.dead = True
		for enemy in self.game.enemies:
			colision_enemies = pg.sprite.collide_mask(enemy,self)
			if colision_enemies != None and self.activate_spike == True:
				enemy.kill()


	def animation(self):
		if self.activate == False:
			self.activate_spike = False
			self.image = self.trap.subsurface((32*self.position,0),(32,32)) 
			if self.sentido == "right": self.image = pg.transform.rotate(self.image,-90)	
			self.mask = pg.mask.from_surface(self.image)			
			self.position +=1
			if self.position == self.frames: self.activate = True

		else:
			if self.position != 6 and self.position > 0:
				self.position -=1
				self.step = 0

			elif self.position == 6:
				self.step +=1
				if self.step == 55: self.position -=1	
			
			elif self.position == 0:
				self.step +=1
				self.activate_spike = True
				if self.step == 55: self.activate = False
		
			self.image = self.trap.subsurface((32*self.position,0),(32,32)) 
			if self.sentido == "right": self.image = pg.transform.rotate(self.image,-90)	
			elif self.sentido == "left": self.image = pg.transform.rotate(self.image,90)
			elif self.sentido == "bottom": self.image = pg.transform.rotate(self.image,-180)
			self.mask = pg.mask.from_surface(self.image)	
			
class Key(pg.sprite.Sprite):
	def __init__(self,x,y,game):
		pg.sprite.Sprite.__init__(self)
		self.image =pg.transform.scale( image["key"],(8,15)) 	
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
			self.game.player.keys['KEY_YELLOW'] = True
			self.game.sound["objs"].play()
			self.kill()

		offset = self.bob_range *  (self.tween(self.step / self.bob_range) - 0.5)
		self.rect.centery = self.posy + offset * self.dir
		self.step += self.bob_speed
		
		if self.step > self.bob_range:
			self.step = 0
			self.dir *=-1

class Trampoline(pg.sprite.Sprite):
	def __init__(self,x,y,game):
		pg.sprite.Sprite.__init__(self)
		self.frames = [(0,0),(21,0),(41,0),(58,0),(76,0),(21,20),(39,20),(56,20),(76,20)]
		
		self.tramp = image["trampoline"]
		self.image = self.tramp.subsurface(self.frames[0],(13,9))
		self.image = pg.transform.scale(self.image,(32,32))

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
				self.game.sound["jump"].stop()
				self.game.sound["jump"].play()

				self.activate = True
				self.jump()

		self.animation()

	def animation(self):
		
		if self.activate == True:
			self.image = self.tramp.subsurface(self.frames[self.position],(13,9)) 			
			self.image = pg.transform.scale(self.image,(32,32))
			self.position +=1
			if self.position >= self.frame: self.activate = False
			
		else:
			self.position = 0
			self.image = self.tramp.subsurface(self.frames[self.position],(13,9)) 			
			self.image = pg.transform.scale(self.image,(32,32))
				
	def jump(self, vl = -15):
		self.game.player.cont_jump = 0
		self.game.player.direcciony = -1
		self.game.player.vly = vl

class Door(pg.sprite.Sprite):
	def __init__(self,x,y,game,Type):
		pg.sprite.Sprite.__init__(self)
		self.position = 0
		self.frames = {0:(0,0),1:(0,42),2:(0,84),3:(0,126)}

		if Type == "YELLOW":
			self.image_a =  image["door"]
		self.image = self.image_a.subsurface(self.frames[0],(39,42))
		self.image = pg.transform.scale(self.image,(62,64))
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
			self.OpenDoor()

	def OpenDoor(self):
		self.step += 2.5
		if self.step > self.delay:
			if self.position < 4:	
				print(self.frames[self.position])				
				self.image = self.image_a.subsurface(self.frames[self.position],(39,42)) 			
				self.image = pg.transform.scale(self.image,(62,64))
				self.position +=1

			elif self.position >= 4:
				self.next = True
				self.position =0

			self.step = 0 
		
class Lemon(pg.sprite.Sprite):
	def __init__(self,x,y,game):
		pg.sprite.Sprite.__init__(self)
		self.image =pg.transform.scale2x( image["lemon"] )
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y 
		self.game = game
		self.tween = tween.easeInOutSine
		self.bob_range = 20
		self.bob_speed = 0.5
		self.step = 0
		self.dir = 1
		self.posy = y

	def update(self):
		if self.rect.colliderect(self.game.player.rect):
				self.game.sound["objs"].play()
				self.kill()

		offset = self.bob_range *  (self.tween(self.step / self.bob_range) - 0.5)
		self.rect.centery = self.posy + offset * self.dir
		self.step += self.bob_speed
		
		if self.step > self.bob_range:
			self.step = 0
			self.dir *=-1

class Fire_Cannon(pg.sprite.Sprite):
	def __init__(self,x,y,game,sentido):
		pg.sprite.Sprite.__init__(self)
		self.fireball = []
		self.limite = 1
		self.game = game
		self.rect = pg.Rect(x,y,20,20)
		self.sentido = sentido
		self.step = 0
	def update(self):
		if len(self.fireball) < self.limite:
			self.step +=1
			if self.step == 20:
				self.fireball.append(Fireball(self.rect.centerx,self.rect.centery,self.sentido))
				self.step = 0

		for fireball in self.fireball:
			colision = pg.sprite.collide_mask(self.game.player,fireball)
			if colision != None:
				self.game.player.dead = True

			colision_pared = pg.sprite.spritecollide(fireball,self.game.plataform,False)
			
			if len(colision_pared) > 0:
				
				self.fireball.remove(fireball)
				
			fireball.update()

class Fireball(pg.sprite.Sprite):

	def __init__(self,x,y,sentido):
		pg.sprite.Sprite.__init__(self)
		self.frames = { 0:(0,0), 1:(0,12), 2:(0,24), }
		self.image_a = image["fireball"]
		self.image = self.image_a.subsurface(self.frames[0],(12,12))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.mask = pg.mask.from_surface(self.image)
		
		if sentido == "right": self.vlx = 3
		elif sentido == "left": self.vlx  = -3
		else: self.vlx = 0		
		
		if sentido == "bottom": self.vly = 3
		elif sentido == "top": self.vly  = -3
		else: self.vly = 0
		
		self.position = 0
		self.step = 0
		self.delay = 10

	def update(self):

		self.rect.x += self.vlx
		self.rect.y += self.vly
		self.animation()

	def animation(self):
		
		self.step += 2.5
		
		if self.step > self.delay:
			if self.position < 3:	
				self.image = self.image_a.subsurface(self.frames[self.position],(12,12)) 			
				self.position +=1
				
			elif self.position >= 3:
				self.position =0

			self.step = 0 