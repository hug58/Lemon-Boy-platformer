import pygame
import pytmx
import os

from script import Player
from script import Enemies
from script import Element

pygame.display.init()
pygame.mixer.init()
pygame.font.init()

#pygame.init()

WIDTH = 620
HEIGHT = 480

SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Project Hugo")
pygame.display.set_icon(pygame.image.load(os.path.abspath("") + "/lemon.ico"))
 

class TileMap:
	def __init__(self,filename):
		tm = pytmx.load_pygame(filename,pixelaplha = True)
		self.width = tm.width * tm.tilewidth
		self.height = tm.height * tm.tileheight
		self.tmxdata = tm

	def render(self,surface):
		ti = self.tmxdata.get_tile_image_by_gid
		for layer in self.tmxdata.visible_layers:
			if isinstance(layer,pytmx.TiledTileLayer):
				for x,y,gid in layer:
					tile = ti(gid)
					if tile:
						
						surface.blit(tile,(x* self.tmxdata.tilewidth,y* self.tmxdata.tileheight))
						
	def make_map(self):
		temp_surface = pygame.Surface((self.width,self.height)) #pygame.SRCALPHA
		
		temp_surface.set_colorkey((0,0,0))	
		self.render(temp_surface)
		#temp_surface.convert_alpha()
		
		return temp_surface

class Camera:
	def __init__(self,width,height):
		self.camera = pygame.Rect((0,0),(width,height))
		self.width = width
		self.height = height
	
	def apply(self,entity):
		return entity.rect.move(self.camera.topleft)
	def apply_rect(self,rect):
		return rect.move(self.camera.topleft)
	
	def update(self,target):
		#Targe en negativo para que en caso de llegar al extremo left (positivo) , el movimiento sea 0
		x =-target.rect.x + int(WIDTH/2)
		y = -target.rect.y + int(HEIGHT/2)
		#print(x)
		#limit scrolling to map size
		x = min(0,x) #left
		y = min(0,y) #top
		#print(self.width)
		#lógica inversa
		#Si -(self.width - WIDTH) es menor que X, X seguira avanzando, en caso contrario X se mantendrá fijo
		x = max(-(self.width - WIDTH),x)#right
		y = max(-(self.height-HEIGHT),y)
		self.camera = pygame.Rect(x,y,self.width,self.height)

class Plataform(pygame.sprite.Sprite):
	def __init__(self,x,y,w,h):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect((x,y),(w,h))
		self.rect.x = x
		self.rect.y = y

class Spikes(pygame.sprite.Sprite):
	def __init__(self,x,y,w,h,game):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect((x,y),(w,h))
		self.rect.x = x
		self.rect.y = y
		self.game = game

	def update(self):
		if self.rect.colliderect(self.game.player.rect):
			self.game.player.dead = True

		for enemy in self.game.enemies:
			if self.rect.colliderect(enemy.rect):
				enemy.kill()

class Sound:
	def __init__(self):
		self.ruta_sound = os.path.abspath("") + "/sound/"
		self.sound_jump = pygame.mixer.Sound(self.ruta_sound + "Jumpa.wav")
		self.sound_arrow = pygame.mixer.Sound(self.ruta_sound + "arrow_sound.wav")
		self.sound_object = pygame.mixer.Sound(self.ruta_sound + "Pickup_Coin.wav")
		self.blip = pygame.mixer.Sound(self.ruta_sound + "blip.wav")

class Paused:
	def __init__(self):
		self.exit = True
		self.clock = pygame.time.Clock()
	def update(self):
		while self.exit == False:
			self.clock.tick(30)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.exit = True

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						self.exit = True

class Menu:
	def __init__(self,maps):
		self.maps = maps
		self.font = pygame.font.Font("Pixel Digivolve.otf",30)
		self.clock = pygame.time.Clock()
		self.lemon =  pygame.transform.scale(pygame.image.load(os.path.abspath("") + "/image/lemon.png"),(30,30))
		self.exit = False
		self.sound = Sound()
		self.color_selection = pygame.Color("#DBAE09")
		self.color_base = pygame.Color("#C4C4C4")
		self.position = 1
		self.changes_maps = False

	def update(self):

		lemon_pos = {1:(0,0),2:(0,40), 3:(0,80)}
		position = 1

		text_partida = self.font.render("Start Game ",2,self.color_base)
		text_about = self.font.render("About",2,self.color_base)
		text_exit = self.font.render("Exit",2,self.color_base)
		text_twitter = self.font.render("@hug588",2,pygame.Color("#1CA4F4"))
		
		texto = (text_partida,text_about,text_exit,text_twitter)
		
		surface = pygame.Surface((620,480))
		surface = self.apply(surface,texto)
		
		

		while self.exit == False:
			self.clock.tick(30)
	
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:

						if position == 1:
							self.exit = True
							self.changes()

						elif position == 2:							
							self.about()
							self.sound.blip.stop()							
							self.sound.blip.play()

						elif position == 3:
							pygame.quit()

					elif event.key == pygame.K_DOWN:
						if position < 3:
							position +=1
							self.sound.blip.stop()
							self.sound.blip.play()

					elif event.key == pygame.K_UP:
						if position > 1:
							position -=1
							self.sound.blip.stop()
							self.sound.blip.play()
							

			#for i in range(len(texto)):	
			#	if i +1 == position:
			#		texto[i].fill(self.color_selection)
			#	else:
			#		texto[i].fill(self.color_base)				
			#surface = self.apply(texto)
			


			SCREEN.blit(surface,(0,0))
			SCREEN.blit(self.lemon,lemon_pos[position])
			pygame.display.flip()


	def apply(self,surface,args,x= 30,y = 0,space_line = 0):
		#surface = pygame.Surface((620,480))
		surface.fill(pygame.Color("#0C040C"))
		cont = 0

		for text in args:
			surface.blit(text,(x,y))
			cont +=1
			if space_line > 0 and cont == space_line:
				y +=80
				cont = 0

			else:
				y += 40

		return surface

	def about(self,exit = False):
		text_hug = self.font.render("Developer/programmer: Hugo  ",2,self.color_base)
		text_twitter_hug = self.font.render("@hug588",2,pygame.Color("#1CA4F4"))

		text_paty = self.font.render("Artist: Patricia",2,self.color_base)
		text_facebook_paty = self.font.render("The pash team",2,pygame.Color("#3C5C9C"))

		text_return = self.font.render("Return",2,self.color_base)
		texto = (text_hug,text_twitter_hug,text_paty,text_facebook_paty)

		surface = pygame.Surface((620,480))
		surface = self.apply(surface,texto,space_line= 2)
		surface.blit(text_return,(40,440))
		
		
		while exit == False:

			self.clock.tick(30)
	
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						exit = True
						self.sound.blip.stop()
						self.sound.blip.play()
						


					

			SCREEN.blit(surface,(0,0))
			SCREEN.blit(self.lemon,(0,440))
			pygame.display.flip()

	def changes(self,exit = False):
		surface = pygame.Surface((620,480))
		surface_selection = pygame.Surface((200,40))

		texto = [self.font.render( "Map {}".format(i+1),2,self.color_base) for i in range(len(self.maps))]
		position = 1
		y_move = 0
		surface_selection = self.apply(surface_selection,texto,y = y_move)
		surface.fill(pygame.Color("#0C040C"))
		SCREEN.blit(surface,(0,0))

		while exit == False:

			self.clock.tick(30)
	
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						self.position = position -1
						self.changes_maps = True
						exit = True
					

					elif event.key == pygame.K_DOWN:
						if position < len(self.maps):
							y_move -=40
							surface_selection = self.apply(surface_selection,texto,y = y_move)
							position +=1

					elif event.key == pygame.K_UP:
						if position > 1:
							y_move +=40
							surface_selection = self.apply(surface_selection,texto,y = y_move)	
							position -=1


			SCREEN.blit(surface_selection,(240,100))	
			#SCREEN.blit(self.lemon,(0,440))
			pygame.display.flip()




class Game:
	
	def __init__(self,maps):
		#self.maps= ["map/map4.tmx","map/map3.tmx","map/map2.tmx","map/map1.tmx"]
		self.maps = maps
		self.sound = Sound()
		self.map_cont = 0
		self.map = TileMap(self.maps[self.map_cont])
		self.Mapimage = self.map.make_map()
		self.Maprect = self.Mapimage.get_rect()
		self.camera = Camera(self.map.width,self.map.height)
		self.changes_maps = False
		#self.arrow = []

						
	def load(self):
		
		self.arrow = pygame.sprite.Group()
		self.plataform = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		self.objs = pygame.sprite.Group()
		self.spike = pygame.sprite.Group()
		self.trap = pygame.sprite.Group()
		self.fire_cannon = pygame.sprite.Group()

		for sprite in self.map.tmxdata.objectgroups:
			for tile_object in sprite:
				if tile_object.name == "Player":
					self.player = Player.Player(tile_object.x,tile_object.y,self)

		for tile_object in self.map.tmxdata.objects:
			if tile_object.name == "Door":
				if tile_object.type == "YELLOW":
					self.objs.add(Element.Door(tile_object.x,tile_object.y,self,"YELLOW"))
			
			elif tile_object.name == "Spike_trap":
				if tile_object.type == "right":
					self.trap.add(Element.Trap(tile_object.x,tile_object.y,self,"right"))
				else:
					self.trap.add(Element.Trap(tile_object.x,tile_object.y,self))

			elif tile_object.name == "plataform":
				self.plataform.add(Plataform(tile_object.x,tile_object.y,tile_object.width,tile_object.height))

			elif tile_object.name == "Apple":
				if tile_object.type == "left":
					self.enemies.add(Enemies.Apple(tile_object.x,tile_object.y,self,"left"))
				elif tile_object.type == "right":
					self.enemies.add(Enemies.Apple(tile_object.x,tile_object.y,self,"right"))
			
			elif tile_object.name == "Spike":
				self.spike.add(Spikes(tile_object.x,tile_object.y,tile_object.width,tile_object.height,self))

			elif tile_object.name == "Fire_cannon":
				
				if tile_object.type == "left":
					self.fire_cannon.add(Element.Fire_Cannon(tile_object.x,tile_object.y,self, "left"))

				else:
					self.fire_cannon.add(Element.Fire_Cannon(tile_object.x,tile_object.y,self))

			elif tile_object.name == "Key":
				self.objs.add(Element.Key(tile_object.x,tile_object.y,self))


			elif tile_object.name == "jump":
				self.objs.add(Element.Trampoline(tile_object.x,tile_object.y,self))

			elif tile_object.name == "Lemon":
				self.objs.add(Element.Lemon(tile_object.x,tile_object.y,self))
		
	def update(self):
		self.camera.update(self.player)
		self.spike.update()
		self.trap.update()
		self.fire_cannon.update()
		self.arrow.update()
		self.enemies.update()
		for objs in self.objs:
			
			objs.update()

			try:
				if objs.next == True:
					if self.map_cont < len(self.maps) -1:
						self.map_cont +=1
					else:
						self.map_cont = 0
					self.map =  TileMap(self.maps[self.map_cont])
					self.Mapimage = self.map.make_map()
					self.Maprect = self.Mapimage.get_rect()
					self.camera = Camera(self.map.width,self.map.height)
					self.load()
					
			except:
				pass

		if self.changes_maps == True:
			self.map =  TileMap(self.maps[self.map_cont])
			self.Mapimage = self.map.make_map()
			self.Maprect = self.Mapimage.get_rect()
			self.camera = Camera(self.map.width,self.map.height)
			self.load()
			self.changes_maps = False			

		if self.player.dead == True:
			self.load()
		
		self.player.update()

	def draw(self):

		SCREEN.fill(pygame.Color("#A0A0A0"))
		
		for arrow in self.arrow:
			SCREEN.blit(arrow.image,self.camera.apply(arrow))

		SCREEN.blit(self.Mapimage,self.camera.apply_rect(self.Maprect))	

		for cannon in self.fire_cannon:
			for fireball in cannon.fireball:
				SCREEN.blit(fireball.image,self.camera.apply(fireball))
		

		
		for enemies in self.enemies:
			SCREEN.blit(enemies.image,self.camera.apply(enemies))	
		for objs in self.objs:
			SCREEN.blit(objs.image,self.camera.apply(objs))

		SCREEN.blit(self.player.image,self.camera.apply(self.player))

		for trap in self.trap:
			SCREEN.blit(trap.image,self.camera.apply(trap))
		
			
def Main():

	exit = False
	clock = pygame.time.Clock()

	maps= ["map/map4.tmx","map/map3.tmx","map/map2.tmx","map/map1.tmx"]
	menu = Menu(maps)
	game = Game(menu.maps)
	

	game.load()

	while exit == False:
		clock.tick(60)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_x:
					if game.player.cont_jump > 0:
						game.sound.sound_jump.stop()
						game.sound.sound_jump.play()
						game.player.vly = -8
						game.player.cont_jump -=1
						game.player.direcciony = -1
				if event.key == pygame.K_RETURN:
					menu.exit = False

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
					game.player.stop = True

				if event.key == pygame.K_c:
					if game.player.cont_shot >= 13:
						game.player.cont_shot = 0
						game.player.shot()

					else:
						game.player.cont_shot = 0
			

		if menu.changes_maps == True:
			game.map_cont = menu.position
			print(game.map_cont)
			game.changes_maps = True
			menu.changes_maps = False


		menu.update()
		game.update()
		game.draw()
		pygame.display.flip()


if __name__ == "__main__":
	Main()
	pygame.quit()
