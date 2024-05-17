import pygame
from pygame import Color, Surface

from components.transform import Transform
from constants import DEFAULT_SHAPE_SIZE
from ecs import Component, EcsController


class Image(Component):

  def __init__(self,
               color: Color = Color(255, 255, 255),
               surface: Surface | None = None):
    self.transform: Transform
    if surface != None:
      self.surface = surface
      return
    self.surface = Surface(DEFAULT_SHAPE_SIZE)
    self.surface.fill(color)

  def ready(self, _: EcsController):
    self.transform = self.get_transform()
    self.surface = pygame.transform.scale(self.surface, self.transform.size)

  def draw(self, _: EcsController, surface: Surface):
    surface.blit(self.surface, self.transform.position)

  def get_transform(self) -> Transform:
    for component in self.entity.components:
      if type(component) == Transform:
        return component
    raise KeyError(f"Component 'Transform' not found for object {self.entity}")
