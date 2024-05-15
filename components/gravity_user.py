from components.velocity import Velocity
from ecs import Component, EcsController


class GravityUser(Component):

    def __init__(self, multi: float = 1):
        self.multi: float = multi
        self.velocity: Velocity

    def get_velocity(self) -> Velocity | None:
        for component in self.entity.components:
            if type(component) == Velocity:
                return component
        return None

    def ready(self, ecs_controller: EcsController):
        vel = self.get_velocity()
        if vel == None:
            vel = Velocity()
            vel.entity = self.entity
        self.velocity = vel
