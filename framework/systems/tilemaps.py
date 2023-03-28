from framework.ecs import Processor
from framework.components import TileMap as TileMapComponent, Position


class TileSet:
    def __init__(self, name, tile_size, image):
        self.name = name
        self.tile_size = tile_size
        self.image = image
        self.tiles = []

    def populate(self):
        width, height = self.image.get_size()
        columns = width // self.tile_size
        rows = height // self.tile_size
        for row in range(rows):
            for column in range(columns):
                tile = self.image.subsurface(
                    (column * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                self.tiles.append(tile)


class TileMap:
    def __init__(self, name, tile_size, tileset, width, height, data):
        self.name = name
        self.tile_size = tile_size
        self.tileset = tileset
        self.width = width
        self.height = height
        self.data = data
        self.world_offset_x = 0
        self.world_offset_y = 0

    def get_tile(self, column, row):
        index = row * self.width + column
        return self.data[index]
    
    def get_tile_index(self, column, row):
        index = row * self.width + column
        return index
    
    def get_tile_index_at_position(self, x, y):
        x -= self.world_offset_x
        y -= self.world_offset_y
        column = int(x // self.tile_size)
        row = int(y // self.tile_size)
        return self.get_tile_index(column, row)

    def get_tile_at_position(self, x, y):
        x -= self.world_offset_x
        y -= self.world_offset_y
        column = int(x // self.tile_size)
        row = int(y // self.tile_size)
        return self.get_tile(column, row)

    def set_tile(self, column, row, tile_index):
        index = row * self.width + column
        self.data[index] = tile_index


class TileMapRenderer(Processor):
    def __init__(self, screen, assets):
        super().__init__()
        self.screen = screen
        self.assets = assets
        self.tilesets = {}
        self.add_listener("component_added", self.on_component_added)

    def on_component_added(self, entity, component):
        if isinstance(component, TileMapComponent):
            self.load_tilemap(entity, component)

    def load_tilemap(self, entity, tilemap):
        tileset = self.tilesets.get(tilemap.tileset, None)
        if tileset is None:
            data = self.assets.load_tileset_data(tilemap.tileset)
            tileset = TileSet(tilemap.tileset, data.tile_size,
                              self.assets.load_image(data.image_name))
            tileset.populate()
            self.tilesets[tilemap.tileset] = tileset
        tilemap.tilemap = TileMap(
            tilemap.name, tileset.tile_size, tileset, tilemap.width, tilemap.height, tilemap.data)

    def render_tilemap(self, tilemap, pos):
        pass

    def process(self, dt, events):
        for ent, (tilemap, pos) in self.world.get_components(TileMapComponent, Position):
            self.render_tilemap(tilemap, pos)
