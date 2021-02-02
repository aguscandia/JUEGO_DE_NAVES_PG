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




class asteroide:
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
        pg.display.set_caption("Futuro space ship")
        self.asteroide = asteroide( 928, 236, 5, 0)
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
                # metodo movimiento de nave 
                '''
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.nave.y -= 10
                        if self.nave.y <= 0:
                            self.nave.y = 0


                    if event.key == pg.K_DOWN:
                        self.nave.y += 10
                        if self.nave.y + 50 >= GAME_DIMENSIONS[1]:
                            self.nave.y = GAME_DIMENSIONS[1] - 50
                '''

        # metodo movimiento de nave con get pressed

            teclas_pulsadas = pg.key.get_pressed()
            if teclas_pulsadas[pg.K_UP]:
                self.nave.vy = -10
            elif teclas_pulsadas[pg.K_DOWN]:
                self.nave.vy = 10
            else:
                self.nave.vy = 0


            # Zona de Actualización de elementos del juego

            self.nave.actualizar()
            self.asteroide.actualizar()

            self.pantalla.fill((11, 44, 94))
            self.pantalla.blit(self.asteroide.image, (self.asteroide.rect.x, self.asteroide.rect.y))
            self.pantalla.blit(self.nave.image, (self.nave.x, self.nave.y))

            # Zona de refrescar pantalla
            pg.display.flip()