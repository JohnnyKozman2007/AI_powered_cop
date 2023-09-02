import pygame 

class Tile(pygame.sprite.Sprite):
	tiles = []
	def __init__(self,pos,groups,obj):
		super().__init__(groups)
		self.image = obj
		self.window = pygame.display.get_surface()
		self.window.blit(self.image,pos)
		self.rect = self.image.get_rect(topleft = pos)
		self.rect = self.rect
		Tile.tiles.append([pos[0]//40,pos[1]//40])
		#y_offset = HITBOX_OFFSET[sprite_type]
        
		#self.hitbox = self.rect.inflate(0,y_offset)