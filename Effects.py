class Effect(object):
    duration = 0
    type = None
    name = "Default name"


class CombatEffect(Effect):
    def __init__(self, name, duration, attack=0, defence=0, speed=0):
        self.name = name
        self.duration = duration
        self.attack = attack
        self.defence = defence
        self.speed = speed


class Healing(Effect):
    def __init__(self, name, duration, amount):
        self.name = name
        self.duration = duration
        self.amount = amount


class Poisoning(Effect):
    def __init__(self, name, duration, amount):
        self.name = name
        self.duration = duration
        self.amount = amount


class Stun(Effect):
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
