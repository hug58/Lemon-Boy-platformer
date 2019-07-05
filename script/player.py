from script import *
from script.sprite import Sprite




class Player(Sprite):
	def __init__(self,x,y,game):
		

		self.walk = { 	0:(0,0), 1:(32,0), 2:(64,0), 3:(0,52),}
		self.state = { 0:(32,52), 1:(64,52),}
		self.archers = { 0:(0,104), 1:(32,104),2:(64,104),}
		self.jump= {0:(0,156),}
		self.image_a = image["hugo"]
		self.size = (32,52)
		self.game = game

		self.image = self.image_a.subsurface(self.state[0],(32,52))
		Sprite.__init__(self)


		self.activate_jump = False
		self.mask = pg.mask.from_surface(self.image)
		self.rect = pg.Rect((x,y),(25,52))
		self.rect.centerx = self.rect.x
		self.rect.y = y 


		self.vly = 0
		self.vlx = 0


		self.direccionx = 1
		self.direcciony = 0
		self.stop = False

		self.cont_jump = 2
		self.keys = {	'KEY_YELLOW': False,'KEY_BLUE': False,
						'KEY_RED': False,
					}
		
		self.cont_shot  = 0

		self.dead = None
		self.cont_dead = 0

	def update(self):
		
		if self.vlx == 0:
		
			self.frames = self.state

			if self.direccionx > 0: self.animation(0,self.state)
			if self.direccionx < 0: self.animation(1,self.state)
		
		elif self.vlx != 0:
		
			self.frames = self.walk
		
			if self.vlx > 0:  self.animation(0,self.walk) 
			elif self.vlx < 0:  self.animation(1,self.walk)
		
		if self.direcciony < 0:	
			
			self.image = self.image_a.subsurface(self.jump[0],(32,52))
			
			if self.direccionx < 0: self.image = pg.transform.flip(self.image,1,0)
			elif self.direccionx > 0: pass

		self.mask = pg.mask.from_surface(self.image)
		self.move()	

		if self.vlx >= 7: self.vlx = 7
		elif self.vlx <= -7: self.vlx = -7	

		if self.stop == True:
			
			if self.vlx > 0: self.vlx -=1
			elif self.vlx < 0: self.vlx +=1
			else: self.stop = False
		
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
			    if self.cont_shot>= 10: self.archer(1)
			    elif self.cont_shot >= 5: self.archer(0)

	def archer(self,pos):
		
		self.image = self.image_a.subsurface(self.archers[pos],(32,52))
		
		if self.direccionx < 0: self.image = pg.transform.flip(self.archers[pos],1,0)
		elif self.direccionx > 0: pass  			

	def shot(self):

		self.game.sound["arrow"].play()
		
		if self.direccionx > 0: self.game.arrow.add(Arrow(self.rect.right +5,self.rect.centery,1,self.game))
		elif self.direccionx < 0: self.game.arrow.add(Arrow(self.rect.left -5,self.rect.centery,-1,self.game))

	def Fundead(self):
		
		if self.dead == True:
			self.fuerza_gravitatoria = 0
			self.vlx = 0
			self.vly = 0

			if self.cont_dead == 10: sound["dead"].play()
			elif self.cont_dead == 20: self.game.effect.add(Dead(self.rect.centerx,self.rect.centery))
			elif self.cont_dead >= 100: self.game.load()

			self.cont_dead +=1


class Arrow(pg.sprite.Sprite):
	def __init__(self,x,y,direccion,game):
		pg.sprite.Sprite.__init__(self)
		self.direccion = direccion

		if self.direccion > 0: self.image = image["arrow"]
		elif self.direccion < 0: self.image = pg.transform.flip(pg.image.load(resolve_route("image/sprites/hug/arrow.png") ),1,0)

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
		if len(self.colision_enemy) > 0: self.kill()

		self.rect.x += self.vl
	
class Dead(pg.sprite.Sprite):
	def __init__(self,x,y):
		pg.sprite.Sprite.__init__(self)
		self.image = image["dead"]
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
