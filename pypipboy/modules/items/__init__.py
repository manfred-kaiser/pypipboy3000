from pypipboy.pypboy import BaseModule
from pypipboy.modules.items import weapons
from pypipboy.modules.items import apparel
from pypipboy.modules.items import aid
from pypipboy.modules.items import misc
from pypipboy.modules.items import ammo


class Module(BaseModule):

    LABEL = "ITEMS"
    GPIO_LED_ID = 29  # GPIO27 #21

    MODULES = [
        weapons.Module,
        apparel.Module,
        aid.Module,
        misc.Module,
        ammo.Module
    ]
