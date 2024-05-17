from pygame import Vector2

from ecs import Component, EcsController


class Velocity(Vector2, Component):

  def __init__(self, x: float, y: float):
    super().__init__(x, y)

  def update(self, ecs_controller: EcsController):
    pass
