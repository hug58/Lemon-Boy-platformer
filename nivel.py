
import pygame
import colisiones



from sprites import Player
from sprites import Elementos



ANCHO,ALTO = 1000,520

"""	Nota:
	Crear menú de objetos obtenidos
	Mejorar la decteción de colisión con respecto al salto	
"""
	
map1 =[ "#------------------------",
			"#------------------------",
			"#------------------------",
			"##-----------------------",
			"#E-------P-------B-----S-",
			"####---###-----####---###",
			"#-----XX#-----#######--##",
			"#-----###-----########--#",
			"##------#-----####-----##",
			"#X----###-----####----###",
			"##------------L------####",
			"####------XX--###########",
			"#########################"]
map2 =[ "#########################",
			"#-----------------------#",
			"#-----------------------#",
			"#-----XX----------------#",
			"#L-x--##-T-P------------#",
			"#####---###########---###",
			"#-------------------#--##",
			"#-------------####-###--#",
			"##----------B#---------##",
			"#X--------#####------x###",
			"###----X#########----####",
			"#-E---#############X---S-",
			"#########################"] 				

map3 =	 [  "#########################",
			"###----------------------",
			"##-----------------------",
			"#-----------------B----S-",
			"#-----------T---X########",
			"###---#######---#-------#",
			"#-P-#-----#-------------#",
			"#######X----#--##-----L-#",
			"#------##----------x-##-#",
			"#--------##--------#----#",
			"#------------##---------#",
			"#E---------------##-----#",
			"#########################"]

map4 =[ "#########################",
			"#-----------------------#",
			"#------------L----------#",
			"#-----------##----------#",
			"#-------P-B---T-X##--####",
			"#-------####--#-##-----##",
			"#---------------##-------",
			"#-----------T---##-X-X---",
			"#E----------#---##-#-#---",
			"##------------T-##-----S-",
			"#--P##--##----#-##--#--##",
			"#XX###XXX#X##XXXX#XXX#---",
			"#########################"]

map5 =		[ "#########################",
			"#-----------------------#",
			"#-----------------------#",
			"#-----------------------#",
			"#-----------------------#",
			"#-----------------------#",
			"#-----------------------#",
			"#-----------------------#",
			"#-----------------------#",
			"#-----------------------#",
			"#------------------------",
			"#E-L-------------------S-",
			"#########################"] 

class Nivel(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.group_general = pygame.sprite.Group()
		self.group_inmovil = pygame.sprite.Group()
		self.group_trampolin = pygame.sprite.Group()
		self.group_dead = pygame.sprite.Group()
		self.group_lemones = pygame.sprite.Group()
		self.group_enemy = pygame.sprite.Group()
		self.group_sprites = pygame.sprite.Group()

		"""
				ALFHA RECOSTRUIR
									"""

		self.prox_nivel = None
		self.prox_escena = None
		self.colision = colisiones.Colisiones()
		
		self.cont  = 0
		self.maps = [map1,map2,map3,map4,map5]
		self.map = self.maps[0]
		

	def update(self):
		self.group_general.update()
		self.player.update()		


		for sprites in self.group_sprites:
			self.colision.estaticos(sprites,self.group_inmovil)
			self.colision.salto(sprites,self.group_trampolin)
			self.colision.muerto(sprites,self.group_dead,self.llave)
			self.colision.lemon(sprites,self.group_lemones)	
			

		if self.player.rect.colliderect(self.llave.rect):

			self.player.llave = True
			self.llave.kill()
			
		if self.player.rect.colliderect(self.puerta.rect):
			if self.player.llave == True:
				
				self.cont +=1
				self.map = self.maps[self.cont]
				self.puerta.activar_animacion = True


	def draw(self,VENTANA):
		
		self.group_general.draw(VENTANA)
		VENTANA.blit(self.player.image,self.player.rect)

	

	def generate(self):


		x = 0
		y = 0

		for i in range(len(self.map)):
			self.map[i] = list(self.map[i])



		for i in range(len(self.map)):
			for j in range(len(self.map[0])):
				if self.map[i][j] == "E":
					self.player = None
					j = Player.Player(x,y)
					self.player = j
					self.group_sprites.add(j)


				elif self.map[i][j] == "#":
					j = Elementos.Block(x,y,(20*2,20*2),(0,0))
					j.scale2x()
					self.group_general.add(j)
					self.group_inmovil.add(j)

				elif self.map[i][j] == "X":
					j = Elementos.Puas(x,y)
					self.group_general.add(j)
					self.group_dead.add(j)

				elif self.map[i][j] == "S":
					j = Elementos.Puerta(x,y)
					self.puerta = j
					self.group_general.add(j)
					
				elif self.map[i][j] == "-":
					pass  

				elif self.map[i][j] == "P":
					j = Elementos.Lemon(x,y)
					self.group_general.add(j)
					self.group_lemones.add(j)

				elif self.map[i][j] == "L":
					j = Elementos.Llave(x,y)
					self.group_general.add(j)
					self.llave = j

				elif self.map[i][j] == "T":
					j = Elementos.Trampolin(x,y)
					self.group_general.add(j)
					self.group_trampolin.add(j)

				elif self.map[i][j] == "B":	
					j = Player.Enemy(x,y)
					self.group_general.add(j)
					self.group_enemy.add(j)
					self.group_sprites.add(j)


				x +=40




			x = 0
			y +=40

		for i in self.group_enemy:
			i.player = self.player
		#x,y = 0,0




		"""for i in range(len(self.map)):
			for j in range(len(self.map[0])):
				if self.map[i][j] == "B":	
					j = Player.Enemy(x,y,self.player)
					self.group_general.add(j)
					self.group_enemy.add(j)					
					break

				x +=40

			x = 0
			y +=40

		

		print(len(self.group_enemy))
		"""
