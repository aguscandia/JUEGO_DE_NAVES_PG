import pygame as pg
from Space_ship import GAME_DIMENSIONS

import random
import sys

pg.init()

class asteroide:
    imagenes_files = ['asteroides_01.png','asteroides_02.png','asteroides_03.png','asteroides_04.png',  'asteroides_05.png',
                        'asteroides_06.png',  'asteroides_07.png', 'asteroides_08.png', 'asteroides_09.png', 'asteroides_10.png',
                        'asteroides_11.png',  'asteroides_12.png', 'asteroides_13.png', 'asteroides_14.png', 'asteroides_15.png',
                        'asteroides_16.png',  'asteroides_18.png', 'asteroides_19.png', 'asteroides_20.png', 'asteroides_21.png',
                        'asteroides_22.png',  'asteroides_23.png', 'asteroides_24.png', 'asteroides_25.png', 'asteroides_26.png', 
                        'asteroides_27.png',  'asteroides_28.png', 'asteroides_29.png', 'asteroides_30.png', 'asteroides_31.png']

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.image_act = 0     # contador inicializado en 0
        self.imagenes = self.cargaImagenes()
        self.image = self.imagenes[self.image_act]

        self.rect = self.image.get_rect(x=x,y=y)

    def cargaImagenes(self):
        lista_imagenes = []
        for img in self.imagenes_files:
            print(img)
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
        self.asteroide = asteroide( 928, 236,6, 0)


    def bucle_principal(self):           
        game_over = False

        while not game_over:
            events = pg.event.get()
            self.clock.tick(60)
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
        


            self.asteroide.actualizar()
            self.pantalla.fill((11, 44, 94))

            self.pantalla.blit(self.asteroide.image, (self.asteroide.rect.x, self.asteroide.rect.y))

            pg.display.flip()