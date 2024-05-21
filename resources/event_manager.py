import pygame

from ecs import Resource


class EventManager(Resource):
    def __init__(self):
        self.events = None

    def update(self, _):
        self.events = pygame.event.get()
        if len([ev for ev in self.events if ev.type == pygame.QUIT]):
            pygame.quit()
