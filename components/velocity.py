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
        self.set_transform()
        self.set_time(ecs_controller)

    def update(self, ecs_controller: EcsController):
        self.transform.position += self.vel * self.time.delta_time

    def set_transform(self):
        for component in self.entity.components:
            if type(component) == Transform:
                self.transform = component
                return
        raise KeyError(
            f"Component '{Transform}' not found for object {self.entity}")

    def set_time(self, ecs: EcsController):
        query = ecs.get_resource(Time)
        if type(query) != Time:
            raise KeyError(f"Could not find resource of type '{Time}'")
        self.time = query
