
	def generar_old(self):
		self.barra.restablecido()
		"""
		#ESCALERAS
		"""


		if len(self.lista_escalerax) > 0:
			for i in range(len(self.lista_escalerax)):
				small = Elementos.Block(self.lista_escalerax[i],self.lista_escaleray[i],(20,20,),(0,20))
				self.group_general.add(small)
				self.escalera.add(small)


		"""
		#PAREDES GROUP INMOVIL
		"""

		if len(self.paredesx) > 0:
			for i in range(len(self.paredesx)):
				pared = Elementos.Block(self.paredesx[i],self.paredesy[i],self.trozo_paredes[i],self.pos_paredes[i])
				pared.color = self.color
				self.group_general.add(pared)
				self.group_inmovil.add(pared)

		"""
		#PISOS USA GROUP INMOVIL
		"""

		if len(self.lista_pisox) > 0:
			for i in range(len(self.lista_pisox)):
				piso = Elementos.Block(self.lista_pisox[i],self.lista_pisoy[i],self.trozo_piso[i],self.pos_piso[i])
				piso.scale2x()
				piso.add(self.group_general)	
				piso.add(self.group_inmovil)	


		
		"""
		#PARED PARKOUR
		#EN PRUEBA

		"""

		#if len(self.pared_parkourx) > 0:
		#	for i in range(len(self.pared_parkourx)):
		#		pared_parkour = Elementos.Block(self.pared_parkourx[i],self.pared_parkoury[i],self.trozo_parkour[i],self.pos_parkour[i])
		#		pared_parkour.add(self.group_general)
		#		pared_parkour.add(self.group_prueba)

		"""
			#TRAMPOLINES
		"""


		if len(self.list_trampolinx) > 0:
			for i in range(len(self.list_trampolinx)):
				tramp = Elementos.Trampolin(self.list_trampolinx[i],self.list_trampoliny[i],self.group_trampolin)
				self.group_general.add(tramp)

		"""
			#LIMONES
		"""

		if len(self.list_limonsitosx) > 0:
			for i in range(len(self.list_limonsitosx)):
				lemon = Elementos.Lemon(self.list_limonsitosx[i],self.list_limonsitosy[i],self.group_lemones)
				self.group_general.add(lemon)


		"""
		#PÚAS NORMALES
		"""

		if len(self.list_puasx)> 0:
			for i in range(len(self.list_puasx)):
				puas = Elementos.Puas(self.list_puasx[i],self.list_puasy[i])
				self.group_general.add(puas)
				self.group_dead.add(puas)


		"""
		#LLAVE
		"""
		self.llave = Elementos.Llave(self.llave_posx,self.llave_posy)
		self.group_general.add(self.llave)


		"""
		#PUERTA
		"""

		self.puerta = Elementos.Puerta(self.puerta_posx,self.puerta_posy)
		self.group_general.add(self.puerta)


		"""
		#PLAYER
		"""

		self.player = Player.Player(self.player_posx,self.player_posy)
		self.player.color =self.color
		self.group_general.add(self.player)

		"""
		#ENEMY
		"""


		self.enemy = Player.Enemy(self.group_enemy,self.enemy_posx,self.enemy_posy,self.player)
		self.group_general.add(self.enemy)


class Nivel1(Nivel):
	def __init__(self):	
		Nivel.__init__(self)
		self.prox_nivel = Nivel2()
		self.prox_escena = None

		#color de nivel
		self.color = (4,175,238)	

		#block_small escaleras
		self.lista_escalerax = []
		self.lista_escaleray = []
		self.destruir = []


		#PISOS LARGOS
		self.lista_pisox = [0,0,100]
		self.lista_pisoy = [340,660,660]
		self.trozo_piso = [(900,40),(1000,40),(100,40)] 
		self.pos_piso = [(0,0)]*3




		"""
		#PAREDES Y OBSTACULOS
		"""

		self.paredesx = []
		self.paredesy = []
		self.trozo_paredes = []
		self.pos_paredes = []
		cont = 480

		"""
		#GENERADOR DE OBSTACULOS
		"""

		for i in range(2):
			
			self.paredesy.append(205)
			self.paredesx.append(cont)
			self.trozo_paredes.append((20,140))
			self.pos_paredes.append((0,20))
			
			cont +=20

		cont = 580
		for i in range(2):

			self.paredesy.append(280)
			self.paredesx.append(cont)
			self.trozo_paredes.append((20,60))
			self.pos_paredes.append((0,20))
			cont +=20



		#cont = 570 
		cont = 225
		for i in range(3):
			#cont = 570
			self.paredesy.append(540)
			self.paredesx.append(cont)
			self.trozo_paredes.append((20,120))
			self.pos_paredes.append((0,20))

			cont +=20

		cont = 225
		#contx = 225
		for i in range(3):
			#cont = 360
			self.paredesy.append(360)
			self.paredesx.append(cont)
			self.trozo_paredes.append((20,110))
			self.pos_paredes.append((0,40))

			cont += 20


		"""
		#PARED DERECHA 
		#	Nota = se puede hacer un salto por los lados
		
		"""
		self.pared_parkourx = []
		self.pared_parkoury = []
		self.trozo_parkour = []
		self.pos_parkour = []
		
		cont = 0
		for i in range(6):
			self.pared_parkoury.append(cont)
			self.pared_parkourx.append(980)
			self.trozo_parkour.append((20,120))
			self.pos_parkour.append((0,40))
			cont += 120

		
		"""
		#PARED IZQUIERDA

		"""

		
		cont = 340
		for i in range(2):
			self.pared_parkoury.append(cont)
			self.pared_parkourx.append(880)
			self.trozo_parkour.append((20,130))
			
			if i == 0:
				self.pos_parkour.append((0,20))
			else:
				self.pos_parkour.append((0,20))

			cont += 120



		#Puas
		self.list_puasx = [232,250,268,550]
		self.list_puasy = [559,559,559,self.lista_pisoy[0]-10]


		#Trampolines
		self.list_trampolinx = [120,330,660,580+6]
		self.list_trampoliny = [660,660,self.lista_pisoy[0]-20	,280-20]

				
	
		"""
		#CONFIGURACIÓN BASICA
		"""
	
		#llave posicion
		self.llave_posx = 480 + 20
		self.llave_posy = 220 -40

		#Puerta posicion
		self.puerta_posx = 10
		self.puerta_posy = self.lista_pisoy[0]


		#sprite posicion
		self.player_posx = 600
		self.player_posy = 200

		#Enemy
		self.enemy_posy = 320
		self.enemy_posx = 200 

		#Lemones
		self.list_limonsitosx = [400]
		self.list_limonsitosy = [650]

class Nivel2(Nivel):
	def __init__(self):
		Nivel.__init__(self)
		self.prox_nivel = None
		self.prox_escena = None

		#color de nivel
		self.color = (4,175,238)	

		#block_big ascensores
		self.list_block_x = [911]
		self.list_block_y = [360]
		self.mov_vertical = [False]
		self.mov_horizontal = [None]
		
		#VELOCIDAD DE ASCENSORES
		self.vl = [1,1]

		#block_small escaleras
		self.lista_escalerax = []
		self.lista_escaleray = []
		self.destruir = []
		cont = 550
		conty = 670
		for i in range(10):

			#if i < 5 or i > 6: 

			self.lista_escalerax.append(cont)
			self.lista_escaleray.append(conty)

			conty -=20
			cont += 35
				
		#PISOS LARGOS
		self.lista_pisox = [0]
		self.lista_pisoy = [340]
		self.ancho_piso = [900]
		self.largo_piso = [20]

	
		"""
		#ESTA ES LA CONFIGURACIÓN DE LA LLAVE
		"""
	
		#llave posicion
		self.llave_posx = 480 + 20
		self.llave_posy = 220 -40

		#Puerta posicion
		self.puerta_posx = 10
		self.puerta_posy = self.lista_pisoy[0]


		#sprite posicion
		self.player_posx = 300
		self.player_posy = 230



		#Paredes o obstaculos

		self.paredesx = [580]
							  #ABAJO
		self.paredesy = [570]
		self.trozo_paredes = [(40,20)]


		#Puas
		self.list_puasx = [232,250,268]
		self.list_puasy = [559,559,559]


		#Trampolines
		self.list_trampolinx = [169,330,660,580+6]
		self.list_trampoliny = [660,660,self.lista_pisoy[0]-20	,280-20]


		#Enemy
		self.enemy_posy = 340
		self.enemy_posx = 200 

		#Lemones
		self.list_limonsitosx = [400]
		self.list_limonsitosy = [650]


		def __str__(self):
			return "Estás en el nivel 2" 

class Nivel3(Nivel):
	def __init__(self):
		pass

	def update(self):
		pass


