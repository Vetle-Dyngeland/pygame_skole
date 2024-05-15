from pygame import Color

from components.collider import Collider
from components.image import Image
from components.horizontal_movement import HorizontalMovement
from components.tilemap import Tilemap
from components.transform import Transform
from components.velocity import Velocity
from components.gravity_user import GravityUser
from ecs import EcsController
from resources.collision import CollisionManager
from resources.gravity import Gravity
from resources.time import Time

# Define all systems ABOVE the SystemManager, then place them in the according functions
# This is to make it easier to order the systems without adding a dependency or setting
# up a compex system management section into the EcsManager


def initialize_resources(ecs_controller: EcsController):
    ecs_controller.add_resource(Time())
    ecs_controller.add_resource(CollisionManager())
    ecs_controller.add_resource(Gravity())


def make_image(ecs_controller: EcsController):
    ecs_controller.spawn([
        Transform(position=(0, 0)),
        Velocity(),
        Collider(),
        Image(Color(255, 105, 105)),
        HorizontalMovement(),
        GravityUser(),
    ])


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
