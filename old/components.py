import numpy as np


class Component:
    def __init__(self, icon, name="", parent = None, children = list()):
        self.name = name
        self.icon = icon
        self.values = dict()
        self.parent = parent
        self.children = children

    def walk(self):
        yield self
        for child in self.children:
            for n in walk(child):
                yield n

class R(Component):
    def __init__(self, R=np.nan, **kwargs):
        Component.__init__(self, **kwargs)
        self.values["R"] = R
        self.transfer_func = lambda omega: self.values["R"]


class C(Component):
    def __init__(self, C=np.nan, **kwargs):
        Component.__init__(self, **kwargs)
        self.values["C"] = C
        self.transfer_func = lambda omega: 1. / (1j * self.values["C"] * omega)


class Q(Component):
    def __init__(self, Q=np.nan, n=np.nan, **kwargs):
        Component.__init__(self, **kwargs)
        self.values["Q"] = Q
        self.values["n"] = n
        self.transfer_func = lambda omega: 1. / (1j * self.values["Q"] * omega ** self.values["n"])

def get_component_list(icon_dir="resources/components_icons"):
    component_list = list()
    component_list.append(R(icon=icon_dir + "/R.png", name="Resistance"))
    component_list.append(C(icon=icon_dir + "/C.png", name="Capacitance"))
    component_list.append(Q(icon=icon_dir + "/Q.png", name="Constant phase element"))
    return component_list
