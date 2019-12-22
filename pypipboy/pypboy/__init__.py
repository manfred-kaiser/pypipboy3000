import pkg_resources
import pygame
from pypipboy import game
from pypipboy import config
import pypipboy.pypboy.ui
from pypipboy.pypboy.ui import Menu

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass


class BaseModule(game.EntityGroup):

    submodules = []

    def __init__(self, boy, *args, **kwargs):
        super(BaseModule, self).__init__()

        if config.GPIO_AVAILABLE:
            GPIO.setup(self.GPIO_LED_ID, GPIO.OUT)
            GPIO.output(self.GPIO_LED_ID, False)

        self.active = None
        self.pypboy = boy
        self.position = (0, 40)

        self.footer = pypipboy.pypboy.ui.Footer()
        self.footer.menu = []
        for mod in self.submodules:
            self.footer.menu.append(mod.label)
        self.footer.selected = self.footer.menu[0]
        self.footer.position = (0, config.HEIGHT - 53)  # 80
        self.add(self.footer)

        self.switch_submodule(0)

        self.action_handlers = {
            "pause": self.handle_pause,
            "resume": self.handle_resume
        }
        if config.SOUND_ENABLED:
            self.module_change_sfx = pygame.mixer.Sound(pkg_resources.resource_filename('pypipboy', 'data/sounds/module_change.ogg'))

    def move(self, x, y):
        super(BaseModule, self).move(x, y)
        if hasattr(self, 'active'):
            self.active.move(x, y)

    def switch_submodule(self, module):
        if hasattr(self, 'active') and self.active:
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
            if hasattr(self, 'active') and self.active:
                self.active.handle_action(action, value)

    def handle_event(self, event):
        if hasattr(self, 'active') and self.active:
            self.active.handle_event(event)

    def handle_pause(self):
        self.paused = True
        if config.GPIO_AVAILABLE:
            GPIO.output(self.GPIO_LED_ID, False)

    def handle_resume(self):
        self.paused = False
        if config.GPIO_AVAILABLE:
            GPIO.output(self.GPIO_LED_ID, True)
        if config.SOUND_ENABLED:
            self.module_change_sfx.play()
        self.active.handle_action("resume")


class SubModule(game.EntityGroup):

    label = None
    headline = None
    title = None

    def __init__(self, parent, *args, **kwargs):
        super(SubModule, self).__init__()
        self.parent = parent
        self.menu = Menu(self)
        self.add(self.menu)

        self.action_handlers = {
            "pause": self.handle_pause,
            "resume": self.handle_resume
        }

        if config.SOUND_ENABLED:
            self.submodule_change_sfx = pygame.mixer.Sound(pkg_resources.resource_filename('pypipboy', 'data/sounds/submodule_change.ogg'))

    def handle_action(self, action, value=0):
        if action.startswith("dial_") and self.menu:
            self.menu.handle_action(action)
        elif action in self.action_handlers:
            self.action_handlers[action]()

    def handle_event(self, event):
        pass

    def handle_pause(self):
        self.paused = True

    def handle_resume(self):
        self.parent.pypboy.set_title(self.headline, self.title)
        self.paused = False
        if config.SOUND_ENABLED:
            self.submodule_change_sfx.play()
