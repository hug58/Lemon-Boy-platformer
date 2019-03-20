import pygame as pg 
import os.path, sys
import pytweening as tween
from script import Sprite
from script import function_utils as fun

class Player(Sprite.Sprite):
	def __init__(self,x,y,game):
		Sprite.Sprite.__init__(self)

		self.state = [	pg.image.load(fun.resolve_route("image/sprites/hug/hug0.png")),
						pg.image.load(fun.resolve_route("image/sprites/hug/hug1.png")),
																			]
		
		self.walk = [	
						pg.image.load(fun.resolve_route("image/sprites/hug/hug2.png") ),
						pg.image.load(fun.resolve_route("image/sprites/hug/hug3.png") ),													
						pg.image.load(fun.resolve_route("image/sprites/hug/hug4.png")),
						pg.image.load(fun.resolve_route("image/sprites/hug/hug5.png") ),												
																				]


		self.jump = [	pg.image.load(fun.resolve_route("image/sprites/hug/hug6.png")),
																				]

		self.archers = [	pg.image.load(fun.resolve_route("image/sprites/hug/hug7.png")),
						pg.image.load(fun.resolve_route("image/sprites/hug/hug9.png")),]

		
		self.activate_jump = False
		self.animation_state = Sprite.animation(self.state,32,52)
		self.animation_walk = Sprite.animation(self.walk,32,52)

		self.image = self.state[0]
		self.mask = pg.mask.from_surface(self.image)
		self.rect = pg.Rect((x,y),(25,52))
		self.rect.centerx = self.rect.x
		self.rect.y = y 
		self.vly = 0
		self.vlx = 0
		
		self.direccionx = 1
		self.direcciony = 0
		self.stop = False

		self.game = game
		self.cont_jump = 2
		self.keys = {	'KEY_YELLOW': False,'KEY_BLUE': False,
						'KEY_RED': False,
					}
		
		self.cont_shot  = 0

		self.dead = None

		self.cont_dead = 0

	def update(self):
		
		if self.vlx == 0:
			self.animation_state.limite = 10
			if self.direccionx > 0:
				self.image = self.animation_state.update(False)
			if self.direccionx < 0:
				self.image = self.animation_state.update(True)
		elif self.vlx > 0:
			self.image = self.animation_walk.update(False) 
		elif self.vlx < 0:
			self.image = self.animation_walk.update(True)
		if self.direcciony < 0:	

			if self.direccionx > 0:
				self.image = self.jump[0]
			else:
				self.image = pg.transform.flip(self.jump[0],1,0)

		self.mask = pg.mask.from_surface(self.image)
		self.move()	

		if self.vlx >= 7:
			self.vlx = 7
		elif self.vlx <= -7:
			self.vlx = -7	

		if self.stop == True:
			if self.vlx > 0:
				self.vlx -=1
			elif self.vlx < 0:
				self.vlx +=1
			else:
				self.stop = False
		
		self.gravity()
		self.Fundead()
		self.collided()

		if len(self.colision_plataform) == 0 and self.cont_jump == 2:
			self.direcciony = -1
			self.cont_jump = 1

	def move(self):
		move = pg.key.get_pressed()
		
		if move[pg.K_LEFT]:
			self.direccionx = -1
			self.vlx +=-1  			
			self.stop = False
		if move[pg.K_RIGHT]:
			self.direccionx = 1
			self.vlx += 1		
			self.stop = False	
		if move[pg.K_c]:
		    if self.vlx == 0:
			    self.cont_shot += 0.55
			    if self.cont_shot>= 10:
				    self.archer(1)
			    elif self.cont_shot >= 5:
				    self.archer(0)

	def archer(self,pos):
		
		if self.direccionx > 0:
			self.image = self.archers[pos] 			
		elif self.direccionx < 0:
			self.image = pg.transform.flip(self.archers[pos],1,0)

	def shot(self):

		self.game.sound["arrow"].play()
		
		if self.direccionx > 0:
			self.game.arrow.add(Arrow(self.rect.right +5,self.rect.centery,1,self.game))
		elif self.direccionx < 0:
			self.game.arrow.add(Arrow(self.rect.left -5,self.rect.centery,-1,self.game))

	def Fundead(self):
		
		if self.dead == True:
			self.fuerza_gravitatoria = 0
			self.vlx = 0
			self.vly = 0
			if self.cont_dead == 0:
				self.game.sound["dead"].play()
			self.cont_dead +=1
			if self.cont_dead >= 10:
				self.game.load()
		
class Arrow(pg.sprite.Sprite):
	def __init__(self,x,y,direccion,game):
		pg.sprite.Sprite.__init__(self)
		self.direccion = direccion
		if self.direccion > 0:
			self.image = pg.image.load(fun.resolve_route("image/sprites/hug/arrow.png"))
		elif self.direccion < 0:
			self.image = pg.transform.flip(pg.image.load(fun.resolve_route("image/sprites/hug/arrow.png") ),1,0)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y  = y
		self.game = game
		self.vl = 11 if self.direccion > 0 else -11

	def update(self):
		self.colision =  pg.sprite.spritecollide(self,self.game.plataform,False)
		if len(self.colision) > 0:
			self.vl = 0
			self.vly = 0
		self.colision_enemy = pg.sprite.spritecollide(self,self.game.enemies,True)
		if len(self.colision_enemy) > 0:
			self.kill()

		self.rect.x += self.vl
	
class Dead(pg.sprite.Sprite):
	def __init__(self,x,y):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.image.load(fun.resolve_route("dead.png"))
		self.image = pg.transform.scale(self.image,(32,32))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.tween = tween.easeInOutSine
		self.bob_range = 20
		self.bob_speed = 0.7
		self.step = 0
		self.dir = 1
		self.posy = y
		self.posx = x

	def update(self):
		offset = self.bob_range *  (self.tween(self.step / self.bob_range) - 0.5)
		self.rect.centery -=1 
		self.rect.centerx = self.posx + offset * self.dir
		self.step += self.bob_speed
		
		if self.step > self.bob_range:
			self.step = 0
			self.dir *=-1