import pkg_resources
import pygame

from pypipboy import pypboy
from pypipboy import game
from pypipboy.pypboy.ui import MenuItem


class Module(pypboy.SubModule):

    LABEL = "Status"
    headline = "STATUS"
    title = " HP 160/175  |  AP 62/62"

    def __init__(self, parent, configfile=None):
        super(Module, self).__init__(parent, configfile)
        self.add(Health())
        self.menu.add_item(MenuItem("CND", self.call_test))
        self.menu.add_item(MenuItem("RAD"))

    def call_test(self, menuitem):
        print(menuitem)


class Health(game.Entity):

    def __init__(self):
        super(Health, self).__init__()
        image = pygame.image.load(pkg_resources.resource_filename('pypipboy', 'data/images/pipboy.png'))
        self.rect = image.get_rect()
        self.image = image.convert()
        self.rect[0] = 4
        self.rect[1] = 40
