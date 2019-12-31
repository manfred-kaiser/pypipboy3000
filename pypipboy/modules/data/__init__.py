from pypipboy.pypboy import BaseModule
from pypipboy.modules.data import quests
from pypipboy.modules.data import misc
from pypipboy.modules.radio import RadioModule

from pypipboy.modules.map import WorldMapModule, LocalMapModule


class Module(BaseModule):

    LABEL = "DATA"
    GPIO_LED_ID = 28  # GPIO 23 #23
    MODULES = [
        LocalMapModule,
        WorldMapModule,
        quests.Module,
        misc.Module,
        RadioModule
    ]
