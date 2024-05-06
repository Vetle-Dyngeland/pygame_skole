from pygame import Color, Surface

from components.transform import Transform
from constants import DEFAULT_SHAPE_SIZE
from ecs import Component, EcsController


class Image(Component):

    def __init__(self,
                 color: Color = Color(255, 255, 255),
                 surface: Surface = Surface(DEFAULT_SHAPE_SIZE)):
        self.surface = surface
        self.transform: Transform
        self.surface.fill(color)

    def ready(self, _: EcsController):
        self.get_transform()

    def draw(self, _: EcsController, surface: Surface):
        surface.blit(self.surface, self.transform.position)

    def get_transform(self) -> Transform:
        for component in self.entity.components:
            if type(component) == Transform:
                return component
        raise KeyError(
            f"Component 'Transform' not found for object {self.entity}")
