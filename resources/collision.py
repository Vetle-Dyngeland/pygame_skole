from pygame import Rect, Vector2

from components.collider import Collider
from components.tilemap import Tilemap
from components.velocity import Velocity
from ecs import EcsController, Resource
from resources.time import Time


def get_collisions(rect: Rect, colliders: list[Rect]) -> list[Rect]:
    close = [
        col for col in colliders
        if Vector2(rect.center).distance_squared_to(Vector2(col.center)) <= (
            max(col.width, col.height) + max(rect.width, rect.height))**2
    ]
    return [col for col in close if rect.colliderect(col)]


def move(rect: Rect, velocity: Vector2, colliders: list[Rect]) -> (Vector2, Vector2):
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


def get_all_tilemap_rects(ecs: EcsController) -> list[Rect]:
    tilemaps: list[Tilemap] = [
        t[0] for t in ecs.query_components([Tilemap, Collider])
    ]

    return [t[1] for tilemap in tilemaps for t in tilemap.draw_map]


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
    return get_all_collidable_rects(ecs, colliders=colliders)


def get_dynamic_colliders(ecs: EcsController) -> list[Collider]:
    return [
        c[0] for c in ecs.query_components([Collider])
        if c[0].velocity != None
    ]


class CollisionManager(Resource):

    def __init__(self):
        self.static_colliders: list[Rect] = []
        self.dynamic_colliders: list[Collider] = []
        self.time: Time

    def ready(self, ecs_controller: EcsController):
        self.time = ecs_controller.get_resource(Time)

    def reset_colliders(self):
        self.static_colliders = []
        self.dynamic_colliders = []

    def update(self, ecs_controller: EcsController):
        if len(self.static_colliders) == 0 or len(self.dynamic_colliders) == 0:
            self.static_colliders = get_static_colliders(ecs_controller)
            self.dynamic_colliders = get_dynamic_colliders(ecs_controller)

        self.handle_collisions()

    def handle_collisions(self):
        dynamic = [(col, col.transform.rect) for col in self.dynamic_colliders]
        if len(dynamic) == 0:
            return

        rects = self.static_colliders + \
            [col.transform.rect for col in self.dynamic_colliders]

        for (col, rect) in dynamic:
            (new_vel, new_pos) = move(col.transform.rect,
                                      col.velocity.vel * self.time.delta_time,
                                      rects)
            col.transform.pos = new_pos
            col.velocity.vel = new_vel / self.time.delta_time
