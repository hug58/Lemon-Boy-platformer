import pygame
import math

class Colisiones(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.colision_escalera = None
		self.colision_block = None
		self.colision_paredes = None
		self.colision_trampolin = None
		self.colision_dead = None
		self.colision_inmovil = None
		self.colision_lemon = None
		self.distancia = 0

	def paredes(self,player,group):
		self.colision_paredes = pygame.sprite.spritecollide(player,group,False)

		for block in self.colision_paredes:
			
			#if not player.vlx < 0 and not player.vlx >0:
			#	player.vly -=1.5 

			if 	player.vly < 0: 
				player.vly -=1
				if player.vlx > 0 and player.direccionx > 0:
					player.vlx = -14
					player.vly = 0
				elif player.vlx < 0 and player.direccionx < 0:
					player.vlx =14
					player.vly = 0
				
				#player.direccionx *=-1



			if player.rect.left < block.rect.left and player.rect.right >= block.rect.left:
				player.rect.right = block.rect.left 

			elif player.rect.right > block.rect.right and player.rect.left <= block.rect.right:
				player.rect.left = block.rect.right 

	def estaticos(self,player,group):

		self.colision_inmovil =  pygame.sprite.spritecollide(player,group,False)

		for block in self.colision_inmovil:

			if player.rect.top < block.rect.top and player.rect.bottom < block.rect.bottom and	player.rect.left < block.rect.right and player.rect.right > block.rect.left:	
					player.vly = 0
					
					player.rect.bottom = block.rect.top 				
					
			elif player.rect.left < block.rect.left:
				player.rect.right = block.rect.left 
						
			elif player.rect.right > block.rect.right:
				player.rect.left = block.rect.right 

			elif player.rect.bottom >= block.rect.bottom:
				player.rect.top = block.rect.bottom

				

	def ascensores(self,player,group):

		self.colision_block =  pygame.sprite.spritecollide(player,group,False)

				
		for block in self.colision_block:
	 
			if player.rect.top < block.rect.top and player.rect.bottom < block.rect.bottom and	player.rect.x < block.rect.right and player.rect.right > block.rect.left:
				player.rect.bottom = block.rect.top 
				block.activar = True
				#player.vlx = block.vlx
				#BUG 0.3
				#player.vly = block.vly
				player.vly = 0
				#player.vlx = 0
				
			elif player.rect.left < block.rect.left:
				player.rect.right = block.rect.left

			elif player.rect.right > block.rect.right:
				player.rect.left = block.rect.right

			
	def escaleras(self,player,group):
		
		
		self.colision_escalera =  pygame.sprite.spritecollide(player,group,False)
		for scall in self.colision_escalera:
			pass
			#scall.destruir(False,self.escalera,self.group_general,self.group_temporal)
			
			#if player.vlx < 0:
			#	player.rect.bottom = scall.rect.top 
			#if player.vlx > 0:
			#	player.rect.bottom = scall.rect.top 
			
		for scall in self.colision_escalera:

			if player.rect.top < scall.rect.top:
				player.rect.bottom = scall.rect.top
			#	player.vlx = scall.vlx
				player.vly = 0
				
			#if player.rect.bottom > scall.rect.bottom:
			#	player.rect.top = player.rect.bottom

	def salto(self,player,group):
		

		self.colision_trampolin = pygame.sprite.spritecollide(player,group,False)

		for trampolin in self.colision_trampolin:
			player.rect.bottom = trampolin.rect.top
			player.vly = trampolin.jump()
			trampolin.activar_animacion = True

	def muerto(self,player,group,llave):
		
		self.colision_dead = pygame.sprite.spritecollide(player,group,False)
		
		
		for dead in self.colision_dead:
			#player.rect.x = player_posx
			#player.rect.y = ALTO- player.rect.height 
			llave.vlx = 0
			llave.vly = 0
			llave.rect.x = llave.llave_posx
			llave.rect.y = llave.llave_posy
			player.vlx = 0
			player.vly = 0
			player.dead = True
			player.rect.bottom = dead.rect.top +27

	def lemon(self,player,group):
		self.colision_lemon = pygame.sprite.spritecollide(player,group,False)
		

		for lemon in self.colision_lemon:
			#player.estado = 0
			lemon.kill()
	
		
	