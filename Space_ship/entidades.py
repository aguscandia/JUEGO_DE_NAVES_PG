import pygame as pg
from Space_ship import GAME_DIMENSIONS, FPS

import random
import sys

pg.init()

# fuente
pg.font.init()


def create_font(t, s=72, c=(255, 255, 0), b=False, i=False):
    font = pg.font.SysFont("Arial", s, bold=b, italic=i)
    text = font.render(t, True, c)
    return text


GAME_OVER_FONT = create_font("GAME OVER")
SURF = pg.display.set_mode(GAME_DIMENSIONS)

class Planet:
    def __init__(self):
        self.image = pg.image.load("recursos/imagenes/planet-450x461.png")
        self.x = GAME_DIMENSIONS[0]
        self.y = (GAME_DIMENSIONS[1] - pg.Surface.get_height(self.image)) / 2

    def move(self, x, y):
        self.x += x
        self.y += y

    def getWidth(self):
        return pg.Surface.get_width(self.image)



class Nivel:
    def __init__(self, n, m):
        self.stop_level = False
        self.ending_level = False
        self.finish_level = False
        self.bigAsters = []
        self.aster = []
        self.nivel = n
        self.puntos = 0
        self.update_nivel()
        self.meta_nivel = m
        self.finalizando = False

    def update_nivel(self):
        for i in range(random.randint(2, 7)):
            ax3 = Asteroidex3()
            ax3.vx = random.randint(2, 15)
            self.aster.append(ax3)

        # for i in range(random.randint(2, 7)):
        for i in range(1):
            ax3 = asteroide()
            #   ax3.vx = random.randint(2, 15)
            self.bigAsters.append(ax3)

    def actualizarBigAsters(self):
        for bigAster in self.bigAsters:
            bigAster.actualizar(self.finalizando)

    def actualizarAsters(self):
        for aster in self.aster:
            aster.actualizar(self.finalizando)

    def tieneAsteroides(self):
        totalAsteroides = []
        for bigAster in self.bigAsters:
            totalAsteroides.append(bigAster.rect.x < - pg.Surface.get_width(bigAster.image))
        for aster in self.aster:
            totalAsteroides.append(aster.x < - pg.Surface.get_width(aster.image))
        return not all(totalAsteroides)

    def restart(self):
        self.bigAsters = []
        self.aster = []
        self.update_nivel()

    def get_numeroNivel(self):
        return self.nivel


class Explote(pg.sprite.Sprite):
    imagenes_files = ['explote100x100_01.png', 'explote100x100_02.png', 'explote100x100_03.png',
                      'explote100x100_04.png', 'explote100x100_05.png',
                      'explote100x100_06.png', 'explote100x100_07.png', 'explote100x100_08.png',
                      'explote100x100_09.png', 'explote100x100_10.png',
                      'explote100x100_11.png', 'explote100x100_12.png', 'explote100x100_13.png',
                      'explote100x100_14.png', 'explote100x100_15.png',
                      'explote100x100_16.png', 'explote100x100_18.png', 'explote100x100_19.png',
                      'explote100x100_20.png']

    def __init__(self):
        super(Explote, self).__init__()
        self.image_act = 0
        self.imagenes = self.cargaImagenes()
        self.image = self.imagenes[self.image_act]
        self.rect = pg.Rect(5, 5, 150, 198)
        self.ciclos_tras_refresco = 0
        self.retardo_anim = 5

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
        pg.mixer.music.set_volume(0.1)

class nave:

    def __init__(self, x, y, vy):
        self.angle = 0
        self.vc = 5   # velocidad crucero
        self.x = x
        self.y = y
        self.vy = vy
        self.image = pg.image.load("recursos/imagenes/nave-75x50.png")
        self.rect = pg.Surface.get_rect(self.image)
        self.rect.top = y
        self.rect.left = x
        self.setDimension()
        self.printPos = (0, 0)
        self.printImage = self.image

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
        self.printPos = (self.x, self.y)
        self.printImage = self.image
        if self.angle != 0:
            # Antes de hacer la transformación (rotación) me guardo las coordenadas del centro de mi nave original
            centro_naveX = self.rect.centerx
            centro_naveY = self.rect.centery
            # Roto la nave el angulo angulo y la guardo en una nueva surface (nave_rotadaS)
            nave_rotadaS = pg.transform.rotozoom(self.image, self.angle, 1)
            # Obtengo el rectángulo de mi nueva surface CENTRADO EN LA POSICION GUARDADA ANTES
            rectanguloRot = nave_rotadaS.get_rect(centerx=centro_naveX, centery=centro_naveY)
            self.printPos = rectanguloRot
            self.printImage = nave_rotadaS

    def naveAterrizando(self):
        # si la nave esta por abajo de la mitad de la pantalla tiene que acelerar hacia arriba
        # si la nave esta por arriba de la mitad de la pantalla tiene que acelerar hacia abajo
        # si la nave esta en el centro y la nave no este en el final de la pantalla tiene que acelerar en x
        # si la nave esta al final de la pantalla menos su ancho girar 180° y no aterrizar mas.
        if self.y < GAME_DIMENSIONS[1] / 2:
            self.y += self.vc
            self.rect.top += self.vc
        if self.y > GAME_DIMENSIONS[1] / 2:
            self.y -= self.vc
            self.rect.top -= self.vc
        if self.y == GAME_DIMENSIONS[1] / 2 and not self.x == GAME_DIMENSIONS[0] - self.width:
            self.x += self.vc
            self.rect.left += self.vc
        if self.x == GAME_DIMENSIONS[0] - self.width and self.angle < 180: # hasta que siga girando vaya aumentando de a 1
            self.angle += 1

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
    w = 50
    h = 50

    def __init__(self):
        self.x = -self.w
        self.y = random.randint(0, 550)
        self.vx = 4
        self.image = pg.image.load("recursos/imagenes/aster1-50x50.png")
        # self.rect = self.image.get_rect(x = self.x, y = self.y)
        self.rect = pg.Surface.get_rect(self.image)

    def actualizar(self, finalizando):
        self.x -= self.vx
        self.rect.x -= self.vx
        if self.x <= -50 and not finalizando:
            self.x = 850
            self.rect.x = 850
            self.y = random.randint(0, 550)
            self.rect.y = self.y
            self.vx = random.randint(2, 10)


class asteroide():
    imagenes_files = ['asteroides_01.png', 'asteroides_02.png', 'asteroides_03.png', 'asteroides_04.png',
                      'asteroides_05.png',
                      'asteroides_06.png', 'asteroides_07.png', 'asteroides_08.png', 'asteroides_09.png',
                      'asteroides_10.png',
                      'asteroides_11.png', 'asteroides_12.png', 'asteroides_13.png', 'asteroides_14.png',
                      'asteroides_15.png',
                      'asteroides_16.png', 'asteroides_18.png', 'asteroides_19.png', 'asteroides_20.png',
                      'asteroides_21.png',
                      'asteroides_22.png', 'asteroides_23.png', 'asteroides_24.png', 'asteroides_25.png',
                      'asteroides_26.png',
                      'asteroides_27.png', 'asteroides_28.png', 'asteroides_29.png', 'asteroides_30.png',
                      'asteroides_31.png']

    retardo_anim = 5  # mientras mas aumenta en valor mas lenta es la animacion

    def __init__(self):
        self.x = 928
        self.y = random.randint(2, 15)
        self.vx = 5
        self.vy = 0
        self.image_act = 0  # contador inicializado en 0
        self.ciclos_tras_refresco = 0  # contador de ciclos para  velocidad de la animacion
        self.imagenes = self.cargaImagenes()
        self.image = self.imagenes[self.image_act]
        self.rect = self.image.get_rect(x=self.x, y=self.y)
        # self.circleRadius = pg.Surface.get_rect(self.image)[0]/2

    def cargaImagenes(self):
        lista_imagenes = []
        for img in self.imagenes_files:
            lista_imagenes.append(pg.image.load(f"recursos/imagenes/{img}"))
        return lista_imagenes

    def actualizar_posicion(self, finalizando):

        # Gestionar posicion del asteroide

        if self.rect.x <= -128 and not finalizando:
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

    def actualizar(self, finalizando):
        self.actualizar_posicion(finalizando)
        self.actualizar_imagen()


class Game:
    def __init__(self):
        self.timeLeft = 0
        self.numeroDeNiveles = 1
        self.puntosAcumulados = 0
        self.planet1 = Planet()
        self.clock = pg.time.Clock()
        self.pantalla = pg.display.set_mode(GAME_DIMENSIONS)
        self.bg = pg.image.load("recursos/imagenes/fondo-800x600.jpg")
        pg.display.set_caption("Futuro space ship")
        self.crash_nave = False
        self.nivel = Nivel(1, 10)
        self.vidas = 3
        self.puntos = 0
        self.goalRect = pg.Rect(0, 0, 1, 600)
        self.nave = nave(10, 275, 0)
        self.explote = Explote()

    # bucle principal
    def bucle_principal(self):
        game_over = False
        contador = 0

        while not game_over:
            # Gestión de eventos

            events = pg.event.get()
            self.clock.tick(FPS)
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            if not self.nivel.stop_level:
                self.nave.manejar_eventos()

                # Zona de Actualización de elementos del juego

                self.nave.actualizar()
                self.nivel.actualizarAsters()
                self.nivel.actualizarBigAsters()

                # Zona de pintado de elementos

                # self.pantalla.fill((11, 44, 94))       
                self.pantalla.blit(self.bg, (0, 0))

                # colision

                allAsters = []
                for aster in self.nivel.aster:
                    allAsters.append(aster.rect)
                    self.pantalla.blit(aster.image, (aster.x, aster.y))
                for bigAster in self.nivel.bigAsters:
                    allAsters.append(bigAster.rect)
                    self.pantalla.blit(bigAster.image, (bigAster.rect.x, bigAster.rect.y))

                if self.nave.rect.collidelistall(allAsters):
                    self.explote.explote_sound()
                    self.nivel.stop_level = True
                    self.crash_nave = True
                    allAsters = []
                self.pantalla.blit(self.nave.image, (self.nave.x, self.nave.y))
                # pg.draw.rect(self.pantalla,(255, 0, 0), self.goalRect) # control de puntos
                if self.goalRect.collidelistall(allAsters):
                    self.puntos += 1

                if self.puntos > self.nivel.meta_nivel:
                    self.nivel.finalizando = True
                if self.puntos > self.nivel.meta_nivel and not self.nivel.tieneAsteroides():
                    self.nivel.stop_level = True
                    self.nivel.ending_level = True
                    self.nave.vy = 0

            if self.nivel.stop_level:
                if self.crash_nave:
                    textoVidas = create_font("No Te Rindas!, Inténtalo De Nuevo", 32, (255, 255, 255))
                    SURF.blit(textoVidas, ((GAME_DIMENSIONS[0] - textoVidas.get_width()) / 2, GAME_DIMENSIONS[1] / 2))
                    contador += 1
                    if contador < len(self.explote.imagenes) * self.explote.retardo_anim:
                        self.pantalla.blit(self.bg, (0, 0))
                        self.pantalla.blit(self.explote.image, (self.nave.x, self.nave.y - self.nave.getHeight() / 2))
                        self.explote.update()
                    if contador > 200:
                        self.vidas -= 1
                        contador = 0
                        self.nivel.restart()
                        self.nivel.stop_level = False
                        self.crash_nave = False
                        self.nivel.finalizando = False
                elif self.nivel.ending_level:
                    self.pantalla.blit(self.bg, (0, 0))

                    while self.planet1.x != (GAME_DIMENSIONS[0] - self.planet1.getWidth() / 2):
                        self.planet1.move(-0.25, 0)
                        self.pantalla.blit(self.bg, (0, 0))
                        self.pantalla.blit(self.planet1.image, (self.planet1.x, self.planet1.y))
                        self.pantalla.blit(self.nave.image, (self.nave.x, self.nave.y))
                        pg.display.flip()
                    self.nave.naveAterrizando()
                    self.nave.actualizar()
                    self.pantalla.blit(self.planet1.image, (self.planet1.x, self.planet1.y))
                    self.pantalla.blit(self.nave.printImage, self.nave.printPos)
                    if self.nave.angle == 180:
                        self.nivel.finish_level = True
                        self.nivel.ending_level = False
                        self.timeLeft = pg.time.get_ticks() # siempre va a ir en aumento el tiempo actual
                elif self.nivel.finish_level:

                    if self.nivel.get_numeroNivel() >= self.numeroDeNiveles:
                        textLevelComplete = create_font(" Juego Completado!, Pulse Enter ", 32, (255, 255, 255))
                        SURF.blit(textLevelComplete,((GAME_DIMENSIONS[0] - textLevelComplete.get_width()) / 2, GAME_DIMENSIONS[1] / 2))

                        tecla_pulsada = pg.key.get_pressed()
                        if tecla_pulsada[pg.K_RETURN]:
                            self.puntosAcumulados = 0
                            self.puntos = 0
                            self.vidas = 3
                            self.nivel = Nivel(1, 30)
                            self.nave = nave(10, 275, 0)

                        if ((pg.time.get_ticks() - self.timeLeft) / 1000) > 5:
                            self.irAlaPortada()

                    else:
                        textLevelComplete = create_font(" Nivel " + str(self.nivel.nivel) + " Completado! Pulse Enter para continuar ",32, (255, 255, 255))
                        SURF.blit(textLevelComplete, ((GAME_DIMENSIONS[0] - textLevelComplete.get_width()) / 2, GAME_DIMENSIONS[1] / 2))

                        tecla_pulsada = pg.key.get_pressed()
                        if tecla_pulsada[pg.K_RETURN]:
                            self.puntosAcumulados = self.nivel.puntos
                            self.nivel = Nivel(self.nivel.get_numeroNivel() + 1, 30)
                            self.nave = nave(10, 275, 0)

                    # cambiar meta de puntos por tiempo
                    # game over
                    # tablas de puntaje


            SURF.blit(create_font("Nivel:" + str(self.nivel.nivel), 32, (255, 255, 255)),((GAME_DIMENSIONS[0] / 6) * 0, 0))
            SURF.blit(create_font("Vidas:" + str(self.vidas), 32, (255, 255, 255)), ((GAME_DIMENSIONS[0] / 6) * 2, 0))
            SURF.blit(create_font("Puntos:" + str(self.puntos), 32, (255, 255, 255)), ((GAME_DIMENSIONS[0] / 6) * 4, 0))

            # Zona de refrescar pantalla
            pg.display.flip()

    def irAlaPortada(self):
        portada = True
        while portada:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            # self.pantalla.blit(self.bg, (0, 0))
            self.pantalla.fill((11, 44, 94))
            textPortada = create_font(" Pulse Enter para continuar ", 32, (255, 255, 255))
            SURF.blit(textPortada, ((GAME_DIMENSIONS[0] - textPortada.get_width()) / 2, GAME_DIMENSIONS[1] / 2))

            tecla_pulsada = pg.key.get_pressed()
            if tecla_pulsada[pg.K_RETURN]:
                self.puntosAcumulados = 0
                self.puntos = 0
                self.vidas = 3
                self.nivel = Nivel(1, 30)
                self.nave = nave(10, 275, 0)
                portada = False

            pg.display.flip()


