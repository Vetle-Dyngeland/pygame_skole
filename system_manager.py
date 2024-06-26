import pygame
from pygame import Color

from components.collider import Collider
from components.gravity_user import GravityUser
from components.horizontal_movement import HorizontalMovement
from components.image import Image
from components.jumper import Jumper
from components.tilemap import Tilemap
from components.transform import Transform
from components.velocity import Velocity

from ecs import EcsController
from resources.collision import CollisionManager
from resources.gravity import Gravity
from resources.time import Time
from resources.tilemap_creation import TilemapCreation
from resources.event_manager import EventManager

# Define all systems ABOVE the class, and place them in the according functions
# This is to order the systems without adding a dependency or setting
# up a comlpex system management section into the EcsManager


def initialize_resources(ecs_controller: EcsController):
    ecs_controller.add_resource(Time())
    ecs_controller.add_resource(CollisionManager())
    ecs_controller.add_resource(Gravity())
    ecs_controller.add_resource(EventManager())


def make_image(ecs_controller: EcsController):
    ecs_controller.spawn([
        Transform(position=(0, 0)),
        Velocity(0, 0),
        Collider(),
        Image(Color(255, 255, 255), pygame.image.load(
            "./files/images/p1_stand.png")),
        HorizontalMovement(),
        GravityUser(),
        Jumper()
    ])


def make_tilemap(ecs_controller: EcsController):
    tilemap = Tilemap(image_path="./files/images/tiles_spritesheet.png",
                      file_path="./files/tilemap.csv")
    ecs_controller.spawn([
        Transform(),
        Collider(),
        tilemap
    ])

    ecs_controller.add_resource(TilemapCreation(tilemap))


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
