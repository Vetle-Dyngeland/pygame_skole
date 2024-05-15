from pygame import Vector2

from components.transform import Transform
from ecs import Component, EcsController
from resources.time import Time


class Velocity(Component):

    def __init__(self):
        self.transform: Transform
        self.vel = Vector2(0, 0)
        self.time: Time

    def ready(self, ecs_controller: EcsController):
        self.transform = self.get_transform()
        self.time = ecs_controller.get_resource(Time)

    def update(self, ecs_controller: EcsController):
        self.transform.position += self.vel * self.time.delta_time

    def get_transform(self) -> Transform:
        for component in self.entity.components:
            if type(component) == Transform:
                return component
        raise KeyError(
            f"Component '{Transform}' not found in entity {self.entity}")
