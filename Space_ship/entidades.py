import pygame as pg
from Space_ship import GAME_DIMENSIONS

import random
import sys

pg.init()

class asteroide:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

        self.image = pg.image.load("recursos/imagenes/asteroides_01.png")
        self.rect = self.image.get_rect(x=x,y=y)

    def update(self):
        if self.rect.x <= -128:
            self.rect.x = 928
            self.rect.y = random.randint(0, 472)
        self.rect.x -= self.vx


class Game:
    def __init__(self):
        self.clock = pg.time.Clock()
        self.pantalla = pg.display.set_mode( GAME_DIMENSIONS )
        pg.display.set_caption("Futuro space ship")
        self.asteroide = asteroide( 928, 236,5, 0)


    def bucle_principal(self):           
        game_over = False

        while not game_over:
            events = pg.event.get()
            self.clock.tick(60)
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
        


            self.asteroide.update()

            self.pantalla.fill((11, 44, 94))
            self.pantalla.blit(self.asteroide.image, (self.asteroide.rect.x, self.asteroide.rect.y))

            pg.display.flip()