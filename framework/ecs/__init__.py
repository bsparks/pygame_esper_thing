import esper


class Processor(esper.Processor):
    def dispatch_event(self, event_name, *args, **kwargs):
        esper.dispatch_event(event_name, *args, **kwargs)

    def add_listener(self, event_name, callback):
        esper.set_handler(event_name, callback)

    def remove_listener(self, event_name, callback):
        esper.remove_handler(event_name, callback)

    def on_added_to_world(self, world):
        pass

    def on_removed_from_world(self, world):
        pass


class World(esper.World):
    def add_processor(self, processor_instance: Processor, priority=0) -> None:
        super().add_processor(processor_instance, priority)
        processor_instance.on_added_to_world(self)

    def remove_processor(self, processor_type: esper._Type[Processor]) -> None:
        self.get_processor(processor_type).on_removed_from_world(self)
        super().remove_processor(processor_type)

    def create_entity(self, *components: esper._C) -> int:
        entity = super().create_entity(*components)
        esper.dispatch_event("entity_created", entity)
        return entity

    def add_component(self, entity: int, component: esper._C) -> None:
        super().add_component(entity, component)
        esper.dispatch_event("component_added", entity, component)

    def remove_component(self, entity: int, component_type: esper._Type[esper._C]) -> None:
        super().remove_component(entity, component_type)
        esper.dispatch_event("component_removed", entity, component_type)
