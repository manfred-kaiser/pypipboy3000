from pypipboy.pypboy import BaseModule
from pypipboy.pypboy.modules.data import local_map
from pypipboy.pypboy.modules.data import world_map
from pypipboy.pypboy.modules.data import quests
from pypipboy.pypboy.modules.data import misc
from pypipboy.pypboy.modules.data import radio


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
