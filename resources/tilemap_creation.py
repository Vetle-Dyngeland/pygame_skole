import pygame
from pygame import Surface, Rect

from components.tilemap import Tilemap
from ecs import Resource, EcsController
from resources.event_manager import EventManager
from resources.collision import CollisionManager


class TilemapCreation(Resource):
    def __init__(
        self,
        tilemap: Tilemap,
        toggle_key: int = pygame.K_SPACE,
        select_axis_change_key: int = pygame.K_LCTRL,
        eraser_key: int = pygame.K_e,
        save_key: int = pygame.K_s,
        reload_colliders_key: int = pygame.K_r
    ):
        self.tilemap: Tilemap = tilemap
        self.edit_mode: bool = False
        self.toggle_just_held: bool = False
        self.just_saved: bool = False
        self.just_reloaded_colliders: bool = False

        self.toggle_key: int = toggle_key
        self.select_axis_change_key: int = select_axis_change_key
        self.eraser_key: int = eraser_key
        self.save_key: int = save_key
        self.reload_colliders_key: int = reload_colliders_key

        self.selected_tile: list[int] = [0, 0]
        self.brush: list[int] = [0, 0]
        self.before_eraser_brush: list[int] = [0, 0]

        self.event_manager: EventManager

    def ready(self, ecs_controller: EcsController):
        self.event_manager = ecs_controller.get_resource(EventManager)

    def update(self, ecs_controller: EcsController):
        self.handle_toggle()
        if not self.edit_mode:
            return

        self.brush_selection()
        self.tile_selection()
        self.draw_tilemap()
        self.misc_keymaps(ecs_controller)

    def handle_toggle(self):
        held = pygame.key.get_pressed()[self.toggle_key]
        if held and not self.toggle_just_held:
            self.edit_mode = not self.edit_mode
        self.toggle_just_held = held

    def brush_selection(self):
        if pygame.key.get_pressed()[self.eraser_key]:
            if self.brush != [-1, -1]:
                self.before_eraser_brush = self.brush
                self.brush = [-1, -1]
            return

        if self.brush == [-1, -1]:
            self.brush = self.before_eraser_brush

        if pygame.mouse.get_pressed()[1]:
            brush = self.tilemap.tiles[self.selected_tile[0]
                                       ][self.selected_tile[1]]
            if brush[0] >= 0:
                self.brush = brush

        wheel_delta = next((
            ev.y for ev in self.event_manager.events
            if ev.type == pygame.MOUSEWHEEL), 0)

        idx = int(not pygame.key.get_pressed()[self.select_axis_change_key])
        self.brush[idx] += wheel_delta

        if self.brush[idx] < 0:
            self.brush[idx] = self.tilemap.tile_amount[idx]
        self.brush[idx] %= self.tilemap.tile_amount[idx]

    def tile_selection(self):
        self.selected_tile = [
            int(pygame.mouse.get_pos()[1] / self.tilemap.tile_size),
            int(pygame.mouse.get_pos()[0] / self.tilemap.tile_size)]

    def draw_tilemap(self):
        if not pygame.mouse.get_pressed()[0]:
            return

        self.expand_tilemap_to(self.selected_tile[0], self.selected_tile[1])
        self.tilemap.tiles[self.selected_tile[0]
                           ][self.selected_tile[1]] = self.brush.copy()
        self.set_draw_map_tile()

    def set_draw_map_tile(self):
        tile_rect = self.get_selected_tile_rect()
        self.tilemap.draw_map = [
            tile for tile in self.tilemap.draw_map if tile[0] != tile_rect]
        self.tilemap.draw_map.append(self.get_selected_tile_draw_map())

    def expand_tilemap_to(self, x: int, y: int):
        while len(self.tilemap.tiles) <= x:
            self.tilemap.tiles.append(
                [[-1, -1] for i in range(x)])
        while len(self.tilemap.tiles[x]) <= y:
            for line in self.tilemap.tiles:
                line.append([-1, -1])

    def misc_keymaps(self, ecs: EcsController):
        pressed = pygame.key.get_pressed()
        self.saving(pressed)
        self.reloading_colliders(pressed, ecs)

    def saving(self, pressed):
        if not pressed[self.save_key] or not pressed[pygame.K_LCTRL]:
            self.just_saved = False
            return

        if self.just_saved:
            return

        self.tilemap.save_file()
        self.just_saved = True

    def reloading_colliders(self, pressed, ecs: EcsController):
        if not pressed[self.reload_colliders_key]\
                or not pressed[pygame.K_LCTRL]:
            self.just_reloaded_colliders = False
            return
        if self.just_reloaded_colliders:
            return

        ecs.get_resource(CollisionManager).reset_colliders()
        self.just_reloaded_colliders = True

    def draw(self, _, surface: Surface):
        if not self.edit_mode:
            return

        draw_map = self.get_selected_tile_draw_map()
        surface.blit(self.tilemap.image, draw_map[0], draw_map[1])

    def get_selected_tile_draw_map(self) -> tuple[Rect, Rect]:
        return (
            self.get_selected_tile_rect(),
            self.get_selected_brush_rect(),
        )

    def get_selected_tile_rect(self) -> Rect:
        return Rect(
            self.selected_tile[1] * self.tilemap.tile_size,
            self.selected_tile[0] * self.tilemap.tile_size,
            self.tilemap.tile_size,
            self.tilemap.tile_size,
        )

    def get_selected_brush_rect(self) -> Rect:
        return Rect(
            self.brush[0] * self.tilemap.tile_size,
            self.brush[1] * self.tilemap.tile_size,
            self.tilemap.tile_size,
            self.tilemap.tile_size,
        )
