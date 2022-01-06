import pygame
import random

class Dusman(pygame.sprite.Sprite):
    def __init__(self,SCREEN_WIDTH,y,hareketli_grafik,scale):
        pygame.sprite.Sprite.__init__(self)
        #değişkenleri tanımlama
        self.animasyon_list=[]
        self.frame_index =0
        self.update_time = pygame.time.get_ticks()
        self.direction=random.choice([-1,1])
        if self.direction==1:
            self.flip=True
        else:
            self.flip=False
        
        #görseli hareketli_görselden yükleme
        animasyon_adimlari=8
        for animasyon in range(animasyon_adimlari):
            image = hareketli_grafik.gorseli_getir(animasyon, 32, 32, scale, (0, 0, 0))
            image= pygame.transform.flip(image, self.flip, False)
            image.set_colorkey((0,0,0))
            self.animasyon_list.append(image)
            
            #başlangıç görselini seçip ardından rectangle oluşturma
            self.image=self.animasyon_list[self.frame_index]
            self.rect = self.image.get_rect()
            
            if self.direction==1:
                self.rect.x=0
            else:
                self.rect.x=SCREEN_WIDTH
            self.rect.y=y
    def update(self,scroll,SCREEN_WIDTH):
        #animasyonları güncelle
        Animasyon_c=50
        #geçerli frame e bağlı olarak görseli güncelleme
        self.image=self.animasyon_list[self.frame_index]
        #son update den bu yana yeterli zaman geçip geçmediğini kontrol ediyorum
        if pygame.time.get_ticks() - self.update_time > Animasyon_c:
            self.update_time=pygame.time.get_ticks()
            self.frame_index += 1
        #animasyon biterse başlangıca geri dön
        if self.frame_index >= len(self.animasyon_list):
            self.frame_index=0
        
        
        #dusmanin hareketi
        self.rect.x += self.direction * 2 
        self.rect.y += scroll
        
        #ekrandan çıkıp çıkmadığını kontrol etme
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()        