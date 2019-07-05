
import pygame as pg 
import  os 



pg.mixer.init()


def resolve_route(route_relative):
	#if hasattr(sys,"_MEIPASS"):
	#	return os.path.join(sys._MEIPASS,route_relative)
	return os.path.join(os.path.abspath("."),route_relative)

image = {
	"background": pg.image.load(resolve_route("image/background.png")),
	"lemon": pg.image.load(resolve_route("image/lemon.png")),
	"hugo": pg.image.load(resolve_route("image/hug.png")),
	"paty": pg.image.load(resolve_route("image/paty.png")),
	"plataform_movil": pg.image.load(resolve_route("image/plataform.png")),
	"spikes": pg.image.load(resolve_route("image/spikes.png")),
	"key": pg.image.load(resolve_route("image/key.png")),
	"trampoline": pg.image.load( resolve_route("image/trampoline.png")),
	"door": pg.image.load(resolve_route("image/door.png")),
	"fireball": pg.image.load(resolve_route("image/fireball.png")),
	"apple": pg.image.load(resolve_route("image/apple.png")),
	"dead": pg.image.load(resolve_route("image/dead.png")),
	"arrow": pg.image.load(resolve_route("image/arrow.png")),

 }


sound = {	
	
	"jump": pg.mixer.Sound(resolve_route("sound/Jumpa.wav")),
	"arrow": pg.mixer.Sound(resolve_route("sound/arrow_sound.wav")),


	"objs": pg.mixer.Sound(resolve_route("sound/Pickup_Coin.wav")),
	"blip":pg.mixer.Sound(resolve_route("sound/blip.wav")),
	"dead": pg.mixer.Sound(resolve_route("sound/dead.wav")),
}

