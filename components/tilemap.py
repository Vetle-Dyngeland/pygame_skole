import csv

import pygame
from pygame import Rect, Surface

import constants
from ecs import Component, EcsController


class Tilemap(Component):
    def __init__(
        self,
        image_path: str,
        file_path: str | None = None,
        tile_size: float = constants.DEFAULT_TILE_SIZE,
        img_tile_size: int = 70,
        tile_amount: tuple[int, int] = (12, 13)
    ):
        self.tile_size: float = tile_size
        self.map_path: str | None = file_path
        self.img_tile_size: int = img_tile_size
        self.tiles: list[list[list[int]]]
        self.draw_map: list[tuple[Rect, Rect]]
        self.tile_amount = tile_amount
        self.image: Surface = pygame.transform.scale(
            pygame.image.load(image_path), (self.tile_size * tile_amount[0],
                                            self.tile_size * tile_amount[1])
        )

    def ready(self, _: EcsController):
        if self.map_path is not None:
            self.load_map()

        self.create_draw_map()

    def load_map(self):
        self.tiles = []
        with open(self.map_path, newline="") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                self.tiles.append([])
                for tile in row:
                    self.load_tile(tile)

    def load_tile(self, tile: str):
        if "^" in tile:
            self.tiles.extend([self.tiles[-1]] * int(tile.removeprefix("^")))
            return
        if "*" in tile:
            self.tiles[-1].extend([self.tiles[-1][-1]] *
                                  int(tile.removeprefix("*")))
            return
        if "-" not in tile:
            self.tiles[-1].append([-1, -1])
            return
        self.tiles[-1].append([int(s) for s in tile.split("-", 1)])

    def create_draw_map(self):
        self.draw_map = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile[0] == -1:
                    continue
                tile_rect = Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )

                image_rect = Rect(
                    tile[0] * self.tile_size,
                    tile[1] * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )

                self.draw_map.append((tile_rect, image_rect))

    def save_file(self):
        map = [[f"{t[0]}-{t[1]}" if t[0] > -1 else "" for t in line]
               for line in self.tiles]
        str_map = "\n".join(",".join(line) for line in map) + "\n"

        file = open(self.map_path, "w")
        file.write(str_map)
        file.close()
        print("File saved!")

    def draw(self, _: EcsController, surface: Surface):
        for tile in self.draw_map:
            surface.blit(self.image, tile[0], tile[1])
