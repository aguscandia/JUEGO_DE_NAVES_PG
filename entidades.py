import pygame as pg

class asteroide:
    def __init__(self, x, y, vx, vy, color, escala):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.escala = escala 

        self.image = pg.Surface((self.escala, self.escala))
        self.image.fill(self.color)
    
        self.rect = self.image.get_rect(x=x,y=y)

    