import pygame
from pypipboy.game.core import EntityGroup
import pypipboy.pypboy.ui
from pypipboy.pypboy.ui import Menu

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass


class BaseModule(EntityGroup):

    MODULES = []

    def __init__(self, boy, configfile=None):
        super(BaseModule, self).__init__()
        self.paused = False
        self.pypboy = boy
        self.submodules = []
        if self.pypboy.configfile.getboolean('GPIO', 'enabled'):
            GPIO.setup(self.GPIO_LED_ID, GPIO.OUT)
            GPIO.output(self.GPIO_LED_ID, False)

        self.active = None
        self.configfile = configfile
        self.position = (0, 40)

        self.footer = pypipboy.pypboy.ui.Footer(self.pypboy)
        self.footer.menu = []
        for mod in self.MODULES:
            self.submodules.append(mod(self, self.configfile))
            self.footer.menu.append(mod.LABEL)
        self.footer.selected = self.footer.menu[0]
        self.footer.position = (0, self.pypboy.display.height - 53)  # 80
        self.add(self.footer)

        self.pypboy.actions.add_action(pygame.K_1, self.switch_submodule, [0])
        self.pypboy.actions.add_action(pygame.K_2, self.switch_submodule, [1])
        self.pypboy.actions.add_action(pygame.K_3, self.switch_submodule, [2])
        self.pypboy.actions.add_action(pygame.K_4, self.switch_submodule, [3])
        self.pypboy.actions.add_action(pygame.K_5, self.switch_submodule, [4])

        self.switch_submodule(0)

        self.action_handlers = {
            "pause": self.handle_pause,
            "resume": self.handle_resume
        }

    def move(self, x, y):
        super(BaseModule, self).move(x, y)
        if self.active:
            self.active.move(x, y)

    def switch_submodule(self, module):
        if self.active:
            self.active.handle_action("pause")
            self.remove(self.active)
        if len(self.submodules) > module:
            self.active = self.submodules[module]
            self.active.parent = self
            self.active.handle_action("resume")
            self.footer.select(self.footer.menu[module])
            self.add(self.active)
        else:
            print("No submodule at {}".format(module))

    def render(self, interval):
        self.active.render(interval)
        super(BaseModule, self).render(interval)

    def handle_action(self, action, value=0):
        if action.startswith("knob_"):
            num = int(action[-1])
            self.switch_submodule(num - 1)
        elif action in self.action_handlers:
            self.action_handlers[action]()
        else:
            if self.active:
                self.active.handle_action(action, value)

    def handle_pause(self):
        self.paused = True
        if self.pypboy.configfile.getboolean('GPIO', 'enabled'):
            GPIO.output(self.GPIO_LED_ID, False)

    def handle_resume(self):
        self.paused = False
        if self.pypboy.configfile.getboolean('GPIO', 'enabled'):
            GPIO.output(self.GPIO_LED_ID, True)
        self.pypboy.sounds.play('module_change')
        self.active.handle_action("resume")


class SubModule(EntityGroup):

    LABEL = None
    headline = None
    title = None

    def __init__(self, parent, configfile=None):
        super(SubModule, self).__init__()
        self.parent = parent
        self.configfile = configfile
        self.paused = False
        self.menu = Menu(self)
        self.add(self.menu)

        self.action_handlers = {
            "pause": self.handle_pause,
            "resume": self.handle_resume
        }

    def handle_action(self, action, value=0):
        if action.startswith("dial_") and self.menu:
            self.menu.handle_action(action)
        elif action in self.action_handlers:
            self.action_handlers[action]()

    def handle_pause(self):
        self.paused = True

    def handle_resume(self):
        self.parent.pypboy.set_title(self.headline, self.title)
        self.paused = False
        self.parent.pypboy.sounds.play('submodule_change')
