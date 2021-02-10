import pygame as pg
from Space_ship import GAME_DIMENSIONS, FPS

import random
import sys

pg.init()

# fuente
pg.font.init()

def create_font(t, s=72, c=(255,255,0), b=False, i=False):
    font = pg.font.SysFont("Arial", s, bold=b, italic=i)
    text = font.render(t, True, c)
    return text

GAME_OVER_FONT = create_font("GAME OVER")
SURF = pg.display.set_mode(GAME_DIMENSIONS)


class Nivel:
    def __init__(self, n, m):
        self.nivel = n
        self.puntos = 0
        self.update_nivel()
        self.meta_nivel = m
    
    def update_nivel(self):
        self.asteroide = asteroide( 928, 236, 5, 0)
        self.aster = []
        for i in range(random.randint(2, 7)):
            ax3 = Asteroidex3()
            ax3.vx = random.randint(2, 15)
            self.aster.append(ax3)
        


class Explote(pg.sprite.Sprite): 
    imagenes_files = ['explote100x100_01.png', 'explote100x100_02.png', 'explote100x100_03.png', 'explote100x100_04.png',  'explote100x100_05.png',
                        'explote100x100_06.png',  'explote100x100_07.png', 'explote100x100_08.png', 'explote100x100_09.png', 'explote100x100_10.png',
                        'explote100x100_11.png',  'explote100x100_12.png', 'explote100x100_13.png', 'explote100x100_14.png', 'explote100x100_15.png',
                        'explote100x100_16.png',  'explote100x100_18.png', 'explote100x100_19.png', 'explote100x100_20.png']

    def __init__(self):
        super(Explote, self).__init__()
        self.image_act = 0
        self.imagenes = self.cargaImagenes()
        self.image = self.imagenes[self.image_act]
        self.rect = pg.Rect(5, 5, 150, 198)
        self.ciclos_tras_refresco = 0
        self.retardo_anim = 10
        

    def update(self):
        self.ciclos_tras_refresco += 1
        if self.ciclos_tras_refresco % self.retardo_anim == 0:
            self.image_act += 1
            if self.image_act >= len(self.imagenes):
                self.image_act = 0       
        self.image = self.imagenes[self.image_act]


    def cargaImagenes(self):
        lista_imagenes = []
        for img in self.imagenes_files:
            lista_imagenes.append(pg.image.load(f"recursos/imagenes/{img}"))
        return lista_imagenes

    def setPosition(self, x, y):
        self.rect.top = y
        self.rect.left = x

    def explote_sound(self):
        pg.mixer.init()
        pg.mixer.music.load("recursos/audio/sonido-1.mp3")
        pg.mixer.music.play()


class nave:

    def __init__(self, x, y, vy):
        self.x = x
        self.y = y
        self.vy = vy
        self.image = pg.image.load("recursos/imagenes/nave-75x50.png")
        self.rect = pg.Surface.get_rect(self.image)
        self.rect.top = y
        self.rect.left = x
        self.setDimension()

    def getRect(self):
        return self.rect

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height


    def setDimension(self):
        self.height = pg.Surface.get_height(self.image)
        self.width = pg.Surface.get_width(self.image)


    def actualizar(self):
        self.y += self.vy
        self.rect.top += self.vy 
        if self.y + 50 >= GAME_DIMENSIONS[1]:
            self.y = GAME_DIMENSIONS[1] - 50
            self.rect.top = GAME_DIMENSIONS[1] - 50
        if self.y <= 0:
            self.y = 0
            self.rect.top = 0

    def manejar_eventos(self):
        # metodo movimiento de nave con get pressed
        teclas_pulsadas = pg.key.get_pressed()
        if teclas_pulsadas[pg.K_UP]:
            self.vy = -10
        elif teclas_pulsadas[pg.K_DOWN]:
            self.vy = 10
        else:
            self.vy = 0



class Asteroidex3():
    w=50
    h=50
    def __init__(self):
        self.x = -self.w
        self.y = random.randint(0, 550)
        self.vx = 4
        self.image = pg.image.load("recursos/imagenes/aster1-50x50.png")
        # self.rect = self.image.get_rect(x = self.x, y = self.y)
        self.rect = pg.Surface.get_rect(self.image)



    def actualizar(self):
        self.x -= self.vx
        self.rect.x -= self.vx
        if self.x <= -50:
            self.x = 850
            self.rect.x = 850
            self.y = random.randint(0, 550)
            self.rect.y = self.y
            self.vx = random.randint(2, 10)




class asteroide():
    imagenes_files = ['asteroides_01.png', 'asteroides_02.png', 'asteroides_03.png', 'asteroides_04.png',  'asteroides_05.png',
                        'asteroides_06.png',  'asteroides_07.png', 'asteroides_08.png', 'asteroides_09.png', 'asteroides_10.png',
                        'asteroides_11.png',  'asteroides_12.png', 'asteroides_13.png', 'asteroides_14.png', 'asteroides_15.png',
                        'asteroides_16.png',  'asteroides_18.png', 'asteroides_19.png', 'asteroides_20.png', 'asteroides_21.png',
                        'asteroides_22.png',  'asteroides_23.png', 'asteroides_24.png', 'asteroides_25.png', 'asteroides_26.png', 
                        'asteroides_27.png',  'asteroides_28.png', 'asteroides_29.png', 'asteroides_30.png', 'asteroides_31.png']

    retardo_anim = 5  # mientras mas aumenta en valor mas lenta es la animacion

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.image_act = 0     # contador inicializado en 0
        self.ciclos_tras_refresco = 0  # contador de ciclos para  velocidad de la animacion
        self.imagenes = self.cargaImagenes()
        self.image = self.imagenes[self.image_act] 
        self.rect = self.image.get_rect(x=x,y=y)
        # self.circleRadius = pg.Surface.get_rect(self.image)[0]/2

    def cargaImagenes(self):
        lista_imagenes = []
        for img in self.imagenes_files:
            lista_imagenes.append(pg.image.load(f"recursos/imagenes/{img}"))
        return lista_imagenes

    def actualizar_posicion(self):

        # Gestionar posicion del asteroide

        if self.rect.x <= -128:
            self.rect.x = 928
            self.rect.y = random.randint(0, 472)
        self.rect.x -= self.vx

    def actualizar_imagen(self):

        # Gestionar imagen activa (disfraz de asteroide)

        self.ciclos_tras_refresco += 1
        if self.ciclos_tras_refresco % self.retardo_anim == 0:
            self.image_act += 1
            if self.image_act >= len(self.imagenes):
                self.image_act = 0
        self.image = self.imagenes[self.image_act]


    def actualizar(self):
        self.actualizar_posicion()
        self.actualizar_imagen()


class Game:
    def __init__(self):
        self.clock = pg.time.Clock()      
        self.pantalla = pg.display.set_mode( GAME_DIMENSIONS )
        self.bg = pg.image.load("recursos/imagenes/fondo-800x600.jpg")
        pg.display.set_caption("Futuro space ship")
        self.stop_level = False
        self.finish_level = False
        self.crash_nave = False
        self.nivel = Nivel(1, 10)
        self.nivel_cont = 1
        self.vidas = 3
        self.puntos = 0
        self.goalRect = pg.Rect(0, 0, 1, 600)
        self.asteroide = asteroide( 928, 236, 5, 0)
        self.planet1 = pg.image.load("recursos/imagenes/planet-450x461.png")

        self.aster = []
        for i in range(random.randint(2, 7)):
        # for i in range (2):
            ax3 = Asteroidex3()
            ax3.vx = random.randint(2, 15)
            self.aster.append(ax3)
        
        self.nave = nave( 10, 275, 0)

        self.explote = Explote()
        self.mygroup = pg.sprite.Group(self.explote)


    # bucle principal   
    def bucle_principal(self):        
        game_over = False
        stop_level = False
        contador = 0

        while not game_over:
            # Gestión de eventos
            events = pg.event.get()
            self.clock.tick(FPS)
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            if not self.stop_level:
                self.nave.manejar_eventos()
                # Zona de Actualización de elementos del juego       
                self.nave.actualizar()
                self.nivel.asteroide.actualizar()

                for aster in self.nivel.aster :
                    aster.actualizar()
                # Zona de pintado de elementos 
                
                # self.pantalla.fill((11, 44, 94))       
                self.pantalla.blit(self.bg, (0, 0))
                self.pantalla.blit(self.nivel.asteroide.image, (self.nivel.asteroide.rect.x, self.nivel.asteroide.rect.y))

                # colision
                allAsters = []
                allAsters.append(self.nivel.asteroide.rect)
                for aster in self.nivel.aster :
                    allAsters.append(aster.rect)
                    self.pantalla.blit(aster.image, (aster.x, aster.y))
                    # pintar de rectangulo del asteroide grande
                    # pg.draw.rect(self.pantalla,(0, 255, 0), aster.rect) 

                if  self.nave.rect.collidelistall(allAsters):
                    self.explote.explote_sound()    
                    self.stop_level = True
                    self.crash_nave = True
                    allAsters = []
                self.pantalla.blit(self.nave.image, (self.nave.x, self.nave.y))
                # pg.draw.rect(self.pantalla,(255, 0, 0), self.goalRect) # control de puntos
                if  self.goalRect.collidelistall(allAsters):
                    self.puntos += 1
                if self.puntos > self.nivel.meta_nivel:
                    self.stop_level = True
                    self.finish_level = True
        
            if self.stop_level:
                if self.crash_nave:                  
                    SURF.blit( create_font("Perdiste", 32, (255, 255, 255)), ((GAME_DIMENSIONS[0] / 2) ,(GAME_DIMENSIONS)[1] / 2))
                    contador += 1
                    if contador < len(self.explote.imagenes) * self.explote.retardo_anim:
                        self.pantalla.blit(self.bg, (0, 0))
                        self.pantalla.blit((self.explote.image), (self.nave.x, self.nave.y - self.nave.getHeight()/ 2))
                        self.explote.update()
                    if contador > 500:
                        self.vidas -= 1
                        contador = 0
                        self.nivel.update_nivel()
                        self.stop_level = False
                        self.crash_nave = False
                elif self.finish_level:
                    self.pantalla.blit(self.bg, (0, 0))
                    self.pantalla.blit(self.planet1, ((GAME_DIMENSIONS[0] - pg.Surface.get_width(self.planet1) / 2 ), (0 + (GAME_DIMENSIONS[1] - pg.Surface.get_height(self.planet1)) / 2 ) ))
                    # • Aparecerá un planeta por la parte derecha de la pantalla.
                    # • Dejarán de aparecer obstáculos pero los que estén en pantalla deberán continuar su movimiento hasta
                    # el borde derecho o chocar con la nave.
                    # • La nave girará 180 grados y aterrizará sobre el planeta de forma automática
                    # • Aparecerá un cartel que indique "Pulse <tecla elegida por el programador> para continuar"
                    # • Si fuera el último nivel el cartel sería de felicitación e indicaría acción para reiniciar el juego.
                    # • Si el jugador no iniciara la partida transcurrido un tiempo, se volverá a la portada.


            
            SURF.blit( create_font("Nivel:" + str(self.nivel_cont), 32, (255, 255, 255)), ((GAME_DIMENSIONS[0] / 6) * 0, 0))
            SURF.blit( create_font("Vidas:" + str(self.vidas), 32, (255, 255, 255)), ((GAME_DIMENSIONS[0] / 6) * 2, 0))
            SURF.blit( create_font("Puntos:" + str(self.puntos), 32, (255, 255, 255)), ((GAME_DIMENSIONS[0] / 6) * 4, 0))


            # Zona de refrescar pantalla
            pg.display.flip()

