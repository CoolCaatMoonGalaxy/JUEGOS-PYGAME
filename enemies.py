import pygame
import math

class Enemie(pygame.sprite.Sprite):
    def __init__(self, x, y, animaciones_idle, animaciones_walk, animacion_attack, animacion_muerte, energia_enemie):
        super().__init__()
        self.energia_enemie = energia_enemie
        self.animacion_muerte = animacion_muerte
        self.animaciones_idle = animaciones_idle
        self.animaciones_walk = animaciones_walk
        self.animacion_attack = animacion_attack
        self.animacion_actual = self.animaciones_idle
        self.frame_actual = 0
        self.image = self.animacion_actual[self.frame_actual]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.en_movimiento = False
        self.en_atacando = False
        self.tiempo_cambio_animacion = pygame.time.get_ticks()
        self.flip = False
        self.animando_muerte = False
        self.tiempo_muerte = pygame.time.get_ticks()  # Tiempo de inicio de la animación de muerte
        self.intervalo_muerte = 200  # Intervalo de tiempo en milisegundos entre frames de la animación de muerte

        self.rect_colision = pygame.Rect(
            self.rect.x + 1,
            self.rect.y + 1,
            self.rect.width - 15,
            self.rect.height - 15
        )

    def actualizar(self, jugador):
        if self.energia_enemie <= 0:
            if not self.animando_muerte:
                self.animacion_actual = self.animacion_muerte
                self.frame_actual = 0
                self.animando_muerte = True
                self.tiempo_muerte = pygame.time.get_ticks()  # Reiniciar el tiempo para la animación de muerte
            self.animar_muerte()
            return

        pos_jugador = jugador.rect.center
        distancia_x = pos_jugador[0] - self.rect.centerx
        distancia_y = pos_jugador[1] - self.rect.centery
        distancia = math.hypot(distancia_x, distancia_y)
        speed = 3

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_cambio_animacion > 100:
            self.frame_actual = (self.frame_actual + 1) % len(self.animacion_actual)
            self.image = self.animacion_actual[self.frame_actual]
            self.tiempo_cambio_animacion = tiempo_actual

        if distancia < 20:
            self.en_atacando = True
            self.animacion_actual = self.animacion_attack
            self.en_movimiento = False
        elif distancia < 100:
            self.en_atacando = False
            self.en_movimiento = True
            if distancia != 0:
                vector_unitario_x = distancia_x / distancia
                vector_unitario_y = distancia_y / distancia
                self.rect.x += int(speed * vector_unitario_x)
                self.rect.y += int(speed * vector_unitario_y)
            self.animacion_actual = self.animaciones_walk
        else:
            self.en_movimiento = False
            self.en_atacando = False
            self.animacion_actual = self.animaciones_idle

        self.rect_colision.topleft = (self.rect.x + 10, self.rect.y + 10)

        if distancia_x < 0:
            self.flip = True
        elif distancia_x > 0:
            self.flip = False

    def animar_muerte(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_muerte > self.intervalo_muerte:
            if self.frame_actual >= len(self.animacion_muerte) - 1:
                self.kill()  # Elimina el enemigo del grupo
            else:
                self.frame_actual = (self.frame_actual + 1) % len(self.animacion_muerte)
                self.image = self.animacion_muerte[self.frame_actual]
                self.tiempo_muerte = tiempo_actual  # Reinicia el tiempo para el siguiente frame

    def dibujar(self, interfaz):
        if self.flip:
            textura = pygame.transform.flip(self.image, True, False)
            interfaz.blit(textura, self.rect_colision)
        else:
            interfaz.blit(self.image, self.rect_colision)
