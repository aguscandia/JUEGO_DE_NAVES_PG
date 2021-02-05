import pygame as pg
from Space_ship import GAME_DIMENSIONS, FPS

import random
import sys

pg.init()


class nave:
    def __init__(self, x, y, vy):
        self.x = x
        self.y = y
        self.vy = vy

        self.image = pg.image.load("recursos/imagenes/nave-75x50.png")

    def actualizar(self):
        self.y += self.vy
        if self.y + 50 >= GAME_DIMENSIONS[1]:
            self.y = GAME_DIMENSIONS[1] - 50
        if self.y <= 0:
            self.y = 0

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


    def actualizar(self):
        self.x -= self.vx
        if self.x <= -50:
            self.x = 850
            self.y = random.randint(0, 550)
            self.vx = random.randint(2, 15)



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
        self.asteroide = asteroide( 928, 236, 5, 0)
        self.asteroide2 = asteroide( 928, 116, 4, 0)
        self.asteroide3 = asteroide( 928, 126, 3, 0)
        self.asteroide4 = asteroide( 928, 116, 2, 0)

        self.aster = []
        for i in range(random.randint(2, 7)):
            ax3 = Asteroidex3()
            ax3.vx = random.randint(2, 15)
            self.aster.append(ax3)
        
        self.nave = nave( 10, 275, 0)


    # bucle principal   
    def bucle_principal(self):        
        game_over = False

        while not game_over:
            # Gestión de eventos
            events = pg.event.get()
            self.clock.tick(FPS)
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()


            self.nave.manejar_eventos()

            # Zona de Actualización de elementos del juego

            

            self.nave.actualizar()
            self.asteroide.actualizar()

            self.asteroide2.actualizar()
            self.asteroide3.actualizar()
            self.asteroide4.actualizar()



            for aster in self.aster :
                aster.actualizar()

            # Zona de pintado de elementos 
            
            # self.pantalla.fill((11, 44, 94))       
            self.pantalla.blit(self.bg, (0, 0))
            self.pantalla.blit(self.asteroide.image, (self.asteroide.rect.x, self.asteroide.rect.y))

            self.pantalla.blit(self.asteroide2.image, (self.asteroide2.rect.x, self.asteroide2.rect.y))
            self.pantalla.blit(self.asteroide3.image, (self.asteroide3.rect.x, self.asteroide3.rect.y))
            self.pantalla.blit(self.asteroide4.image, (self.asteroide4.rect.x, self.asteroide4.rect.y))

            for aster in self.aster :
                self.pantalla.blit(aster.image, (aster.x, aster.y))

            self.pantalla.blit(self.nave.image, (self.nave.x, self.nave.y))

            # Zona de refrescar pantalla
            pg.display.flip()

