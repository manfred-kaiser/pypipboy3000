import pygame
from pypipboy import pypboy
from pypipboy import config
from pypipboy.config import CONFIGFILE

from pypipboy.modules.data import entities


class Module(pypboy.SubModule):

    LABEL = "World Map"

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        mapgrid = entities.Map(480, pygame.Rect(0, 0, self.parent.pypboy.display.width - 8, self.parent.pypboy.display.height - 80))
        mapgrid.fetch_map(
            (
                CONFIGFILE.getfloat('MAP', 'longitude'),
                CONFIGFILE.getfloat('MAP', 'latitude')
            ),
            CONFIGFILE.getfloat('MAP', 'zoom_world')
        )
        self.add(mapgrid)
        mapgrid.rect[0] = 4
        mapgrid.rect[1] = 40
