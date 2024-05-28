from ecs import Component, EcsController
from resources.time import Time
from components.velocity import Velocity
from components.collider import Collider

import pygame


class Jumper(Component):
    def __init__(self,
                 key: int = pygame.K_UP,
                 jump_force: float = 600,
                 coyote_time: float = 0.4,
                 jump_buffer: float = 0.2):
        self.jump_key: int = key
        self.jump_force: float = jump_force
        self.coyote_time: float = coyote_time
        self.jump_buffer: float = jump_buffer

        self.coyote_timer: float = coyote_time
        self.jump_buffer_timer: float = jump_buffer
        self.collider: Collider | None = None
        self.time: Time
        self.velocity: Velocity

        self.jump_just_held: bool = False

    def ready(self, ecs_controller: EcsController):
        self.time = ecs_controller.get_resource(Time)
        self.velocity = self.get_velocity()

    def get_velocity(self) -> Velocity:
        for c in self.entity.components:
            if type(c) == Velocity:
                return c
        raise KeyError(
            f"Component 'Velocity' not found for object {self.entity}")

    def update(self, _: EcsController):
        if self.collider is None:
            self.collider = self.get_collider()
        self.update_timers()
        self.handle_jumps()

    def get_collider(self) -> Collider | None:
        for c in self.entity.components:
            if type(c) == Collider:
                return c
        return None

    def grounded(self) -> bool:
        return self.collider.touching_ground

    # slow
    def jump_pressed(self) -> bool:
        held = pygame.key.get_pressed()[self.jump_key]
        val = held and not self.jump_just_held
        self.jump_just_held = held
        return val

    def update_timers(self):
        self.coyote_timer += self.time.delta_time
        self.coyote_timer *= int(not self.grounded())

        self.jump_buffer_timer += self.time.delta_time
        self.jump_buffer_timer *= int(not self.jump_pressed())

    def handle_jumps(self):
        holding_jump: bool = self.jump_buffer_timer < self.jump_buffer
        grounded: bool = self.coyote_timer < self.coyote_time
        if grounded and holding_jump:
            self.jump()

    def jump(self):
        self.velocity.y -= self.jump_force\
            + self.velocity.y * int(self.velocity.y < 0)
        self.coyote_timer = self.coyote_time
        self.jump_buffer_timer = self.jump_buffer
