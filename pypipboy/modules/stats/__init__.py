from pypipboy.pypboy import BaseModule
from pypipboy.modules.stats import status
from pypipboy.modules.stats import special
from pypipboy.modules.stats import skills
from pypipboy.modules.stats import perks
from pypipboy.modules.stats import general


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
