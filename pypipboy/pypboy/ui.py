import datetime
from collections import defaultdict

import pkg_resources
import pygame

from pypipboy.game.core import Entity


class Header(Entity):

    def __init__(self, pipboy, headline="", title=""):
        super(Header, self).__init__((
            pipboy.width,
            pipboy.height
        ))
        self.pipboy = pipboy
        self.headline = headline
        self.title = title
        self.rect[0] = 4
        self._date = None

    def render(self, interval=0):
        new_date = datetime.datetime.now().strftime("%d.%m.%y.%H:%M:%S")
        if new_date != self._date:
            self.image.fill((0, 0, 0))
            pygame.draw.line(self.image, (95, 255, 177), (5, 15), (5, 35), 2)
            pygame.draw.line(self.image, (95, 255, 177), (5, 15), (self.pipboy.width - 154, 15), 2)
            pygame.draw.line(self.image, (95, 255, 177), (self.pipboy.width - 154, 15), (self.pipboy.width - 154, 35), 2)
            pygame.draw.line(self.image, (95, 255, 177), (self.pipboy.width - 148, 15), (self.pipboy.width - 13, 15), 2)
            pygame.draw.line(self.image, (95, 255, 177), (self.pipboy.width - 13, 15), (self.pipboy.width - 13, 35), 2)

            text = self.pipboy.fonts[14].render("  %s  " % self.headline, True, (105, 251, 187), (0, 0, 0))
            self.image.blit(text, (26, 8))
            text = self.pipboy.fonts[14].render(self.title, True, (95, 255, 177), (0, 0, 0))
            self.image.blit(text, ((self.pipboy.width - 154) - text.get_width() - 10, 19))
            text = self.pipboy.fonts[14].render(self._date, True, (95, 255, 177), (0, 0, 0))
            self.image.blit(text, ((self.pipboy.width - 141), 19))
            self._date = new_date

        super(Header, self).update()


class FooterMenu(Entity):

    def __init__(self, parent):
        self.menu = []
        self.parent = parent
        self.pipboy = parent.pipboy
        self.selected = None
        super(FooterMenu, self).__init__((self.pipboy.width, self.pipboy.height))
        self.rect[0] = 4
        self.rect[1] = self.pipboy.height - 40
        self._init_modules()

    def _init_modules(self):
        for module in self.parent.submodules:
            self.menu.append(module.LABEL)
        if self.menu:
            self.selected = self.menu[0]
            self.position = (0, self.pipboy.height - 53)

    def select(self, module):
        # self.dirty = 1
        self.selected = module
        self.image.fill((0, 0, 0))
        pygame.draw.line(self.image, (95, 255, 177), (5, 2), (5, 20), 2)
        pygame.draw.line(self.image, (95, 255, 177), (5, 20), (self.pipboy.width - 13, 20), 2)
        pygame.draw.line(self.image, (95, 255, 177), (self.pipboy.width - 13, 2), (self.pipboy.width - 13, 20), 2)

        offset = 20
        for m in self.menu:
            padding = 1
            text_width = 0
            while text_width < 54:
                spaces = " ".join([" " for x in range(padding)])
                text = self.pipboy.fonts[12].render("%s%s%s" % (spaces, m, spaces), True, (105, 255, 187), (0, 0, 0))
                text_width = text.get_size()[0]
                padding += 1
            # print(m+" : "+str(text.get_size()))
            if m == self.selected:
                pygame.draw.rect(
                    self.image,
                    (95, 255, 177),
                    (offset - 2, 6, (text_width + 3), 26),
                    2
                )
            self.image.blit(text, (offset, 12))

            offset = offset + 120 + (text_width - 100)


class Menu(Entity):

    def __init__(self, submodule, width=100, selected=0):
        super(Menu, self).__init__((width, submodule.parent.pipboy.height - 80))
        self.submodule = submodule
        self._items = defaultdict(list)
        self.selected = selected
        self.rect[0] = 4
        self.rect[1] = 60
        self.submodule.parent.pipboy.actions.add_action(pygame.K_UP, self.select_menu_item, ['dial_up'])
        self.submodule.parent.pipboy.actions.add_action(pygame.K_DOWN, self.select_menu_item, ['dial_down'])

    @property
    def items(self):
        return self._items[self.submodule]

    def add_item(self, item):
        self.items.append(item)
        self.redraw()

    def select(self, item):
        self.selected = item
        self.redraw()
        self.items[item].on_select()

    def select_menu_item(self, action):
        if not self.items:
            return
        if action == "dial_up":
            if self.selected > 0:
                self.submodule.parent.pipboy.sounds.play('dial_move')
                self.select(self.selected - 1)
        if action == "dial_down":
            if self.selected < len(self.items) - 1:
                self.submodule.parent.pipboy.sounds.play('dial_move')
                self.select(self.selected + 1)

    def redraw(self):
        self.image.fill((0, 0, 0))
        offset = 5
        for i in range(len(self.items)):
            text = self.submodule.parent.pipboy.fonts[14].render(
                " %s " % self.items[i].title,
                True,
                (105, 255, 187),
                (0, 0, 0)
            )
            if i == self.selected:
                selected_rect = (5, offset - 2, text.get_size()[0] + 6, text.get_size()[1] + 3)
                pygame.draw.rect(self.image, (95, 255, 177), selected_rect, 2)
            self.image.blit(text, (10, offset))
            offset += text.get_size()[1] + 6


class MenuItem():

    def __init__(self, title, callback=None):
        self.title = title
        self.callback = callback

    def on_select(self):
        self.execute()
        if self.callback:
            self.callback(self)

    def execute(self):
        pass


class Scanlines(Entity):

    def __init__(self, width, height, gap, speed, colours, full_push=False):
        super(Scanlines, self).__init__((width, height))
        self.width = width
        self.height = height
        self.move = gap * len(colours)
        self.gap = gap
        self.colours = colours
        self.rect[1] = 0
        self.top = 0.0
        self.speed = speed
        self.full_push = full_push
        colour = 0
        area = pygame.Rect(0, self.rect[1] * self.speed, self.width, self.gap)
        while area.top <= self.height - self.gap:
            self.image.fill(self.colours[colour], area)
            area.move_ip(0, (self.gap))
            colour += 1
            if colour >= len(self.colours):
                colour = 0

    def render(self, interval=0):
        self.top += self.speed * interval
        self.rect[1] = self.top
        self.dirty = 1
        if self.full_push:
            if self.top >= self.height:
                self.top = 0
        else:
            if (self.top * self.speed) >= self.move:
                self.top = 0
        super(Scanlines, self).render(self)


class Border(Entity):
    def __init__(self):
        super(Border, self).__init__()
        self.image = pygame.image.load(
            pkg_resources.resource_filename(
                'pypipboy',
                'data/images/border.png'
            )
        )
        self.rect = self.image.get_rect()
