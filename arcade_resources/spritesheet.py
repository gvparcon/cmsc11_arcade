import pygame

#object sprite sheet
class SpriteSheet():
	#takes an image file or a spritesheet image
	def __init__(self, image):
		self.sheet = image

	#def get image is for extracting each individual frame for a spritesheet
	def get_image(self, frame, width, height, scale, colour):
		image = pygame.Surface((width, height)).convert_alpha()						#create a surface
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))			#blit the a specific part of the spritesheet (the frames) to the surface
		image = pygame.transform.scale(image, (width * scale, height * scale))		#scales the spritesheet depeding on user scale
		image.set_colorkey(colour)													#creates a colorkey for extracting the images
		return image