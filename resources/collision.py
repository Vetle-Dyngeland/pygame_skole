from components.tilemap import Tilemap
from components.transform import Transform
from components.velocity import Velocity
from components.collider import Collider
from resources.time import Time
from ecs import EcsController, Resource
from pygame import Rect, Vector2


def get_collisions(rect: Rect, colliders: list[Rect]) -> list[Rect]:
    return [collider for collider in colliders if rect.colliderect(collider)]


def is_colliding_with_any(rect: Rect, colliders: list[Rect]) -> bool:
    return any(rect.colliderect(collider) for collider in colliders)


def move(rect: Rect, velocity: Vector2, colliders: list[Rect]) -> Vector2:
    colliders.remove(rect)
    first_rect = rect.copy()
    rect.x += velocity.x
    hit_list = get_collisions(rect, colliders)
    for tile in hit_list:
        if velocity.x > 0:
            rect.right = tile.left
        else:
            rect.left = tile.right

    rect.y += velocity.y
    hit_list = get_collisions(rect, colliders)
    for tile in hit_list:
        if velocity.y > 0:
            rect.bottom = tile.top
        else:
            rect.top = tile.bottom

    return Vector2(rect.center) - Vector2(first_rect.center)


def get_all_tilemap_rects(ecs: EcsController) -> list[Rect]:
    tilemaps: list[Tilemap] = [t[0] for t in
                               ecs.query_components([Tilemap, Collider])]

    return [t[1] for tilemap in tilemaps for t in tilemap.draw_map]


def get_all_collidable_rects(ecs: EcsController,
                             colliders: list[Collider] | None
                             ) -> list[Rect]:
    if colliders is None:
        colliders = [c[0] for c in
                     ecs.query_components([Collider], [Tilemap])]

    return [col.transform.rect for col in colliders] +\
        get_all_tilemap_rects(ecs)


def get_static_colliders(ecs: EcsController) -> list[Rect]:
    colliders = [c[0] for c in ecs.query_components([Collider],
                                                    [Tilemap, Velocity])]
    return get_all_collidable_rects(
        ecs,
        colliders=colliders)


def get_dynamic_colliders(ecs: EcsController) -> list[Transform]:
    return [c[0] for c in ecs.get_components([Collider]) if c.velocity != None]


class CollisionManager(Resource):
    def __init__(self):
        self.static_colliders: list[Rect] = None
        self.dynamic_colliders: list[Collider] = None
        self.time: Time

    def ready(self, ecs_controller: EcsController):
        self.time = ecs_controller.get_resource(Time)

    def update(self, ecs_controller: EcsController):
        if self.static_colliders is None or self.dynamic_colliders is None:
            self.static_colliders = get_static_colliders(ecs_controller)
            self.dynamic_colliders = get_dynamic_colliders(ecs_controller)

        rects = self.static_colliders + \
            [col.transform.rect for col in self.dynamic_colliders]

        dynamic = [(col, col.transform.rect)
                   for col in self.dynamic_colliders]

        for (col, rect) in dynamic:
            col.velocity.vel = move(col.transform.rect,
                                    col.velocity.vel * self.time.delta_time,
                                    rects) / self.time.delta_time
