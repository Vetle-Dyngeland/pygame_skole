import pygame
from pygame import Surface, Vector2, Rect

from components.tilemap import Tilemap
from ecs import Resource, EcsController
from resources.event_manager import EventManager


class TilemapCreation(Resource):

  def __init__(self,
               tilemap: Tilemap,
               toggle_key: int = pygame.K_SPACE,
               select_axis_change_key: int = pygame.K_LCTRL,
               eraser_key: int = pygame.K_e):
    self.tilemap: Tilemap = tilemap
    self.edit_mode: bool = False
    self.toggle_just_held: bool = False

    self.toggle_key: int = toggle_key
    self.select_axis_change_key: int = select_axis_change_key
    self.eraser_key: int = eraser_key

    self.selected_tile: list[int] = [0, 0]
    self.brush: list[int] = [0, 0]

    self.event_manager: EventManager

  def ready(self, ecs_controller: EcsController):
    self.event_manager = ecs_controller.get_resource(EventManager)

  def update(self, _):
    self.handle_toggle()
    if not self.edit_mode:
      return

    self.brush_selection()
    self.tile_selection()
    self.draw_tilemap()

  def handle_toggle(self):
    held = pygame.key.get_pressed()[self.toggle_key]
    if held and not self.toggle_just_held:
      self.edit_mode = not self.edit_mode
    self.toggle_just_held = held

  def brush_selection(self):
    if pygame.key.get_pressed()[self.eraser_key]:
      self.brush = [-1, -1]
      return

    wheel_delta: int = next(
        iter([
            ev.y for ev in self.event_manager.events
            if ev.type == pygame.MOUSEWHEEL
        ]), 0)

    self.brush[int(not pygame.key.get_pressed()[self.select_axis_change_key]
                   )] += wheel_delta

  def tile_selection(self):
    self.selected_tile = [
        int(v / self.tilemap.tile_size) for v in pygame.mouse.get_pos()
    ]

  def draw_tilemap(self):
    if not pygame.mouse.get_pressed()[0]:
      return
    
    while len(self.tilemap.tiles) < self.selected_tile[1]:
      self.tilemap.tiles.append([])
    while len(
        self.tilemap.tiles[self.selected_tile[1]]) < self.selected_tile[1]:
      self.tilemap.tiles[self.selected_tile[1]].append([])

    self.tilemap.tiles[self.selected_tile[1]][
        self.selected_tile[0]] = self.brush
    self.tilemap.draw_map.append(self.get_selected_tile_draw_map())

  def draw(self, _, surface: Surface):
    if not self.edit_mode:
      return

    draw_map = self.get_selected_tile_draw_map()
    surface.blit(self.tilemap.image, draw_map[0], draw_map[1])

  def get_selected_tile_draw_map(self) -> tuple[Rect, Rect]:
    return (Rect(self.selected_tile[0] * self.tilemap.tile_size,
                 self.selected_tile[1] * self.tilemap.tile_size,
                 self.tilemap.tile_size, self.tilemap.tile_size),
            Rect(self.brush[0] * self.tilemap.tile_size,
                 self.brush[1] * self.tilemap.tile_size,
                 self.tilemap.tile_size, self.tilemap.tile_size))
