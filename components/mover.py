from components.velocity import Velocity
from ecs import Component, EcsController
from pygame import Vector2
import pygame


class Mover(Component):

    def __init__(
            self,
            keys: list[int] = [pygame.K_d, pygame.K_a, pygame.K_s, pygame.K_w],
            max_speed: float = 100,
            acceleration_force: float = 100,
            decceleration_multi: float = 0.8):
        self.keys = keys
        self.max_speed = max_speed
        self.acceleration_force = acceleration_force
        self.decceleration_multi = decceleration_multi
        self.velocity: Velocity

    def ready(self, _: EcsController):
        self.set_velocity()

    def set_velocity(self):
        vel = self.get_velocity()
        if vel is not None:
            self.velocity = vel
            return

        self.velocity = Velocity()
        self.entity.components.append(self.velocity)

    def get_velocity(self) -> Velocity | None:
        for component in self.entity.components:
            if type(component) == Velocity:
                return component
        return None

    def update(self, ecs_controller: EcsController):
        pressed = pygame.key.get_pressed()
        move_vector: Vector2 = Vector2(pressed[self.keys[0]] -
                                       pressed[self.keys[1]],
                                       pressed[self.keys[2]] -
                                       pressed[self.keys[3]])

        if move_vector.length_squared() > 0:
            self.accelerate(move_vector)
        else:
            self.deccelerate()

    def accelerate(self, move_vector: Vector2):
        self.velocity.vel += move_vector.normalize() * self.acceleration_force
        if self.velocity.vel.length_squared() > self.max_speed**2:
            self.velocity.vel = self.velocity.vel.normalize() * self.max_speed

    def deccelerate(self):
        self.velocity.vel *= self.decceleration_multi
        self.velocity.vel *= \
            int(self.velocity.vel.length_squared() >= 0.01)
