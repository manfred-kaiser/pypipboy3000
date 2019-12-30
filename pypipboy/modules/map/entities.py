import os
import threading
import pkg_resources
import pygame
from pypipboy.game.core import Entity
from pypipboy import config
from pypipboy.pypboy.data import Maps


class Map(Entity):

    _mapper = None
    _transposed = None
    _size = 0
    _fetching = None
    _map_surface = None
    _loading_size = 0
    _render_rect = None

    _map_icon_path = 'data/images/map_icons'

    MAP_ICONS = {}
    AMENITIES = {}

    def __init__(self, pipboy, width, render_rect=None):
        self.pipboy = pipboy
        self.MAP_ICONS = {}
        for icon in pkg_resources.resource_listdir('pypipboy', self._map_icon_path):
            icon_name = icon.rsplit('.', 1)[0]
            self.MAP_ICONS[icon_name] = pygame.image.load(pkg_resources.resource_filename(
                'pypipboy', os.path.join(self._map_icon_path, icon)
            ))
        self.AMENITIES = {
            key: self.MAP_ICONS[value]
            for key, value
            in self.pipboy.configfile.items('MAPICONS')
        }

        self._mapper = Maps()
        self._size = width
        self._map_surface = pygame.Surface((width, width))
        self._render_rect = render_rect
        super(Map, self).__init__((width, width))
        text = self.pipboy.fonts[14].render("Loading map...", True, (95, 255, 177), (0, 0, 0))
        self.image.blit(text, (10, 10))

    def fetch_map(self, position, radius):
        self._fetching = threading.Thread(target=self._internal_fetch_map, args=(position, radius))
        self._fetching.start()

    def _internal_fetch_map(self, position, radius):
        self._mapper.fetch_by_coordinate(position, radius)
        self.redraw_map()

    def move_map(self, x, y):
        self._render_rect.move_ip(x, y)

    def get_map_icon(self, icon_name):
        if icon_name in self.AMENITIES:
            return self.AMENITIES[icon_name]
        print("Unknown amenity: {}".format(icon_name))
        return self.AMENITIES['default']

    def redraw_map(self, coef=1):
        self._map_surface.fill((0, 0, 0))
        for way in self._mapper.transpose_ways((self._size / coef, self._size / coef), (self._size / 2, self._size / 2)):
            pygame.draw.lines(
                self._map_surface,
                (85, 251, 167),
                False,
                way,
                2
            )
        for tag in self._mapper.transpose_tags((self._size / coef, self._size / coef), (self._size / 2, self._size / 2)):
            image = self.get_map_icon(tag[3])
            pygame.transform.scale(image, (10, 10))
            self._map_surface.blit(image, (tag[1], tag[2]))
            text = self.pipboy.fonts[12].render(tag[0], True, (95, 255, 177), (0, 0, 0))
            self._map_surface.blit(text, (tag[1] + 17, tag[2] + 4))

        self.image.blit(self._map_surface, (0, 0), area=self._render_rect)


class MapSquare(Entity):
    _mapper = None
    _size = 0
    _fetching = None
    _map_surface = None
    map_position = (0, 0)

    def __init__(self, size, map_position, parent):
        self._mapper = Maps()
        self._size = size
        self.parent = parent
        self._map_surface = pygame.Surface((size * 2, size * 2))
        self.map_position = map_position
        self.tags = {}
        self.position = None
        super(MapSquare, self).__init__((size, size))

    def fetch_map(self):
        self._fetching = threading.Thread(target=self._internal_fetch_map)
        self._fetching.start()

    def _internal_fetch_map(self):
        self._mapper.fetch_grid(self.map_position)
        self.redraw_map()
        self.parent.redraw_map()

    def redraw_map(self, coef=1):
        self._map_surface.fill((0, 0, 0))
        for way in self._mapper.transpose_ways((self._size, self._size), (self._size / 2, self._size / 2)):
            pygame.draw.lines(
                self._map_surface,
                (85, 251, 167),
                False,
                way,
                1
            )
        for tag in self._mapper.transpose_tags((self._size, self._size), (self._size / 2, self._size / 2)):
            self.tags[tag[0]] = (tag[1] + self.position[0], tag[2] + self.position[1], tag[3])
        self.image.fill((0, 0, 0))
        self.image.blit(self._map_surface, (-self._size / 2, -self._size / 2))


class MapGrid(Entity):

    _grid = None
    _delta = 0.002
    _starting_position = (0, 0)

    def __init__(self, starting_position, dimensions):
        self._grid = []
        self._starting_position = starting_position
        self.dimensions = dimensions
        self._tag_surface = pygame.Surface(dimensions)
        super(MapGrid, self).__init__(dimensions)
        self.tags = {}
        self.fetch_outwards()

    def fetch_outwards(self):
        for x in range(-4, 4):
            for y in range(-2, 2):
                square = MapSquare(
                    86,
                    (
                        self._starting_position[0] + (self._delta * x),
                        self._starting_position[1] - (self._delta * y)
                    ),
                    self
                )
                square.fetch_map()
                square.position = (
                    (86 * x) + (self.dimensions[0] / 2) - 43,
                    (86 * y) + (self.dimensions[1] / 2) - 43
                )
                self._grid.append(square)

    def draw_tags(self):
        self.tags = {}
        for square in self._grid:
            self.tags.update(square.tags)
        self._tag_surface.fill((0, 0, 0))
        for name in self.tags:
            image = self.get_map_icon(self.tags[name][2])
            pygame.transform.scale(image, (10, 10))
            self.image.blit(image, (self.tags[name][0], self.tags[name][1]))
            # try:
            # TODO: Change to Pipboy
            text = config.FONTS[12].render(name, True, (95, 255, 177), (0, 0, 0))
            # text_width = text.get_size()[0]
            #     pygame.draw.rect(
            #         self,
            #         (0, 0, 0),
            #         (self.tags[name][0], self.tags[name][1], text_width + 4, 15),
            #         0
            #     )
            self.image.blit(text, (self.tags[name][0] + 17, self.tags[name][1] + 4))
            #     pygame.draw.rect(
            #         self,
            #         (95, 255, 177),
            #         (self.tags[name][0], self.tags[name][1], text_width + 4, 15),
            #         1
            #     )
            # except Exception, e:
            #     print(e)
            #     pass

    def redraw_map(self):
        self.image.fill((0, 0, 0))
        for square in self._grid:
            self.image.blit(square._map_surface, square.position)
        self.draw_tags()
