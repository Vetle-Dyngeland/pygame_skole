from resources.time import Time
from components.gravity_user import GravityUser
from ecs import Resource, EcsController


class Gravity(Resource):

    def __init__(self, force: float = 1000):
        self.force: float = force
        self.time: Time
        self.gravity_users: list[GravityUser] = []

    def ready(self, ecs_controller: EcsController):
        self.time = ecs_controller.get_resource(Time)

    def get_gravity_users(self, ecs: EcsController) -> list[GravityUser]:
        return [c[0] for c in ecs.query_components([GravityUser])]

    def update(self, ecs_controller: EcsController):
        if len(self.gravity_users) == 0:
            self.gravity_users = self.get_gravity_users(ecs_controller)

        for user in self.gravity_users:
            user.velocity.y += self.force\
                * self.time.delta_time\
                * user.multi
