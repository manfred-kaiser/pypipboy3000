import pygame
from pypipboy.game.core import EntityGroup
from pypipboy.pypboy.ui import Menu, FooterMenu

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass


class BaseModule(EntityGroup):

    MODULES = []

    def __init__(self, pipboy):
        super(BaseModule, self).__init__()
        self.paused = False
        self.pipboy = pipboy
        if self.pipboy.configfile.getboolean('GPIO', 'enabled'):
            GPIO.setup(self.GPIO_LED_ID, GPIO.OUT)
            GPIO.output(self.GPIO_LED_ID, False)

        self.active = None
        self.submodules = [module(self) for module in self.MODULES]
        self.position = (0, 40)

        self.footer = FooterMenu(self)
        self.add(self.footer)

        self.pipboy.actions.add_action(pygame.K_1, self.switch_submodule, [0])
        self.pipboy.actions.add_action(pygame.K_2, self.switch_submodule, [1])
        self.pipboy.actions.add_action(pygame.K_3, self.switch_submodule, [2])
        self.pipboy.actions.add_action(pygame.K_4, self.switch_submodule, [3])
        self.pipboy.actions.add_action(pygame.K_5, self.switch_submodule, [4])

        self.switch_submodule(0)

    def move(self, x, y):
        super(BaseModule, self).move(x, y)
        if self.active:
            self.active.move(x, y)

    def switch_submodule(self, module):
        if self.active:
            self.active.handle_pause()
            self.remove(self.active)
        if len(self.submodules) > module:
            self.active = self.submodules[module]
            self.active.parent = self
            self.active.handle_resume()
            self.footer.select(self.footer.menu[module])
            self.add(self.active)
        else:
            print("No submodule at {}".format(module))

    def render(self, interval):
        super(BaseModule, self).render(interval)
        self.active.render(interval)

    def handle_pause(self):
        self.paused = True
        if self.pipboy.configfile.getboolean('GPIO', 'enabled'):
            GPIO.output(self.GPIO_LED_ID, False)

    def handle_resume(self):
        self.paused = False
        if self.pipboy.configfile.getboolean('GPIO', 'enabled'):
            GPIO.output(self.GPIO_LED_ID, True)
        self.pipboy.sounds.play('module_change')
        self.active.handle_resume()


class SubModule(EntityGroup):

    LABEL = None
    headline = None
    title = None

    def __init__(self, parent):
        super(SubModule, self).__init__()
        self.pipboy = parent.pipboy
        self.parent = parent
        self.paused = False
        self.menu = Menu(self.pipboy, self)
        self.add(self.menu)

    def handle_pause(self):
        self.paused = True

    def handle_resume(self):
        self.parent.pipboy.set_title(self.headline, self.title)
        self.paused = False
        self.parent.pipboy.sounds.play('submodule_change')
