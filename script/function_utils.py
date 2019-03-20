import os.path, sys

def resolve_route(route_relative):
	if hasattr(sys,"_MEIPASS"):
		return os.path.join(sys._MEIPASS,route_relative)
	return os.path.join(os.path.abspath("."),route_relative)

