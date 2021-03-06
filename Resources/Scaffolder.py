import pygame
import random
pygame.init()
pygame.mixer.init()


visinaProzora=600;
sirinaProzora=500;
prozor= pygame.display.set_mode((sirinaProzora,visinaProzora))
pygame.display.set_caption("Scaffolder")

#-------------------ZVUUUK-----------------------
skok_zvuk = pygame.mixer.Sound('Jump4.wav')




#animacija, treba popraviti, ovo je samo trenutno
hodajDesno1=[pygame.image.load('w1.png'),pygame.image.load('w2.png'),pygame.image.load('w3.png'),pygame.image.load('w4.png'),pygame.image.load('w5.png'),pygame.image.load('w6.png'),pygame.image.load('w7.png'),pygame.image.load('w8.png'),pygame.image.load('w9.png'),pygame.image.load('w10.png')]
hodajDesno = []
for img in hodajDesno1:
    hodajDesno.append(pygame.transform.scale(img , (68,80)))
hodajLevo1=[pygame.transform.flip(pygame.image.load('w1.png'),True,False),pygame.transform.flip(pygame.image.load('w2.png'),True,False),pygame.transform.flip(pygame.image.load('w3.png'),True,False),pygame.transform.flip(pygame.image.load('w4.png'),True,False),pygame.transform.flip(pygame.image.load('w5.png'),True,False),pygame.transform.flip(pygame.image.load('w6.png'),True,False),pygame.transform.flip(pygame.image.load('w7.png'),True,False),pygame.transform.flip(pygame.image.load('w8.png'),True,False),pygame.transform.flip(pygame.image.load('w9.png'),True,False),pygame.transform.flip(pygame.image.load('w10.png'),True,False)]
hodajLevo = []
for img in hodajLevo1:
    hodajLevo.append(pygame.transform.scale(img , (68,80)))
slikaIgracaD=pygame.transform.scale(pygame.image.load('igrac.png') , (64,78))
slikaIgracaL=pygame.transform.flip(slikaIgracaD,True,False)
skokD=pygame.transform.scale(pygame.image.load('j1.png') , (64,76))
skokL=pygame.transform.flip(skokD,True,False)
pozadina=pygame.image.load('pozadina.jpg')
clock=pygame.time.Clock()
platformaSlika1=[pygame.image.load('platformaSlika.png'),pygame.image.load('platformaSlika1.png'),pygame.image.load('platformaSlika2.png'),pygame.image.load('platformaSlika3.png'),pygame.image.load('platformaSlika4.png'),pygame.image.load('platformaSlika5.png'),pygame.image.load('platformaSlika6.png')]
platformaSlika=platformaSlika1[0]

#SCORE-------------

def score(skor):
    font = pygame.font.Font('AGENCYB.ttf', 18)
    text = font.render("SCORE: "+str(skor),True , (255,255,255))
    prozor.blit(text , (5,5))

############## START EKRAN ##################
    
def text_objects(poruka, boja,vel_font=25):
    font = pygame.font.Font('AGENCYB.ttf', vel_font)
    textSurface = font.render(poruka, True, boja)
    return textSurface, textSurface.get_rect()

def ispisi_poruku(poruka , boja , y_pomeraj = 0, vel_font=25):
    font = pygame.font.Font('AGENCYB.ttf', vel_font)
    TextSurf, TextRect = text_objects(poruka, boja,vel_font)
    TextRect.center = (255,500/2 + y_pomeraj) 
    prozor.blit(TextSurf, TextRect)

###########Pauza---------------------------------
def pauza():
    pauza_promenljiva = True
    pygame.mixer.music.pause()
    while pauza_promenljiva:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pauza_promenljiva = False
                    pygame.mixer.music.unpause()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        ispisi_poruku("PAUSED", (255,255,255) , -120, 75)
        ispisi_poruku("\"P\" - CONTINUE  \"Q\" - QUIT" ,(255,255,255) , 0)
        pygame.display.update()
        clock.tick(3)

def start_igre():    
    intro = True
    pygame.mixer.music.load('pocetna.wav')
    pygame.mixer.music.play(loops=-1)
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    intro = False
                    pygame.mixer.music.load('pesma.ogg')
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        #prozor.fill((255,255,255))
        pozadina=pygame.image.load('start.jpg')
        prozor.blit(pozadina,(0,0))
        pygame.display.update()
        #pygame.time.Clock().tick(15)

################# KLASA IGRACA ##################
class player(object):
    def __init__(self,x,y,sirObjekta,visObjekta,platformaa):
        self.x=x
        self.y=y
        self.sirObjekta=sirObjekta
        self.visObjekta=visObjekta
        self.brzina=5
        self.isSkok=False  #KORISTI SE KOD PADANJA
        self.intenzitetSkoka=9
        self.skokBrojac= self.intenzitetSkoka
        self.levoOkrenut=False
        self.desnoOkrenut=True
        self.isKrece=False
        self.hodanjeBrojac=0 #sluzi ako nasa animacija hodanja ima vise slika-faza hodanja
        self.isStoji = True
        self.platformaa=platformaa
    def draw(self,prozor):
############# OVDE JE ANIMACIJA ##################
#(3*3)zelimo da nasa slika traje 3 frejma i imamo 3 razlicite slike hodanja
        if self.hodanjeBrojac + 1 >=30:
            self.hodanjeBrojac=0
        if self.isStoji and not(self.isSkok):  
            if self.levoOkrenut:
                if self.isKrece:
                    prozor.blit(hodajLevo[self.hodanjeBrojac//10],(self.x-10,self.y))
                    self.hodanjeBrojac+=1
                else:
                    prozor.blit(slikaIgracaL,(self.x-10,self.y))
            elif self.desnoOkrenut:
                if self.isKrece:
                    prozor.blit(hodajDesno[self.hodanjeBrojac//10],(self.x-10,self.y))
                    self.hodanjeBrojac+=1
                else:
                    prozor.blit(slikaIgracaD,(self.x-10,self.y))
        else:
            if self.levoOkrenut:
                prozor.blit(skokL , (self.x-10, self.y))
            else:
                prozor.blit(skokD , (self.x-10, self.y))
            
        
        

###################### KLASA PLATFORME ##################
class platforma(object):
    def __init__(self,x ,y , sirObjekta, skorPlatforme):
        self.x=x
        self.y=y
        self.sirObjekta=sirObjekta
        self.visObjekta=20
        self.skorPlatforme=skorPlatforme
    def draw(self, prozor):
        prozor.blit(pygame.transform.scale(platformaSlika,(self.sirObjekta,50)),(self.x,self.y))
        self.hitbox=(self.x+10,self.y+6,self.sirObjekta-20,30)
        #pygame.draw.rect(prozor,(255,0,0),self.hitbox,2)
    #Neki tuzan pokusaj kolajdera, trenutna verzija mozda mnogo bolja
    #def collide(self,rect):
    #    if rect[0]+rect[2]>self.hitbox and rect[0]<self.hitbox[0]+self.hitbox[2]:
    #        if rect[1]+rect[3]> self.hitbox[1]:
    #            return True
    #        return False


############## OSVEZAVANJE EKRANA ##############
def osveziSliku():
    # kad stavimo global to znaci da koristimo
    #vec postojecu promenljivu sa ovim imenom, deklarisanu van funkcije
    prozor.blit(pozadina,(0,0))
    zemlja.draw(prozor)
    for x in platforme:
        x.draw(prozor)
    igrac.draw(prozor)
    score(skor)
    pygame.display.update()


skor = 0
with open("rekordi.txt") as file:  
    rekord = file.read()
pomocna_promenljiva_za_rekord=False
munja = 5
ubrzanje=0
skokUbrzanje=0.5
brojPlatformi=0
indikator = False
start_igre()
zemlja = platforma(0,visinaProzora-37,sirinaProzora,0)
igrac  = player(150,visinaProzora-105,42,78,zemlja)
brojacZaPadanje=0
platforme = []
platforme.append(zemlja)
run=True
GameOver = False
#GLAVNA UPDATE FUNKCIJA
pygame.mixer.music.play(loops=-1)
while run:    

    #milisekunde, FPS, koliko cesto se slika apdejta
    #for plat in platforme:
    #    if plat.collide(igrac.hitbox):
    #        igrac.y=plat.y+igrac.visObjekta
    clock.tick(30)
    if igrac.y <= visinaProzora/5:
        igrac.y += abs(igrac.intenzitetSkoka)
        for plat in platforme:
            plat.y += abs (igrac.intenzitetSkoka)

############ GameOver ekran--------------------------------------   
    while GameOver == True:
        pomocna_pozadina=pygame.image.load('gameover.jpg')
        prozor.blit(pomocna_pozadina,(0,0))
        if skor>int(rekord):
            pomocna_promenljiva_za_rekord=True


        if pomocna_promenljiva_za_rekord:
            ispisi_poruku("YOU SET NEW RECORD!!!",(81,81,81),10,50)
            rekord = skor
            with open("rekordi.txt","w") as f:
                f.write(str(rekord))
        else:
            ispisi_poruku("MAXIMUM SCORE: " +str(rekord),(81,81,81),10,40)
        ispisi_poruku("GAMEOVER" , (81,81,81),90,40)
        ispisi_poruku("SCORE: " + str(skor) , (81,81,81),50, 25)
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    pygame.mixer.music.load('pesma.ogg')
                    pygame.mixer.music.play(loops=-1)
                    skor = 0
                    MOJE_novcici = 0
                    brojPlatformi=0
                    ubrzanje=0
                    skokUbrzanje=0.5
                    GameOver = False
                    run = True
                    zemlja = platforma(0,visinaProzora-37,sirinaProzora,0)
                    igrac  = player(150,visinaProzora-105,42,78,zemlja)
                    brojacZaPadanje=0
                    platforme = []
                    platforme.append(zemlja)
                    pomocna_promenljiva_za_rekord=False

                if event.key == pygame.K_q:
                    GameOver = False
                    run = False

    if igrac.y >530:
        GameOver = True
        indikator = False
        pygame.mixer.music.load('pocetna.wav')
        pygame.mixer.music.play(loops=-1)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pauza()

############# GENERACIJA PLATFORMI ###########
    if len(platforme) < 20:
        if len(platforme) == 1:
            brojPlatformi+=1                   
            platformaA = platforma(random.randint(20,sirinaProzora-170),zemlja.y-100, 150,brojPlatformi)
            platforme.append(platformaA)
        else:
            brojPlatformi+=1
            platformaB = platforme.pop()
            pomocnaProm=random.random()
            pomocnaProm1=random.randint(platformaB.x,platformaB.x+190)
            pomocnaProm2=random.randint(platformaB.x-125,platformaB.x)
            if pomocnaProm <0.5:
                if pomocnaProm1<sirinaProzora-100:
                    platformaA = platforma(pomocnaProm1,platformaB.y-100, 150-random.randint(1,50),brojPlatformi)
                else:
                    platformaA = platforma(pomocnaProm2,platformaB.y-100, 150-random.randint(1,50),brojPlatformi)
            else:
                if pomocnaProm2<0:
                    platformaA = platforma(pomocnaProm1,platformaB.y-100, 150-random.randint(1,50),brojPlatformi)
                else:
                    platformaA = platforma(pomocnaProm2,platformaB.y-100, 150-random.randint(1,50),brojPlatformi)                           
            platforme.append(platformaB)
            platforme.append(platformaA) 
    elif platforme[1].skorPlatforme + 4<skor:
        platforme.pop(1)

    keys=pygame.key.get_pressed()
####### KRETNJA I GRANICA KRETNJE #######
    if keys[pygame.K_LEFT] and igrac.x>0:
        igrac.x-=igrac.brzina
        igrac.levoOkrenut=True
        igrac.desnoOkrenut=False
        igrac.isKrece=True

    elif keys[pygame.K_RIGHT] and igrac.x<(sirinaProzora-igrac.sirObjekta):
        igrac.x+=igrac.brzina
        igrac.levoOkrenut=False
        igrac.desnoOkrenut=True
        igrac.isKrece=True

    else:
        igrac.isKrece=False
        igrac.hodanjeBrojac=0

####### SKAKANJE I PADANJE ##########

    if not(igrac.isStoji): ####    KAD NE STOJI
        for plat in platforme:
            if igrac.y+72+7+munja>plat.y and igrac.y+72<= plat.y and igrac.x-10 + igrac.sirObjekta-10>=plat.x+2 and igrac.x+5<= plat.x+plat.sirObjekta:#igrac.x-10 + igrac.sirObjekta-5>=plat.x+2 and igrac.x-10<= plat.x+plat.sirObjekta:
                igrac.y=plat.y-igrac.visObjekta+11
                igrac.isStoji=True
                igrac.platformaa=plat
                brojacZaPadanje=0
                if skor < plat.skorPlatforme:
                    skor=plat.skorPlatforme
                    if skor % 5 == 0:
                        platformaSlika = platformaSlika1[(skor//5)%7]
                    if skor % 16 == 15 and ubrzanje <1.5:
                        ubrzanje+=0.5
                        
                        
                break
    else: #########___KAD STOJI___#########
        if igrac.x-10 + igrac.sirObjekta-10<igrac.platformaa.x+2 or igrac.x+5> igrac.platformaa.x+igrac.platformaa.sirObjekta:
            igrac.isStoji=False
    if not(igrac.isSkok): 
        if not(igrac.isStoji): ####   KAD PADA
            igrac.y+=7
        if keys[pygame.K_SPACE] and igrac.isStoji:
            skok_zvuk.play()
            igrac.isSkok = True
            igrac.hodanjeBrojac=0
            brojacZaPadanje=0
    else:
        if igrac.skokBrojac >= 0: 
            igrac.y-=(igrac.skokBrojac ** 2)*skokUbrzanje
            igrac.skokBrojac -= 1
        else:
            igrac.isSkok=False
            igrac.isStoji=False
            igrac.skokBrojac=igrac.intenzitetSkoka
    
########### POCINJU PLATFORME DA SE POMERAJU ############
    if igrac.y <=256:
        indikator = True
    if indikator == True:
        for p in platforme:
            p.y += munja + ubrzanje
        igrac.y += munja + ubrzanje
    osveziSliku()
pygame.quit()
