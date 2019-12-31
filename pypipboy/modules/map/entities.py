import os
import threading
import pkg_resources
import pygame
from pypipboy.game.core import Entity
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

    def __init__(self, pipboy, width, render_rect=None):
        super(Map, self).__init__((width, width))
        self.pipboy = pipboy
        self.map_icons = {}
        for icon in pkg_resources.resource_listdir('pypipboy', self._map_icon_path):
            icon_name = icon.rsplit('.', 1)[0]
            self.map_icons[icon_name] = pygame.image.load(pkg_resources.resource_filename(
                'pypipboy', os.path.join(self._map_icon_path, icon)
            ))
        self.amenities = {
            key: self.map_icons[value]
            for key, value
            in self.pipboy.configfile.items('MAPICONS')
        }

        self._mapper = Maps()
        self._size = width
        self._map_surface = pygame.Surface((width, width))
        self._render_rect = render_rect
        text = self.pipboy.fonts[14].render("Loading map...", True, (95, 255, 177), (0, 0, 0))
        self.image.blit(text, (10, 10))

    def fetch_map(self, position, radius):
        self._fetching = threading.Thread(target=self._internal_fetch_map, args=(position, radius))
        self._fetching.start()

    def _internal_fetch_map(self, position, radius):
        self._mapper.fetch_by_coordinate(position, radius)
        self.redraw_map()

    def move_map(self, x, y):  # pylint: disable=invalid-name
        self._render_rect.move_ip(x, y)

    def get_map_icon(self, icon_name):
        if icon_name in self.amenities:
            return self.amenities[icon_name]
        print("Unknown amenity: {}".format(icon_name))
        return self.amenities['default']

    def redraw_map(self, coef=1):
        self._map_surface.fill((0, 0, 0))
        for way in self._mapper.transpose_ways(
                (self._size / coef, self._size / coef),
                (self._size / 2, self._size / 2)
        ):
            pygame.draw.lines(
                self._map_surface,
                (85, 251, 167),
                False,
                way,
                2
            )
        for tag in self._mapper.transpose_tags(
                (self._size / coef, self._size / coef),
                (self._size / 2, self._size / 2)
        ):
            image = self.get_map_icon(tag[3])
            pygame.transform.scale(image, (10, 10))
            self._map_surface.blit(image, (tag[1], tag[2]))
            text = self.pipboy.fonts[12].render(tag[0], True, (95, 255, 177), (0, 0, 0))
            self._map_surface.blit(text, (tag[1] + 17, tag[2] + 4))

        self.image.blit(self._map_surface, (0, 0), area=self._render_rect)
