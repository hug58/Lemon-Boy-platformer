from script import *

class Camera:
	def __init__(self,width,height,size):
		self.camera = pg.Rect((0,0),(width,height))
		self.width = width
		self.height = height

		self.size_width = size[0]
		self.size_height = size[1]
	
	def apply(self,entity):
		return entity.rect.move(self.camera.topleft)
	def apply_rect(self,rect):
		#mueve la posición de la surface a la pos de la camara en topleft (arriba/izquierda)
		return rect.move(self.camera.topleft)
	
	def update(self,target):
		#Targe en negativo para que en caso de llegar al extremo left (positivo) , el movimiento sea 0
		x =-target.rect.x + int(self.size_width/2)
		y = -target.rect.y + int(self.size_height/2)
		#print(x)
		#limit scrolling to map size
		x = min(0,x) #left
		y = min(0,y) #top
		#print(self.width)
		#lógica inversa
		#Si -(self.width - WIDTH) es menor que X, X seguira avanzando, en caso contrario X se mantendrá fijo
		x = max(-(self.width - self.size_width),x)#right
		y = max(-(self.height-self.size_height),y)
		self.camera = pg.Rect(x,y,self.width,self.height)