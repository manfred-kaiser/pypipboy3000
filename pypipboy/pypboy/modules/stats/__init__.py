from pypipboy.pypboy import BaseModule
from pypipboy.pypboy.modules.stats import status
from pypipboy.pypboy.modules.stats import special
from pypipboy.pypboy.modules.stats import skills
from pypipboy.pypboy.modules.stats import perks
from pypipboy.pypboy.modules.stats import general


class Module(BaseModule):

    LABEL = "STATS"
    GPIO_LED_ID = 30  # GPIO 22 #19

    MODULES = [
        status.Module,
        special.Module,
        skills.Module,
        perks.Module,
        general.Module
    ]
