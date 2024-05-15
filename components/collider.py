from components.transform import Transform
from components.velocity import Velocity
from ecs import Component, EcsController


class Collider(Component):

  def __init__(self):
    self.transform: Transform
    self.velocity: Velocity | None

  def ready(self, _: EcsController):
    self.transform = self.get_transform()
    self.velocity = self.get_velocity()

  def get_transform(self) -> Transform:
    for component in self.entity.components:
      if type(component) == Transform:
        return component
    raise KeyError(f"Component 'Transform' not found for object {self.entity}")

  def get_velocity(self) -> Velocity | None:
    for component in self.entity.components:
      if type(component) == Velocity:
        return component
    return None
