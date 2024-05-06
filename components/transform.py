from pygame import Vector2, Rect

from constants import DEFAULT_SHAPE_SIZE
from ecs import Component


class Transform(Component):

  def __init__(self,
               position: Vector2 = Vector2(0, 0),
               size: Vector2 = DEFAULT_SHAPE_SIZE,
               rotation: float = 0):
    super().__init__()
    self.position = position
    self.size = size
    self.rotation = rotation

  def get_rect(self) -> Rect:
    return Rect(self.position, self.size)

  def set_rect(self, value: Rect):
    self.position = Vector2(value.x, value.y)
    self.size = value.size

  rect = property(get_rect, set_rect)