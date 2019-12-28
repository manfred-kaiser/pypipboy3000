import pygame
from pypipboy import pypboy

from pypipboy.modules.data import entities


class MapModule(pypboy.SubModule):

    LABEL = "Map"
    headline = "Basic Map"
    title = " Cityname"

    MAPNAME = None

    def __init__(self, *args, **kwargs):
        super(MapModule, self).__init__(*args, **kwargs)
        if self.MAPNAME is None:
            raise NotImplementedError('Map need MAPNAME')

        mapgrid = entities.Map(self.parent.pypboy, self.parent.pypboy.display.width, pygame.Rect(4, (self.parent.pypboy.display.width - self.parent.pypboy.display.height) / 2, self.parent.pypboy.display.width - 8, self.parent.pypboy.display.height - 80))
        mapgrid.fetch_map(
            (
                self.parent.pypboy.configfile.getfloat('MAP', 'longitude'),
                self.parent.pypboy.configfile.getfloat('MAP', 'latitude')
            ),
            self.parent.pypboy.configfile.getfloat('MAP', 'zoom_{}'.format(self.MAPNAME))
        )
        self.add(mapgrid)
        mapgrid.rect[0] = 4
        mapgrid.rect[1] = 40


class WorldMapModule(MapModule):

    MAPNAME = 'world'
    LABEL = 'World'


class LocalMapModule(MapModule):

    MAPNAME = 'local'
    LABEL = 'Local'
