import pygame
from pypipboy.pypboy import SubModule

from pypipboy.modules.map.entities import Map


class MapModule(SubModule):

    LABEL = "Map"
    headline = "Basic Map"
    title = " Cityname"

    MAPNAME = None

    def __init__(self, parent):
        super(MapModule, self).__init__(parent)
        if self.MAPNAME is None:
            raise NotImplementedError('Map need MAPNAME')

        mapgrid = Map(
            self.parent.pipboy,
            self.parent.pipboy.display.width,
            pygame.Rect(
                4,
                (self.parent.pipboy.display.width - self.parent.pipboy.display.height) / 2,
                self.parent.pipboy.display.width - 8, self.parent.pipboy.display.height - 80
            )
        )
        mapgrid.fetch_map(
            (
                self.parent.pipboy.configfile.getfloat('MAP', 'longitude'),
                self.parent.pipboy.configfile.getfloat('MAP', 'latitude')
            ),
            self.parent.pipboy.configfile.getfloat('MAP', 'zoom_{}'.format(self.MAPNAME))
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
