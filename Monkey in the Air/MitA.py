import pygame
import random
import os
from pygame import mixer
from hareketli_grafik import Hareketli_Grafik
from dusman import Dusman

mixer.init()
pygame.init()

SCREEN_WIDTH=400
SCREEN_HEIGHT=600

ekran = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Monkey in the Air')

clock = pygame.time.Clock()
FPS = 60

pygame.mixer.music.load('Assets/aol.mp3')
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1, 0.0)
ziplama_fx= pygame.mixer.Sound('Assets/jump.mp3')
ziplama_fx.set_volume(0.5)
olum_fx=pygame.mixer.Sound('Assets/death.mp3')
olum_fx.set_volume(0.5)
muz_fx=pygame.mixer.Sound('Assets/muz.mp3')
muz_fx.set_volume(0.1)

SCROLL_THRESH=200 
GRAVITY=0.8
Maks_dal=10
scroll=0
bg_scroll=0
oyun_bitti=False
skor=0
sayac=0


if os.path.exists('skor.txt'):
    with open('skor.txt','r') as file:
        rekor=int(file.read())
else:
    rekor=0



#rengi tanımlayalım
Beyaz=(255,255,255)
Siyah=(0,0,0)
PANEL = (153, 217, 234)

#fontları tanımlayalım
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)


arkaplan_gorseli=pygame.image.load('Assets/background.jpg').convert_alpha()
monkey_gorseli=pygame.image.load('Assets/monkey.png').convert_alpha()
dal_gorseli=pygame.image.load('Assets/dal.png').convert_alpha()

#kuş hareketli grafikleri
kus_graifigi_gorseli= pygame.image.load('Assets/kus.png').convert_alpha()
kus_grafigi = Hareketli_Grafik(kus_graifigi_gorseli)



#ekrana metin çıktılarımı vermem için gerekli fonksiyon
def draw_text(text,font,text_rengı,x,y):
    img=font.render(text,True,text_rengı)
    ekran.blit(img,(x,y))

#yukarıda skor yazan yerin fonksiyonu
def draw_skor():
    pygame.draw.rect(ekran, PANEL, (0, 0, SCREEN_WIDTH, 30))
    pygame.draw.line(ekran, Beyaz, (0, 30), (SCREEN_WIDTH, 30), 2)
    draw_text('SKOR: ' + str(skor), font_small, Beyaz, 0, 0)

#arka planı çizmemi sağlayan fonksiyon
def draw_bg(bg_scroll):
    ekran.blit(arkaplan_gorseli, (0, 0 + bg_scroll))
    ekran.blit(arkaplan_gorseli, (0, -600 + bg_scroll))



class Oyuncu():
    def __init__(self,x,y):
        self.image=pygame.transform.scale(monkey_gorseli,(45,45))
        self.width=25
        self.height=40
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=(x,y)
        self.vel_y=0
        self.flip=False
    def hareket(self):
        
        scroll=0
        dx=0
        dy=0
        #tuş kombinasyonlarını ayarlıyorum
        key= pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10
            self.flip=True
        if key[pygame.K_d]:
            dx= 10
            self.flip=False
        
        #Yerçekimi
        self.vel_y += GRAVITY
        
        dy += self.vel_y            
        
        #oyuncunun ekran dışına çıkıp çıkmadığını kontrol ediyorum
        if self.rect.left + dx <0:
            dx= -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx= SCREEN_WIDTH - self.rect.right
        #dallarla olan temasını kontrol ediyorum
        for dal in dal_group:
            #y yönündeki temaslar
            if dal.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #platformun üstünde mi değil mi
                if self.rect.bottom < dal.rect.centery:
                    if self.vel_y>0:
                        self.rect.bottom=dal.rect.top
                        dy=0
                        self.vel_y=-20
                        ziplama_fx.play()
                                    
        #oyuncu ekranın üstünü geçiyor mu
        if self.rect.top <= SCROLL_THRESH:
            #eğer oyuncu zıplıyorsa
            if self.vel_y < 0:
                scroll = -dy
                            
        self.rect.x += dx
        self.rect.y += dy + scroll
        
        return scroll
        
    def draw(self):
            ekran.blit(pygame.transform.flip(self.image,self.flip, False),(self.rect.x -12, self.rect.y -5 ))
            #pygame.draw.rect(ekran, Beyaz, self.rect,2)
            

#DAL SINIFI
class Dal(pygame.sprite.Sprite):
    def __init__(self, x, y, width,hareketli):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(dal_gorseli, (width, 10))
        self.hareketli=hareketli
        self.hareket_sayaci=random.randint(0, 50)
        self.direction=random.choice([-1,1])
        self.hiz=random.randint(1, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self,scroll):
         #eğer dal hareketli ise dalı yan yana hareket ettirtiyoruz
         if self.hareketli==True:
             self.hareket_sayaci +=1
             self.rect.x += self.direction * self.hiz
         #tamamen hareket ettiyse veya bir duvara çarptıysa platform yönünü değiştiriyoruz
         if self.hareket_sayaci>=100 or self.rect.left<0 or self.rect.right> SCREEN_WIDTH:
             self.direction *= -1
             self.hareket_sayaci=0
         
             
         #dalların dikeydeki konumunu güncelledim
         self.rect.y += scroll
         #dalların ekrandan çıkıp çıkmadığını kontrol ettim
         if self.rect.top > SCREEN_HEIGHT:
             self.kill()
             
             
class Banana(pygame.sprite.Sprite):
    def __init__(self,x,y,width):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load('Assets/muz.png')
        self.image=pygame.transform.scale(img, (width,30 ))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self,scroll):
        self.rect.y += scroll
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()





monkey= Oyuncu(SCREEN_WIDTH // 2 , SCREEN_HEIGHT -150)

#hareketli dal oluştur
dal_group = pygame.sprite.Group()
dusman_group=pygame.sprite.Group()
muz_group=pygame.sprite.Group()

#başlangıç dalını oluşturdum
dal = Dal(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100,False)
dal_group.add(dal)        


run=True
while run:
    
    clock.tick(FPS)
    if oyun_bitti==False:
        scroll=monkey.hareket()
            
        #arka planı çiz(yukarı ilerlemeden ötürü olan)
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)
        
        #dalları ürettim
        if len(dal_group)< Maks_dal:
           d_w= random.randint(40,60)
           d_x=random.randint(0, SCREEN_WIDTH- d_w)
           d_y=dal.rect.y- random.randint(80, 120)
           d_type=random.randint(1, 2)
           if d_type == 1 and skor>500: #hareketli dalların gelme şartı skorun 500 den fazla olması
               d_hareketli=True
           else:
               d_hareketli=False
           dal = Dal(d_x, d_y, d_w,d_hareketli)
           dal_group.add(dal)       
        

        
        dal_group.update(scroll)
        
        #arkaplanı ekranda gösterme
        ekran.blit(arkaplan_gorseli,(0,0))
        
        #Düsmanı tanımlama
        if len(dusman_group) == 0 and skor > 1000:
            dusman = Dusman(SCREEN_WIDTH, 100, kus_grafigi, 1.5)
            dusman_group.add(dusman)
        #Muzu tanımlama
        if len(muz_group) == 0 and skor > 500:
            muz = Banana(random.randint(40,60),random.randint(80, 120),30)
            muz_group.add(muz)            

        #düsmanlari ve muzu update e sokuyoruz
        dusman_group.update(scroll, SCREEN_WIDTH)        
        muz_group.update(scroll)
        
        #skoru güncelleme
        if scroll>0:
            skor += scroll
        #ekrana önceki rekoru çizgi ile belli ediyorum
        pygame.draw.line(ekran, Beyaz, (0, skor - rekor + SCROLL_THRESH), (SCREEN_WIDTH, skor - rekor + SCROLL_THRESH), 3)
        draw_text('--REKOR--', font_small, Beyaz, SCREEN_WIDTH - 130, skor - rekor + SCROLL_THRESH)
            
        
        dal_group.draw(ekran)
        dusman_group.draw(ekran)
        muz_group.draw(ekran)
        monkey.draw()
        draw_skor()
        
        
        #oyunun bitip bitmediğini kontrol ediyorum
        if monkey.rect.top > SCREEN_HEIGHT:
            oyun_bitti=True
            olum_fx.play()
        
        #düşmanla olan temasını kontrol ediyorum
        if pygame.sprite.spritecollide(monkey,dusman_group,False):
            if pygame.sprite.spritecollide(monkey,dusman_group,False,pygame.sprite.collide_mask):
                oyun_bitti=True
                olum_fx.play()
        #muzla olan temasını kontrol ediyorum
        if pygame.sprite.spritecollide(monkey,muz_group,True):
           skor += 50
           
           muz_fx.play()              
    else:
        if sayac<SCREEN_WIDTH:
            sayac +=5
            for y in range(0,6,2):
                pygame.draw.rect(ekran,Siyah,(0, y * 100,sayac,100))
                pygame.draw.rect(ekran,Siyah,(SCREEN_WIDTH-sayac,(y + 1) * 100,SCREEN_WIDTH,100))
        else:
            draw_text('OYUN BİTTİ!', font_big, Beyaz, 130, 200)
            draw_text('SKOR: '+str(skor), font_big, Beyaz, 130, 250)
            draw_text('OYNAMAK İÇİN SPACE e BAS', font_big, Beyaz, 40, 300)
            
            #rekoru güncelleme
            if skor>rekor:
                rekor=skor
                with open('skor.txt','w') as file:
                    file.write(str(rekor))
            key=pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                #değerleri sıfırlayalım
                oyun_bitti=False
                skor=0
                scroll=0
                sayac=0
                #monkeyi yeniden pozisyon aldırtıyorum
                monkey.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
                #dalları sıfırlıyorum
                dal_group.empty()
                #düsmanlari sifirliyorum
                dusman_group.empty()
                #başlangıç dalını oluşturuyorum
                dal=Dal(SCREEN_WIDTH//2 -50,SCREEN_HEIGHT-50,100,False)
                dal_group.add(dal)
        
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            #rekoru güncelleme
            if skor>rekor:
                rekor=skor
                with open('skor.txt','w') as file:
                    file.write(str(rekor))
            run=False
    
    
    pygame.display.update()

pygame.quit()        
    