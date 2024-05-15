import pygame

from constants import BACKGROUND_COLOR, SCREEN_SIZE
from ecs import EcsController
from system_manager import SystemManager


class Game:
  running: bool = True

  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_SIZE.x, SCREEN_SIZE.y))

    self.ecs: EcsController = EcsController()
    self.systems: SystemManager = SystemManager(self.ecs)
    self.ecs.ready()

  def update(self):
    self.handle_quitting()
    self.ecs.update()
    self.systems.update()

  def handle_quitting(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False

  def draw(self):
    self.screen.fill(BACKGROUND_COLOR)
    self.ecs.draw(self.screen)
    self.systems.draw()

    pygame.display.update()


game: Game = Game()

while game.running:
  game.update()
  game.draw()
