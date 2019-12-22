from pypipboy import pypboy


class Module(pypboy.SubModule):

    label = " Weapons "
    headline = "ITEMS"
    title = " HP 160/175  |  AP 62/62"

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
