import pygame
from pygame import Surface

from components.tilemap import Tilemap
from ecs import Resource, EcsController
from resources.event_manager import EventManager


class TilemapCreation(Resource):
    def __init__(self,
                 tilemap: Tilemap,
                 toggle_key: int = pygame.K_SPACE,
                 select_axis_change_key: int = pygame.K_LCTRL):
        self.tilemap: Tilemap = tilemap
        self.edit_mode: bool = False
        self.toggle_just_held: bool = False

        self.toggle_key: int = toggle_key
        self.select_axis_change_key: int = select_axis_change_key
        self.event_manager: EventManager

        self.selected_tile: list[int] = [0, 0]
        self.brush: list[int] = [0, 0]

    def ready(self, ecs_controller: EcsController):
        self.event_manager = ecs_controller.get_resource(EventManager)

    def update(self, _):
        self.handle_toggle()
        if not self.edit_mode:
            return

        self.brush_selection()
        self.tile_selection()

    def handle_toggle(self):
        held = pygame.key.get_pressed()[self.toggle_key]
        if held and not self.toggle_just_held:
            self.edit_mode = not self.edit_mode
        self.toggle_just_held = held

    def brush_selection(self):
        mouse_delta: int = next(
            iter([ev.y for ev in self.event_manager.events if ev.type == pygame.MOUSEWHEEL]), 0)

        self.brush[int(not pygame.key.get_pressed()[
            self.select_axis_change_key])] += mouse_delta

    def tile_selection(self):
        mouse_position: tuple[int, int] = tuple(
            [int(v / self.tilemap.tile_size) for v in pygame.mouse.get_pos()])
        print(mouse_position[0], mouse_position[1])

    def draw(self, _, surface: Surface):
        if not self.edit_mode:
            return
