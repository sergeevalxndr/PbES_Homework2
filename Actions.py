class Action(object):
    priority = 0
    charge = 0
    type = None
    effects = []
    name = "Default name"

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.name!r})')


class Attack(Action):
    def __init__(self, name, priority, power, accuracy, effects=[], charge=0):
        self.name = name
        self.power = power
        self.accuracy = accuracy
        self.priority = priority
        self.effects = list(effects)
        self.charge = charge


class Defence(Action):
    def __init__(self, name, priority, defence, effects=[], charge=0):
        self.name = name
        self.defence = defence
        self.priority = priority
        self.effects = list(effects)
        self.charge = charge


class Waiting(Action):
    def __init__(self):
        self.name = "Ожидание"
