from pygame import Rect, Vector2, quit

from components.collider import Collider
from components.tilemap import Tilemap
from components.velocity import Velocity
from ecs import EcsController, Resource
from resources.time import Time

DANGERS: list[list[int]] = [[7, 0], [5, 11], [4, 12]]

DIE_COUNTER_MAX = 1


def get_collisions(rect: Rect, colliders: list[Rect]) -> list[Rect]:
    close = [
        col for col in colliders
        if Vector2(rect.center).distance_squared_to(Vector2(col.center)) <= (
            max(col.width, col.height) + max(rect.width, rect.height))**2
    ]
    return [col for col in close if rect.colliderect(col)]


def move(rect: Rect,
         velocity: Vector2,
         colliders: list[Rect]) -> tuple[Vector2, Vector2]:
    if rect in colliders:
        colliders.remove(rect)

    rect.x += int(velocity.x)
    hit_list = get_collisions(rect, colliders)
    for tile in hit_list:
        if velocity.x > 0:
            rect.right = tile.left
        else:
            rect.left = tile.right
    velocity.x *= int(len(hit_list) == 0)

    rect.y += int(velocity.y)
    hit_list = get_collisions(rect, colliders)
    for tile in hit_list:
        if velocity.y > 0:
            rect.bottom = tile.top
        else:
            rect.top = tile.bottom
    velocity.y *= int(len(hit_list) == 0)

    return (velocity, Vector2(rect.topleft))


def is_danger(tile_rect: Rect, tilemap: Tilemap) -> bool:
    print([int(tile_rect.x / tilemap.tile_size),
           int(tile_rect.y / tilemap.tile_size)])
    return [int(tile_rect.x / tilemap.tile_size),
            int(tile_rect.y / tilemap.tile_size)] in DANGERS


def get_all_tilemap_rects(ecs: EcsController) -> list[Rect]:
    tilemaps: list[Tilemap] = [
        t[0] for t in ecs.query_components([Tilemap, Collider])
    ]

    return [t[0] for tilemap in tilemaps for t in tilemap.draw_map if not is_danger(t[1], tilemap)]


def get_all_collidable_rects(ecs: EcsController,
                             colliders: list[Collider] = []) -> list[Rect]:
    if len(colliders) == 0:
        colliders = [c[0] for c in ecs.query_components([Collider], [Tilemap])]

    return [col.transform.rect for col in colliders] +\
        get_all_tilemap_rects(ecs)


def get_static_colliders(ecs: EcsController) -> list[Rect]:
    colliders = [
        c[0] for c in ecs.query_components([Collider], [Tilemap, Velocity])
    ]
    return get_all_collidable_rects(ecs, colliders)


def get_dynamic_colliders(ecs: EcsController) -> list[Collider]:
    return [
        c[0] for c in ecs.query_components([Collider])
        if c[0].velocity != None
    ]


def get_dangerous(ecs: EcsController) -> list[Rect]:
    tilemaps = [
        c[0] for c in ecs.query_components([Tilemap, Collider])
    ]
    return [t[0] for tilemap in tilemaps for t in tilemap.draw_map if is_danger(t[1], tilemap)]


class CollisionManager(Resource):

    def __init__(self):
        self.static_colliders: list[Rect] = []
        self.dynamic_colliders: list[Collider] = []
        self.dangerous_oo: list[Rect] = []
        self.time: Time

    def ready(self, ecs_controller: EcsController):
        self.time = ecs_controller.get_resource(Time)

    def reset_colliders(self):
        self.static_colliders = []
        self.dynamic_colliders = []
        self.dangerous_oo = []

    def update(self, ecs_controller: EcsController):
        if len(self.static_colliders) == 0 or len(self.dynamic_colliders) == 0:
            self.static_colliders = get_static_colliders(ecs_controller)
            self.dynamic_colliders = get_dynamic_colliders(ecs_controller)
            self.dangerous_oo = get_dangerous(ecs_controller)

        self.handle_collisions()

    def handle_collisions(self):
        if len(self.dynamic_colliders) == 0:
            return

        rects = self.static_colliders + \
            [col.transform.rect for col in self.dynamic_colliders]
        for col in self.dynamic_colliders:
            (new_vel, new_pos) = move(col.transform.rect,
                                      col.velocity * self.time.delta_time,
                                      rects)
            col.transform.position = new_pos

            col.touching_wall = bool(
                col.velocity.x * self.time.delta_time != new_vel.x)
            col.velocity.x = new_vel.x / self.time.delta_time

            col.touching_ground = bool(
                col.velocity.y * self.time.delta_time != new_vel.y)
            col.velocity.y = new_vel.y / self.time.delta_time

        for col in self.dynamic_colliders:
            if len(get_collisions(col.transform.get_rect(), self.dangerous_oo)):
                quit()
