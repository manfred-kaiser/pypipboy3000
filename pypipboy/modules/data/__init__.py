from pypipboy.pypboy import BaseModule
from pypipboy.modules.data import local_map
from pypipboy.modules.data import world_map
from pypipboy.modules.data import quests
from pypipboy.modules.data import misc
from pypipboy.modules.data import radio


class Module(BaseModule):

    LABEL = "DATA"
    GPIO_LED_ID = 28  # GPIO 23 #23
    MODULES = [
        local_map.Module,
        world_map.Module,
        quests.Module,
        misc.Module,
        radio.Module
    ]
