import pygame
import constantes
import extra_anim

class Personaje:
    def __init__(self, x, y, animaciones_caminando, animaciones_idle, animaciones_agachar,
                  animaciones_salto, animaciones_caer, animacion_ataque_estatico):
        self.animaciones_caminando = animaciones_caminando
        self.animaciones_idle = animaciones_idle
        self.animaciones_agachar = animaciones_agachar
        self.animaciones_salto = animaciones_salto
        self.animaciones_caer = animaciones_caer  
        self.animacion_ataque_estatico = animacion_ataque_estatico
        self.ataque_activo = False
        self.frame_ataque_actual = 0
        self.tiempo_ataque = pygame.time.get_ticks()
        self.frame_actual = 0
        self.flip = False
        self.en_movimiento = False
        self.agachado = False
        self.salto = False
        self.velocidad_salto = constantes.velocidad_salto
        self.gravedad = constantes.gravedad
        self.velocidad_y = 0
        self.en_suelo = constantes.en_suelo
        self.tiempo_cambio_animacion = pygame.time.get_ticks()
        self.tiempo_cambio_animacion_caer = pygame.time.get_ticks()  # Temporizador específico para caer

        self.textura = self.animaciones_idle[self.frame_actual]
        self.rect = self.textura.get_rect()
        self.rect.center = (x, y)

    # Creamos la función para el ataque estático
    def ataque(self):
        if not self.ataque_activo:
            self.ataque_activo = True
            self.frame_ataque_actual = 0
            self.tiempo_ataque = pygame.time.get_ticks()

    # Aquí estará todo el movimiento y los frames para las animaciones
    def movimiento(self, delta_x, agacharse, saltar):
        if self.ataque_activo:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ataque > 32:  # Cambia el frame cada 32 ms
                self.frame_ataque_actual = (self.frame_ataque_actual + 1) % len(self.animacion_ataque_estatico)
                self.textura = self.animacion_ataque_estatico[self.frame_ataque_actual]
                self.tiempo_ataque = tiempo_actual

                if self.frame_ataque_actual == len(self.animacion_ataque_estatico) - 1:
                    self.ataque_activo = False
                    self.textura = self.animaciones_idle[self.frame_actual]
        else:
            if saltar and self.en_suelo:
                self.velocidad_y = self.velocidad_salto
                self.en_suelo = False
                self.salto = True

            self.velocidad_y += self.gravedad
            self.rect.y += self.velocidad_y

            if self.rect.bottom > constantes.ALTO_ventana:
                self.rect.bottom = constantes.ALTO_ventana
                self.velocidad_y = 0
                self.en_suelo = True
                self.salto = False

            self.rect.x += delta_x

            if delta_x < 0:
                self.flip = True
            elif delta_x > 0:
                self.flip = False

            tiempo_actual = pygame.time.get_ticks()
            
            if agacharse:
                if tiempo_actual - self.tiempo_cambio_animacion > 100:
                    self.frame_actual = (self.frame_actual + 1) % len(self.animaciones_agachar)
                    self.textura = self.animaciones_agachar[self.frame_actual]
                    self.tiempo_cambio_animacion = tiempo_actual
            elif self.velocidad_y < 0:
                if tiempo_actual - self.tiempo_cambio_animacion > 100:
                    self.salto = True
                    self.frame_actual = (self.frame_actual + 1) % len(self.animaciones_salto)
                    self.textura = self.animaciones_salto[self.frame_actual]
                    self.tiempo_cambio_animacion = tiempo_actual
            elif self.velocidad_y > 0 and not self.en_suelo:
                if tiempo_actual - self.tiempo_cambio_animacion_caer > 100:
                    self.salto = False
                    self.frame_actual = (self.frame_actual + 1) % len(self.animaciones_caer)
                    self.textura = self.animaciones_caer[self.frame_actual]
                    self.tiempo_cambio_animacion_caer = tiempo_actual
            elif delta_x != 0:
                if tiempo_actual - self.tiempo_cambio_animacion > 100:
                    self.frame_actual = (self.frame_actual + 1) % len(self.animaciones_caminando)
                    self.textura = self.animaciones_caminando[self.frame_actual]
                    self.tiempo_cambio_animacion = tiempo_actual
            else:
                if tiempo_actual - self.tiempo_cambio_animacion > 100:
                    self.frame_actual = (self.frame_actual + 1) % len(self.animaciones_idle)
                    self.textura = self.animaciones_idle[self.frame_actual]
                    self.tiempo_cambio_animacion = tiempo_actual

    # Dibujamos el personaje dentro del juego
    def dibujar(self, interfaz):
        if self.flip:
            image_flip = pygame.transform.flip(self.textura, flip_x=True, flip_y=False)
            interfaz.blit(image_flip, self.rect)
        else:
            interfaz.blit(self.textura, self.rect)


class Enemigo(Personaje):
    def __init__(self, x, y, animaciones_caminando, animaciones_idle, animaciones_agachar,
                 animaciones_salto, animaciones_caer, animacion_ataque_estatico,
                 animaciones_enemigos):
        # Llamada al constructor de la clase base
        super().__init__(x, y, animaciones_caminando, animaciones_idle, animaciones_agachar,
                         animaciones_salto, animaciones_caer, animacion_ataque_estatico)
        
        # Agregamos los atributos específicos para enemigos
        self.animaciones_enemigos = animaciones_enemigos
        self.frame_enemigo_actual = 0
        self.tiempo_enemigo = pygame.time.get_ticks()

    def movimiento(self, delta_x, agacharse, saltar):
        super().movimiento(delta_x, agacharse, saltar)
        
        # Actualización específica para enemigos
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_enemigo > 150:  # Cambia el frame cada 150 ms para enemigos
            self.frame_enemigo_actual = (self.frame_enemigo_actual + 1) % len(self.animaciones_enemigos)
            self.textura = self.animaciones_enemigos[self.frame_enemigo_actual]
            self.tiempo_enemigo = tiempo_actual

    def dibujar(self, interfaz):
        super().dibujar(interfaz)
