import csv

import pygame
from pygame import Rect, Surface

import constants
from ecs import Component, EcsController

IMG_TILE_SIZE = 70


class Tilemap(Component):

  def __init__(self,
               image_path: str,
               file_path: str | None = None,
               tile_size: float = constants.DEFAULT_TILE_SIZE):
    self.tile_size: float = tile_size
    self.map_path: str | None = file_path
    self.tiles: list[list[(int, int)]]
    self.image = pygame.image.load(image_path)
    self.draw_map: list[(Surface, Rect, Rect)]

  def ready(self, _: EcsController):
    if self.map_path is not None:
      self.load_map()

    self.create_draw_map()

  def load_map(self):
    self.tiles = []
    with open(self.map_path, newline='') as file:
      reader = csv.reader(file, delimiter=",")
      for row in reader:
        self.tiles.append([])
        for tile in row:
          self.load_tile(tile)

  def load_tile(self, tile: str):
    if "*" in tile:
      self.tiles[-1].extend([self.tiles[-1][-1]] * int(tile.removeprefix("*")))
      return
    if "-" not in tile:
      self.tiles[-1].append((-1, -1))
      return
    self.tiles[-1].append(tuple(tile.split("-", 1)))

  def create_draw_map(self):
    self.draw_map = []
    scaled_image = pygame.transform.scale(
        self.image, (self.tile_size * 12, self.tile_size * 12))

    for y, row in enumerate(self.tiles):
      for x, tile in enumerate(row):
        if tile[0] == -1:
          continue
        tile_rect = Rect(x * self.tile_size, y * self.tile_size,
                         self.tile_size, self.tile_size)

        image_rect = Rect(
            float(tile[0]) * self.tile_size,
            float(tile[1]) * self.tile_size, self.tile_size, self.tile_size)

        self.draw_map.append((scaled_image, tile_rect, image_rect))

  def draw(self, ecs_controller: EcsController, surface: Surface):
    for tile in self.draw_map:
      surface.blit(tile[0], tile[1], tile[2])
