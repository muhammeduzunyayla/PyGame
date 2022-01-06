import pygame

class Hareketli_Grafik():
    def __init__(self,image):
        self.sheet=image
    def gorseli_getir(self,frame,width,height,scale,renk):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        image.set_colorkey(renk)

        return image

