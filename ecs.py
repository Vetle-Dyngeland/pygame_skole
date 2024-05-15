from pygame import Surface


class Entity:

    def __init__(self, components=[]):
        self.components = components
        for component in self.components:
            component.entity = self

    def ready(self, ecs_controller):
        for component in self.components:
            component.ready(ecs_controller)

    def update(self, ecs_controller):
        for component in self.components:
            component.update(ecs_controller)

    def draw(self, ecs_controller, drawing_surface: Surface):
        for component in self.components:
            component.draw(ecs_controller, drawing_surface)


class Component:

    def __init__(self):
        pass

    def ready(self, ecs_controller):
        pass

    def update(self, ecs_controller):
        pass

    def draw(self, ecs_controller, surface: Surface):
        pass


class Resource:

    def __init__(self):
        pass

    def ready(self, ecs_controller):
        pass

    def update(self, ecs_controller):
        pass

    def draw(self, ecs_controller, surface: Surface):
        pass


class EcsController:

    resources: list[Resource]
    entities: list[Entity]

    def __init__(self):
        self.resources = []
        self.entities = []

    def ready(self):
        for resource in self.resources:
            resource.ready(self)
        for entity in self.entities:
            entity.ready(self)

    def update(self):
        for resource in self.resources:
            resource.update(self)
        for entity in self.entities:
            entity.update(self)

    def draw(self, surface: Surface):
        for resource in self.resources:
            resource.draw(self, surface)
        for entity in self.entities:
            entity.draw(self, surface)

    def add_resource(self, resource: Resource):
        self.resources.append(resource)

    def spawn(self, bundle: list[Component]) -> Entity:
        entity: Entity = Entity(bundle)
        self.entities.append(entity)
        return entity

    # EXPENSIVE
    def get_components(self, component_type: type) -> list[Component]:
        components: list[Component] = []
        for entity in self.entities:
            for component in entity.components:
                if type(component) == component_type:
                    components.append(component)
        return components

    def get_resource(self, resource_type: type) -> Resource | None:
        for resource in self.resources:
            if type(resource) == resource_type:
                return resource
        return None

    def query(self, has: list[type], exclude: list[type] = []) -> list[Entity]:
        matching = []
        for entity in self.entities:
            has_checklist = sum(
                int(type(component) in has and type(component) not in exclude)
                for component in entity.components)

            if has_checklist >= len(has):
                matching.append(entity)
        return matching

    def query_components(self,
                         has: list[type],
                         exclude: list[type] = []) -> list[list[Component]]:
        matching_entities = self.query(has, exclude)
        return_value = []
        for entity in matching_entities:
            return_value.append([
                component for component_type in has
                for component in entity.components
                if type(component) == component_type
            ])
        return return_value
