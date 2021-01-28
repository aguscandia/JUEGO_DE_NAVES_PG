import pygame as pg 
import sys
import random
import entidades 


class Game:
    def __init__(self):
        self.clock = pg.time.Clock()
        self.pantalla = pg.display.set_mode( (800, 600) )
        pg.display.set_caption("Futuro space ship")
        self.asteroide = entidades.asteroide( 770, random.randint(30, 570)
                                            ,10, 0, (255, 0, 0), 30)
 

    def bucle_principal(self):           
        game_over = False

        while not game_over:
            events = pg.event.get()
            self.clock.tick(60)
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
        

        # modificacion de los objetos color velocidad etc.

            if self.asteroide.rect.x <= -30:
                self.asteroide = entidades.asteroide( 770, random.randint(30, 570)
                                                    ,10, 0, (255, 0, 0), 30)

            self.asteroide.rect.x -= self.asteroide.vx



            self.pantalla.fill((11, 44, 94))
            self.pantalla.blit(self.asteroide.image, (self.asteroide.rect.x, self.asteroide.rect.y))

            pg.display.flip()


if __name__ == '__main__':
    pg.init()
    game = Game()
    game.bucle_principal()
