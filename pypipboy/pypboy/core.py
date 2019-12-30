import logging
import os
from configparser import ConfigParser
import pkg_resources
import pygame

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass

from pypipboy import config
from pypipboy.config import FontManager, SoundManager, ActionManager
from pypipboy.game.core import Engine

from pypipboy.pypboy.ui import Header, Border, Scanlines


class PypboyDisplay():

    def __init__(self, pipboy):
        self.pipboy = pipboy
        self.width = self.pipboy.configfile.getint('Display', 'width')
        self.height = self.pipboy.configfile.getint('Display', 'height')


class Pypboy(Engine):

    def __init__(self, pipboy_name, configfile=None):
        self.configfile = ConfigParser(allow_no_value=True)
        self.configfile.read(pkg_resources.resource_filename('pypipboy', 'data/default.ini'))
        if configfile:
            if os.path.isfile(configfile):
                self.configfile.read(configfile)
            else:
                logging.error("configfile '%s' not found!", configfile)

        self.fonts = FontManager(self)
        self.sounds = SoundManager(self)
        self.actions = ActionManager(self)
        self.actions.add_action(pygame.K_F1, self.switch_module, ['stats'])
        self.actions.add_action(pygame.K_F2, self.switch_module, ['items'])
        self.actions.add_action(pygame.K_F3, self.switch_module, ['data'])

        self.events = {}
        self.display = PypboyDisplay(self)
        self.running = False

        super(Pypboy, self).__init__(
            pipboy_name,
            self.display.width,
            self.display.height
        )

        self.active = None
        self.header = Header(self)
        self.border = Border()
        self.scanlines = [
            Scanlines(800, 480, 3, 1, [(0, 13, 3, 50), (6, 42, 22, 100), (0, 13, 3, 50)]),
            Scanlines(800, 480, 8, 40, [(0, 10, 1, 0), (21, 62, 42, 90), (61, 122, 82, 100), (21, 62, 42, 90)] + [(0, 10, 1, 0) for x in range(50)], True)
        ]
        self.background = pygame.image.load(pkg_resources.resource_filename('pypipboy', 'data/images/overlay.png'))

        self.modules = {}
        self.gpio_actions = {}

    def add_module(self, module_name, module_cls):
        self.modules[module_name] = module_cls(self)

    def register_event(self, event, callback):
        self.events[event] = callback

    def _init_modules(self):
        self.root_children.add(self.header)
        self.root_children.add(Border())
        for scanline in self.scanlines:
            self.root_children.add(scanline)

        for module in self.modules.values():
            module.move(4, 40)

    def _init_gpio_controls(self):
        if not self.configfile.getboolean('GPIO', 'enabled'):
            return
        for pin, action in config.GPIO_ACTIONS.items():
            print("Intialising pin {} as action '{}'".format(pin, action))
            GPIO.setup(pin, GPIO.IN)
            self.gpio_actions[pin] = action

    def check_gpio_input(self):
        for pin, action in self.gpio_actions.items():
            if not GPIO.input(pin):
                pass
                # TODO: fix gpio actions
                # self.handle_action(action)

    def set_title(self, headline, title):
        self.header.headline = headline
        self.header.title = title

    def update(self):
        if self.active:
            self.active.update()
        super(Pypboy, self).update()

    def render(self):
        interval = super(Pypboy, self).render()
        if self.active:
            self.active.render(interval)

    def switch_module(self, module):
        if module in self.modules:
            if self.active:
                self.active.handle_pause()
                self.remove(self.active)
            self.active = self.modules[module]
            self.active.parent = self
            self.active.handle_resume()
            self.add(self.active)
            self.active.switch_submodule(0)
        else:
            print("Module '{}' not implemented.".format(module))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            else:
                self.actions.handle_action(event)
        elif event.type == pygame.QUIT:
            self.running = False
        elif event.type in self.events:
            self.events[event.type](event)

    def run(self, start_module):
        self._init_modules()
        self._init_gpio_controls()
        self.switch_module(start_module)
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.update()
            self.render()
            self.check_gpio_input()
            pygame.time.wait(10)

        try:
            pygame.mixer.quit()
        except Exception:
            pass
