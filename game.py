import pygame, time, sys, random
from pygame import QUIT
from pygame.mixer import pre_init
pygame.init()
pygame.mixer.init()
width = 1000
height = 700
white = (255,255,255)
black = (0,0,0)
sand_color = (195,169,139)
background = pygame.image.load("assets/background_2.png")
#Crea la ventana/fps!!!
screen = pygame.display.set_mode((width,height))
fps = pygame.time.Clock()
#creación de canales de música
game_channel = pygame.mixer.Channel(0)
options_channel = pygame.mixer.Channel(1)
main_channel = pygame.mixer.Channel(2)
gameover_channel = pygame.mixer.Channel(3)
#carga de efectos de sonido y música
game_channel_sound = pygame.mixer.Sound("sound/song.ogg")
options_channel_sound = pygame.mixer.Sound("sound/options.ogg")
main_channel_sound = pygame.mixer.Sound("sound/main.ogg")
gameover_channel_sound = pygame.mixer.Sound("sound/gameover.ogg")
engine = pygame.mixer.Sound("sound/engine.ogg")
explosion = pygame.mixer.Sound("sound/explosion.ogg")
shoot_sound = pygame.mixer.Sound("sound/shoot.ogg")
iron_sound = pygame.mixer.Sound("sound/iron_sound.ogg")
sonidoMenu = pygame.mixer.Sound('sound/selection.ogg')

#Fuente y tamaño de las letras
font = pygame.font.SysFont(None, 40)
font2 = pygame.font.SysFont(None, 100)

#clases......................................................................../
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  
        self.image = pygame.image.load("assets/player.png").convert()     
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height -10
        self.speed_x = 0
        self.speed_y = 0  
        self.hp=200
        self.nivel=1
        self.misiles=0
        self.puntaje=0  
        self.apoyo=3

class Death(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()             
        self.sprites = []
        self.is_animating = False
        self.sprites.append(pygame.image.load("assets/TankExplosion/0001.png"))
        self.sprites.append(pygame.image.load("assets/TankExplosion/0002.png"))
        self.sprites.append(pygame.image.load("assets/TankExplosion/0003.png"))
        self.sprites.append(pygame.image.load("assets/TankExplosion/0004.png"))
        self.sprites.append(pygame.image.load("assets/TankExplosion/0005.png"))
        self.sprites.append(pygame.image.load("assets/TankExplosion/0006.png"))
        self.sprites.append(pygame.image.load("assets/TankExplosion/0007.png"))
        self.sprites.append(pygame.image.load("assets/TankExplosion/0008.png"))
        self.sprites.append(pygame.image.load("assets/TankExplosion/0009.png"))
        self.sprites.append(pygame.image.load("assets/TankExplosion/0010.png"))
        self.sprites.append(pygame.image.load("assets/TankExplosion/0011.png"))
        self.sprites.append(pygame.image.load("assets/TankExplosion/0012.png"))
        self.sprites.append(pygame.image.load("assets/TankExplosion/0013.png"))
        self.sprites.append(pygame.image.load("assets/TankExplosion/0014.png"))
        self.sprites.append(pygame.image.load("assets/TankExplosion/0015.png"))
        self.current_sprite=0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = x-30
        self.rect.y = y-30
    def animate(self):
        self.is_animating = True
    
    def update(self):
        if self.is_animating == True:
            self.current_sprite+=1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite=-1
                self.is_animating = False
            self.image = self.sprites[self.current_sprite]

class Shooting(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("assets/bullet.png").convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
  
    def update(self):
        self.rect.y -= 3    

#Avion que surge de la parte inferior de la pantalla y destrulle a los tanques por debajo
class ApoyoAereo(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("assets/avion.png").convert_alpha()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
  
    def update(self):
        self.rect.y -= 9    

class Tank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/tank_red.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(200 , 700)
        self.rect.y = random.randrange(height - 350)
        self.speed_y = 1

   #funcionalidad para que se vuelva a generar un tanque al salir del mapa
    def update (self):
        if self.rect.y > height:
            self.rect.y = -10
            self.rect.x = random.randrange(150,750) 
#clase hija
class Tank_green(Tank):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/tank_green.png").convert_alpha()

def simple_show_text(string,position1, position2):
    text1 = font.render(string, True, (173,255,47))
    screen.blit(text1, (position1,position2))

def show_text(string, int, position1, position2, position3, position4):
    text1 = font.render(string, True, (173,255,47))
    screen.blit(text1, (position1,position2))
    text2 = font.render(str(int), True, (173,255,47))
    screen.blit(text2, (position3,position4))

def gameOver():
    gameover_channel.play(gameover_channel_sound, loops=0, fade_ms=0)
    text1 = font2.render("GAME OVER", True, (255,0,0))
    text_rect = text1.get_rect(center=(width/2, height/2))
    screen.blit(text1, text_rect)
    game_channel.stop()

def Pause(surface): #Pausa dibuja un rectangulo negro con baja opacidad en la pantalla
    shape_surf = pygame.Surface(pygame.Rect((0, 0, width, height)).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, (0,0,0, 127), shape_surf.get_rect())
    shape_surf.set_alpha(128)
    surface.blit(shape_surf, (0, 0, width, height))
    text1 = font2.render("PAUSA", True, (0,143,57))
    text2 = font.render("Pulse p para continuar", True, (0,143,57))
    text_rect = text1.get_rect(center=(width/2, height/2))
    text_rect2 = text2.get_rect(center=(width/2, height/2+50))
    screen.blit(text1, text_rect)
    screen.blit(text2, text_rect2)



#Menu del juego....................................................................../
"""Texto en la mitad mas 50 para arriba y 50 para abajo.Posicion de los cuadrados que marcan que
opcion estas eligiendo va a ser lo mismo, para tener una referencia y despues un event
que vaya manejando la variable
width = 1000
height = 700"""
def menu():
    main_channel.play(main_channel_sound, loops=-1, fade_ms=100)
    sigueEnMenu= True
    cuadradoEnX = int(width/2)
    cuadradoEnY = int((height/2)-50)
    jugar=int((height/2)-50)
    salir= int((height/2)+50)
    negro= pygame.image.load("assets/main.png")
    #cuadrado = pygame.Rect(cuadradoEnX, cuadradoEnY, 150, 30)
    while(sigueEnMenu):
        pygame.draw.rect(screen, (255, 0, 0), (cuadradoEnX, cuadradoEnY, 150, 30), 1)
        # Texto
        simple_show_text("Jugar", width/2, (height/2)-50)
        simple_show_text("Opciones", width/2, (height/2))
        simple_show_text("Salir", width/2, (height/2)+50)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sonidoMenu.play()
                    pygame.quit()
                if event.key == pygame.K_UP:
                    sonidoMenu.play()
                    cuadradoEnY -= 50
                    if cuadradoEnY < jugar:
                        cuadradoEnY=((height/2)+50)
                if event.key == pygame.K_DOWN:
                    sonidoMenu.play()
                    cuadradoEnY = cuadradoEnY + 50
                    if cuadradoEnY > salir:
                        cuadradoEnY = ((height/2)-50)
                if event.key == pygame.K_RETURN:
                    sonidoMenu.play()
                    if cuadradoEnY == ((height/2)-50) :
                        main_channel.stop()
                        game_channel.play(game_channel_sound, loops=-1, fade_ms=100)
                        sigueEnMenu = False
                    elif cuadradoEnY == ((height / 2)):
                        opciones(cuadradoEnX,cuadradoEnY)
                    elif cuadradoEnY == ((height / 2)+50):
                        pygame.quit()
        # actualiza la pantalla
        pygame.display.update()
        screen.blit(negro, (0,0))
def opciones(cuadradoEnX,cuadradoEnY):
    sigueEnOpciones=True
    opcionesFondo = pygame.image.load("assets/options.png")
    main_channel.stop()
    options_channel.play(options_channel_sound, loops=-1, fade_ms=100)
    Video = int((height / 2) - 50)
    Atras = int((height / 2) + 50)
    while (sigueEnOpciones):
        pygame.draw.rect(screen, (255, 0, 0), (cuadradoEnX, cuadradoEnY, 150, 30), 1)
        # Texto
        simple_show_text("Video", width / 2, (height / 2) - 50)
        simple_show_text("Sonido", width / 2, (height / 2))
        simple_show_text("Atrás", width / 2, (height / 2) + 50)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sonidoMenu.play()
                    pygame.quit()
                if event.key == pygame.K_UP:
                    sonidoMenu.play()
                    cuadradoEnY -= 50
                    if cuadradoEnY < Video:
                        cuadradoEnY = ((height / 2) + 50)
                if event.key == pygame.K_DOWN:
                    sonidoMenu.play()
                    cuadradoEnY = cuadradoEnY + 50
                    if cuadradoEnY > Atras:
                        cuadradoEnY = ((height / 2) - 50)
                if event.key == pygame.K_RETURN:
                    sonidoMenu.play()
                    if cuadradoEnY == ((height / 2) - 50):
                        sigueEnOpciones = True
                    elif cuadradoEnY == ((height / 2)):
                        sigueEnOpciones = True
                    elif cuadradoEnY == ((height / 2) + 50):
                        options_channel.stop()
                        main_channel.play(main_channel_sound, loops=-1, fade_ms=100)
                        sigueEnOpciones = False
        # actualiza la pantalla
        pygame.display.update()
        screen.blit(opcionesFondo, (0,0))

def init():
    global tank_red_list
    global tank_green_list
    global shoot_list
    global crash_list
    global apoyo_list
    global all_sprites
    global player
    global game_over
    global pause
    #creación de listas
    tank_red_list = pygame.sprite.Group()
    tank_green_list = pygame.sprite.Group()
    shoot_list = pygame.sprite.Group()
    crash_list = pygame.sprite.Group()
    apoyo_list=pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    #instanciación del jugador con clase player
    player = Player()

    #instanciación y guardado de tanques verdes
    for i in range(3):
        tank_green = Tank_green()
        tank_green_list.add(tank_green)
        all_sprites.add(tank_green)

    #instanciación y guardado de tanques rojos
    for i in range(5):
        tank_red = Tank()    
        tank_red_list.add(tank_red)
        all_sprites.add(tank_red)

    #guardo el sprite del tanque una lista
    all_sprites.add(player)

    #Condición para que corra el juego!!!
    game_over = False

#Bucle principal...................................................................../
enProceso = True
def game():
    player.hp=200
    player.nivel=1
    player.misiles=3
    player.apoyo=3
    misilNuevo=0
    player.puntaje=0
    ultimoMisil=0   
    y=700
    all_sprites.add(player)
    game_over=False
    completado=False
    tiempoFinal=int(pygame.time.get_ticks())/500
    pause=False
  
    while not game_over :
        if not pause:
            tiempoTranscurrido=int(pygame.time.get_ticks())/500-tiempoFinal
        for event in pygame.event.get():
            #Eventos teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_p:
                    pause=not pause
                    Pause(screen)
                # tanque rojo!!!
                if event.key == pygame.K_LEFT:
                    player.speed_x = -3
                    player.image = pygame.image.load("assets/player_left.png").convert()
                    player.image.set_colorkey(black)
                if event.key == pygame.K_RIGHT: 
                    player.speed_x = 3
                    player.image = pygame.image.load("assets/player_right.png").convert()
                    player.image.set_colorkey(black)
                if event.key == pygame.K_UP:
                    player.speed_y = -3
                    player.image = pygame.image.load("assets/player.png").convert()     
                    player.image.set_colorkey(black)
                if event.key == pygame.K_DOWN: 
                    player.speed_y = 3   
                    player.image = pygame.image.load("assets/player_down.png").convert()     
                    player.image.set_colorkey(black)
                if event.key == pygame.K_q: 
                    if(player.apoyo>0):
                            apoyo = ApoyoAereo()   
                            apoyo.rect.x = player.rect.x +10
                            apoyo.rect.y = height
                            all_sprites.add(apoyo)
                            apoyo_list.add(apoyo)
                            player.apoyo=player.apoyo-1

                if event.key == pygame.K_SPACE:
                        #creación del disparo
                        if(player.misiles>0):
                            if(int(tiempoTranscurrido)-int(ultimoMisil)>15):
                                player.puntaje=player.puntaje-((int(tiempoTranscurrido)-int(ultimoMisil))*300)
                            shoot = Shooting()   
                            shoot.rect.x = player.rect.x +10
                            shoot.rect.y = player.rect.y -20
                            all_sprites.add(shoot)
                            shoot_list.add(shoot)
                            shoot_sound.play() 
                            player.misiles=player.misiles-1
                            misilNuevo=tiempoTranscurrido
                            ultimoMisil=tiempoTranscurrido
                            
            if event.type == pygame.KEYUP:
                # tanque rojo!!!
                if event.key == pygame.K_LEFT:
                    player.speed_x = 0
                if event.key == pygame.K_RIGHT:
                    player.speed_x = 0
                if event.key == pygame.K_UP:
                    player.speed_y = 0
                if event.key == pygame.K_DOWN:
                    player.speed_y = 0    
                
    #control del jugador dentro del escenario
        if player.rect.right > 800:
            player.rect.right = 800
        if player.rect.left < 200:
            player.rect.left = 200  
        if player.rect.top < 0:
            player.rect.top = 0
        if player.rect.bottom > height:
            player.rect.bottom = height    

        #fondo y movimiento de la imagen de fondo
        #se encapsula todas las actualizaciones de sprites condicionados por el estado de "pause"
        if not pause:
            y_relativa = y % background.get_rect().height
            screen.blit(background,(0,y_relativa-background.get_rect().height))
            if y_relativa < height: 
                screen.blit(background,(0,y_relativa))
            y += 1*2

            #actualización del movimiento del tanque rojo
            player.rect.x += player.speed_x
            player.rect.y += player.speed_y
        
            #actualización del movimiento vertical de todos los tanques
            for i in tank_red_list:
                i.rect.y += i.speed_y*2
        
            for i in tank_green_list:
                i.rect.y += i.speed_y*2

            #colisiones del disparo con los tanques rojos
            for i in shoot_list:
                shoot_hits_list = pygame.sprite.spritecollide(shoot,tank_red_list,True)
                for i in shoot_hits_list:
                    all_sprites.remove(shoot)
                    shoot_list.remove(shoot)
                    explosion.play() 
                    death = Death(i.rect.x,i.rect.y)
                    death.animate()
                    all_sprites.add(death)
                    player.puntaje=player.puntaje+200
                if shoot.rect.y < -10:
                    all_sprites.remove(shoot)
                    shoot_list.remove(shoot)
            #Colisiones del apoyo con tanques
            for i in apoyo_list: 
                apoyo_hits_list = pygame.sprite.spritecollide(apoyo,tank_red_list,True)
                apoyo_hits_list2 = pygame.sprite.spritecollide(apoyo,tank_green_list,True)
                for i in apoyo_hits_list:
                    explosion.play() 
                    death = Death(i.rect.x,i.rect.y)
                    death.animate()
                    all_sprites.add(death)
                    player.puntaje=player.puntaje+200
                for i in apoyo_hits_list2:
                    explosion.play() 
                    death = Death(i.rect.x,i.rect.y)
                    death.animate()
                    all_sprites.add(death)
                    player.puntaje=player.puntaje+300
                if apoyo.rect.y < -10:
                    all_sprites.remove(apoyo)
                    apoyo_list.remove(apoyo)

            #colisiones del disparo con las tanques verdes
            for i in shoot_list:
                shoot_hits_list = pygame.sprite.spritecollide(shoot,tank_green_list,len(tank_red_list)==0)
                for i in shoot_hits_list:
                    all_sprites.remove(shoot)
                    shoot_list.remove(shoot)
                    if(len(tank_red_list)>0):
                        iron_sound.play()
                    if(len(tank_red_list)==0):
                        player.puntaje=player.puntaje+500
                        death = Death(i.rect.x,i.rect.y)
                        death.animate()
                        all_sprites.add(death)
                        explosion.play() 
            

            #colisión del player con los tanques
            for i in tank_red_list:
                crash_list = pygame.sprite.spritecollide(player,tank_red_list,True)  
                if len(crash_list) == 1:
                    explosion.play()     
                for i in crash_list:   
                    player.hp=player.hp-20         
                    death = Death(player.rect.x,player.rect.y)
                    death.animate()
                    all_sprites.add(death)
                    if(player.hp<=0): 
                        all_sprites.remove(player)
                        game_over=True
                        if(game_over):
                            gameOver()
                
            for i in tank_green_list:   #revisar como optimizar las dos listas!!!
                crash_list = pygame.sprite.spritecollide(player,tank_green_list,True)  
                if len(crash_list) == 1:
                    explosion.play()     
                for i in crash_list: 
                    player.hp=player.hp-40 
                    death = Death(player.rect.x,player.rect.y)
                    death.animate()
                    all_sprites.add(death)
                    if(player.hp<=0):   
                        all_sprites.remove(player)
                        game_over=True
                        if(game_over):
                            gameOver()

            #todos los metodos update de los objetos de esta lista funcionando
            if(not game_over):
                all_sprites.update()
                #dibujo en la pantalla
                all_sprites.draw(screen)
            #Texto
            show_text("Energía: ", player.hp,0,60,140,60)
            show_text("Misiles: ", player.misiles, 0,120,140,120)
            show_text("Nivel: ", player.nivel,0,180,140,180)
            show_text("Puntaje: ", player.puntaje,0,240,140,240)
            show_text("Apoyos: ", player.apoyo,0,300,140,300)
            pygame.display.flip()
        
            

    #Bucle principal.....................................................................................\

    #Los misiles se incrementan cada 3 segundos
        if(tiempoTranscurrido-misilNuevo>3):
            player.misiles=player.misiles+1
            misilNuevo=tiempoTranscurrido
    #Cuando se eliminen todos los tanques se incrementa el nivel 
    #se hace un bonus de misiles,energia y apoyos.
        if(len(tank_green_list)==0 and len(tank_red_list)==0):
            player.nivel=player.nivel+1
            completado=True
            player.hp=player.hp+100
            player.misiles=player.misiles+3
            player.apoyo=player.apoyo+3
    #Cada vez que se incrementa el nivel se crean más tanques
        if(player.nivel>1 and completado):
            completado=False
            for i in range(player.nivel+2):
                tank_green = Tank_green()
                tank_green_list.add(tank_green)
                all_sprites.add(tank_green)
            for i in range(player.nivel+4):
                tank_red = Tank()    
                tank_red_list.add(tank_red)
                all_sprites.add(tank_red)
        #actualiza la pantalla
        pygame.display.flip()
        fps.tick(40) 
        
while(enProceso):
    pygame.time.wait(3200)
    init()
    menu()
    game()