from pypipboy import pypboy

from pypipboy.pypboy.ui import MenuItem


class Module(pypboy.SubModule):

    label = "S.P.E.C.I.A.L."
    headline = "STATUS"
    title = " HP 160/175  |  AP 62/62"

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        self.menu.add_item(MenuItem("CND"))
