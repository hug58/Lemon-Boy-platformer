from script import *
from script.menu import Menu
from script import image,sound,resolve_route
from script.player import Player
from script.enemy import Apple
from script.elementos import Trap,Door,Trampoline,Key,Lemon
from script.camera import Camera
from script.tilemap import TileMap


pg.display.init()
pg.joystick.init()
pg.font.init()

WIDTH = 620
HEIGHT = 480

WHITE2 =  (252,252,238)
LEMON = (249,215,0)
GREEN = (140,196,51)


SCREEN = pg.display.set_mode((WIDTH,HEIGHT))

pg.display.set_caption("Project Hugo")
pg.display.set_icon(pg.image.load(resolve_route("lemon.ico") ))
 

class Plataform(pg.sprite.Sprite):
	def __init__(self,x,y,w,h):
		pg.sprite.Sprite.__init__(self)
		self.rect = pg.Rect((x,y),(w,h))
		self.rect.x = x
		self.rect.y = y
		self.vlx = 0

class Spikes(pg.sprite.Sprite):
	def __init__(self,x,y,w,h,game):
		pg.sprite.Sprite.__init__(self)
		self.rect = pg.Rect((x,y),(w,h))
		self.rect.x = x
		self.rect.y = y
		self.game = game

	def update(self):
		if self.rect.colliderect(self.game.player.rect):
			self.game.player.dead = True

		for enemy in self.game.enemies:
			if self.rect.colliderect(enemy.rect):
				enemy.kill()



class Game:
	
	def __init__(self,maps):
		self.maps = maps
		self.sound = sound
		self.map_cont = 0
		self.map = TileMap(self.maps[self.map_cont])
		self.Mapimage = self.map.make_map()
		self.Maprect = self.Mapimage.get_rect()
		self.surface_size = (WIDTH,HEIGHT)
		self.camera = Camera(self.map.width,self.map.height,self.surface_size)
		self.changes_maps = False

		#Es más rápido crear otra Surface que dibujarlo directamente en la pantalla
								
	def load(self):

		self.effect = pg.sprite.Group()	
		self.arrow = pg.sprite.Group()
		self.plataform = pg.sprite.Group()
		self.plataform_m = pg.sprite.Group()
		self.enemies = pg.sprite.Group()
		self.objs = pg.sprite.Group()
		self.spike = pg.sprite.Group()
		self.trap = pg.sprite.Group()
		self.fire_cannon = pg.sprite.Group()

		for sprite in self.map.tmxdata.objectgroups:
			for tile_object in sprite:
				if tile_object.name == "Player": 
					self.player = Player(tile_object.x,
									tile_object.y,self)

		for tile_object in self.map.tmxdata.objects:
			if tile_object.name == "plataform": 
				self.plataform.add(
					Plataform(tile_object.x,
						tile_object.y,
						tile_object.width,
						tile_object.height)
					)
			elif tile_object.name == "Door": 
				self.objs.add(
					Door(tile_object.x,
						tile_object.y,
						self,"YELLOW"))
			elif tile_object.name == "Apple": 
				self.enemies.add(
					Apple(tile_object
						.x,tile_object.y,
						self,tile_object.type))
			elif tile_object.name == "Key": 
				self.objs.add(
					Key(tile_object.x,
						tile_object.y,
						self))
			elif tile_object.name == "Lemon": 
				self.objs.add(
					Lemon(tile_object.x,
						tile_object.y,
						self))
			elif tile_object.name == "Spike_trap": 
				self.trap.add(
					Trap(tile_object.x,
						tile_object.y,
						self,tile_object.type))
			elif tile_object.name == "plataform_m": 
				self.plataform_m.add(
					plataform_m(
						tile_object.x,
						tile_object.y,
						tile_object.type))	
			elif tile_object.name == "Spike": 
				self.spike.add(
					Spikes(tile_object.x,
						tile_object.y,
						tile_object.width,
						tile_object.height,
						self))
			elif tile_object.name == "Fire_cannon": 
				self.fire_cannon.add(
					Fire_Cannon(
						tile_object.x,
						tile_object.y,
						self, 
						tile_object.type))				
			elif tile_object.name == "jump": self.objs.add(
					Trampoline(
						tile_object.x,
						tile_object.y,
						self))
		
	def update(self):
		
		self.camera.update(self.player)
		self.spike.update()
		self.trap.update()
		self.fire_cannon.update()
		self.arrow.update()
		self.enemies.update()
		self.plataform_m.update()
		self.effect.update()
		
		for objs in self.objs:	
			objs.update()

			try:
				if objs.next == True:
					
					if self.map_cont < len(self.maps) -1: self.map_cont +=1
					else: self.map_cont = 0

					self.map =  TileMap(self.maps[self.map_cont])
					self.Mapimage = self.map.make_map()
					self.Maprect = self.Mapimage.get_rect()
					self.camera = Camera(self.map.width,self.map.height)
					self.load()
					
			except  Exception  as e: pass

		if self.changes_maps == True:
		
			self.map =  TileMap(self.maps[self.map_cont])
			self.Mapimage = self.map.make_map()
			self.Maprect = self.Mapimage.get_rect()
			self.camera = Camera(self.map.width,self.map.height,self.surface_size)
			self.load()
			self.changes_maps = False			

		self.player.update()

	def draw(self):


		for arrow in self.arrow:
			SCREEN.blit(arrow.image,self.camera.apply(arrow))
		
		SCREEN.blit(self.Mapimage,self.camera.apply_rect(self.Maprect))
		
		for plataform_m in self.plataform_m: 
			SCREEN.blit(plataform_m.image,self.camera.apply(plataform_m))	 
		
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


		for effect in self.effect:
			SCREEN.blit(effect.image,self.camera.apply(effect))


def main():

	exit = False
	clock = pg.time.Clock()
	maps= ["map/map1.tmx",
			"map/map2.tmx",
			"map/map3.tmx",
			"map/map4.tmx",
			"map/map5.tmx",
			"map/map6.tmx",
			"map/map7.tmx"]

	menu = Menu(maps)
	game = Game(menu.maps)
	game.load()
	

	#Creando un objeto joystick e iniciando

	joystick =  pg.joystick.Joystick(0)  if pg.joystick.get_count() > 0 else None
	joystick.init() if joystick != None else None


	background = pg.Surface((WIDTH,HEIGHT)).convert()
	background.blit(pg.transform.scale(image["background"],(WIDTH,HEIGHT)),(0,0))
	draw_background = lambda background: SCREEN.blit(background,(0,0))
		

	while exit != True and menu.exit_game != True:
		clock.tick(60)
		
		for event in pg.event.get():
			if event.type == pg.QUIT: exit = True
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_x:
					if game.player.cont_jump > 0:
						game.player.diffx = 0

						game.sound["jump"].stop()
						game.sound["jump"].play()

						game.player.vly = -8
						game.player.cont_jump -=1
						game.player.direcciony = -1

				if event.key == pg.K_RETURN: menu.exit = False

			if event.type == pg.KEYUP:
				if event.key == pg.K_RIGHT or event.key == pg.K_LEFT: game.player.stop = True
				if event.key == pg.K_c:
					if game.player.cont_shot >= 13:
						game.player.shot()
						game.player.cont_shot = 0
					else: game.player.cont_shot = 0
			
		if menu.changes_maps == True:
			game.map_cont = menu.position
			game.changes_maps = True
			menu.changes_maps = False
		
		if menu.exit != True: 
			menu.update(SCREEN)
		
		draw_background(background)

		#Cerrar el videojuego completamente sin pasar por dibujar el nivel actual(lvl1 por defecto)
		if menu.exit_game != True: 
			game.draw()


		game.update()
		pg.display.flip()

if __name__ == "__main__":
	main()
