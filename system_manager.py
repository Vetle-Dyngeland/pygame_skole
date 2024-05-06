from pygame import Color

from components.tilemap import Tilemap
from components.collider import Collider
from components.mover import Mover
from components.velocity import Velocity
from components.transform import Transform
from components.image import Image
from ecs import EcsController
from resources.time import Time
from resources.collision import CollisionManager

# Define all systems ABOVE the SystemManager, then place them in the according functions
# This is to make it easier to order the systems without adding a dependency or setting
# up a compex system management section into the EcsManager


def initialize_resources(ecs_controller: EcsController):
    ecs_controller.add_resource(Time())
    ecs_controller.add_resource(CollisionManager())


def make_image(ecs_controller: EcsController):
    ecs_controller.spawn([Transform(),
                          Collider(),
                          Image(Color(10, 10, 10))])
    ecs_controller.spawn([Transform(position=(100, 100)),
                          Velocity(),
                          Collider(),
                          Image(Color(255, 105, 105)),
                          Mover()])


def make_tilemap(ecs_controller: EcsController):
    ecs_controller.spawn([
        Transform(),
        Collider(),
        Tilemap(image_path="./files/images/tiles_spritesheet.png",
                file_path="./files/tilemap.csv"),
    ])


class SystemManager:
    ecs_manager: EcsController

    def __init__(self, ecs_manager: EcsController):
        self.ecs_controller = ecs_manager
        self.start()

    def start(self):
        initialize_resources(self.ecs_controller)
        make_image(self.ecs_controller)
        make_tilemap(self.ecs_controller)

    def update(self):
        pass

    def draw(self):
        pass
