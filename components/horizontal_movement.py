from components.velocity import Velocity
from resources.time import Time
from ecs import Component, EcsController
import pygame


class HorizontalMovement(Component):

    def __init__(self,
                 keys: list[int] = [pygame.K_RIGHT, pygame.K_LEFT],
                 max_speed: float = 300,
                 acceleration_force: float = 3000,
                 decceleration_multi: float = 0.8):
        self.keys = keys
        self.max_speed = max_speed
        self.acceleration_force = acceleration_force
        self.decceleration_multi = decceleration_multi
        self.velocity: Velocity
        self.time: Time

    def ready(self, ecs_controller: EcsController):
        self.time = ecs_controller.get_resource(Time)

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
        move_value: float = pressed[self.keys[0]] - pressed[self.keys[1]]

        self.accelerate(move_value)
        self.deccelerate()

    def accelerate(self, move_value: float):
        def sign(x): return 0 if x == 0 else abs(x) / x

        self.velocity.x += move_value * self.acceleration_force * self.time.delta_time
        over_max_speed = abs(self.velocity.x) > self.max_speed
        moving_same_direction = sign(self.velocity.x) == sign(move_value)
        if over_max_speed and moving_same_direction:
            self.velocity.x = move_value * self.max_speed

    def deccelerate(self):
        self.velocity.x *= self.decceleration_multi
        self.velocity.x *= int(abs(self.velocity.x) >= 0.01)
