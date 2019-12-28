import pygame
from pypipboy import pypboy

from pypipboy.modules.data import entities


class Module(pypboy.SubModule):

    LABEL = "Local Map"

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        mapgrid = entities.Map(self.parent.pypboy, self.parent.pypboy.display.width, pygame.Rect(4, (self.parent.pypboy.display.width - self.parent.pypboy.display.height) / 2, self.parent.pypboy.display.width - 8, self.parent.pypboy.display.height - 80))
        mapgrid.fetch_map(
            (
                self.parent.pypboy.configfile.getfloat('MAP', 'longitude'),
                self.parent.pypboy.configfile.getfloat('MAP', 'latitude')
            ),
            self.parent.pypboy.configfile.getfloat('MAP', 'zoom_local')
        )
        self.add(mapgrid)
        mapgrid.rect[0] = 4
        mapgrid.rect[1] = 40
