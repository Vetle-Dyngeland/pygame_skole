import pygame
from pygame import Surface

from constants import FRAME_RATE, SHOW_FPS
from ecs import EcsController, Resource


class Time(Resource):

    def __init__(self):
        self.total_time = 0
        self.delta_time = 1
        self.clock = pygame.time.Clock()
        self.font: pygame.font.SysFont

        if not SHOW_FPS:
            return
        self.font = pygame.font.SysFont("Comic Sans MS", 30)

    def update(self, _: EcsController):
        self.delta_time = self.clock.tick(FRAME_RATE) / 1000
        self.total_time += self.delta_time

    def draw(self, ecs_controller: EcsController, surface: Surface):
        if not SHOW_FPS:
            return

        text = self.font.render(f"{1 / self.delta_time}", False, (0, 0, 0))
        surface.blit(text, (0, 0))
