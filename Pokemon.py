import Actions
import random
import Effects
from math import floor


class PokemonType(object):
    NORMAL = 0
    EARTH = 1
    WATER = 2
    ELECTRIC = 3
    FIRE = 4
    FLYING = 5


dmg_matrix = [[1, 1, 1, 1, 1, 1],
              [1, 0.8, 1.2, 1, 0.8, 0.8],
              [1, 0.8, 0.8, 1.2, 1.4, 1],
              [1, 0.8, 1.2, 0.8, 1, 1.2],
              [1, 1.2, 0.8, 1, 0.8, 1],
              [1, 1.2, 1, 0.8, 1, 1]]


class Pokemon(object):
    __pokename__ = "Default Name"
    __level__ = 1
    __health__ = max_health = 50
    attack = bonus_attack = 0.0
    defence = bonus_defence = 0.0
    type = PokemonType.NORMAL
    speed = bonus_speed = 0
    atb_position = 0

    actions = []
    effects = []

    def gain_exp(self, poke):
        step = int(poke.get_level()) / int(self.__level__) / 5
        new_level = round(self.__level__ + step, 2)
        if int(self.__level__) < int(new_level):
            self.level_up(int(new_level))
            print("%s получает новый уровень!" % self.get_name())
        self.__level__ = new_level

    def atb_step(self):
        for a in self.effects:
            a.duration -= self.speed
            if a.duration < 0:
                if type(a) is Effects.CombatEffect:
                    self.bonus_attack = round(self.bonus_attack - a.attack, 2)
                    self.bonus_defence = round(self.bonus_defence - a.defence, 2)
                    self.bonus_speed = round(self.bonus_speed - a.speed, 2)
                self.effects.remove(a)
        self.atb_position += self.speed + self.bonus_speed

    def refresh(self):
        self.__health__ = self.max_health
        self.atb_position = 0
        self.effects.clear()
        self.bonus_attack = 0
        self.bonus_defence = 0
        self.bonus_speed = 0

    def level_up(self, level):
        pass

    def get_hp(self):
        return self.__health__

    def get_name(self):
        return self.__pokename__  # + "(lvl_%s)" % floor(self.__level__)

    def get_level(self):
        return self.__level__

    def change_hp(self, step):
        self.__health__ += step

    def introduce_yourself(self):
        print("Имя: " + self.__pokename__)
        print("Уровень: " + str(self.__level__))
        print("Тип: " + str(self.type))
        print("Атака: " + str(self.attack))
        print("Защита: " + str(self.defence))
        print("Здоровье: " + str(self.max_health))
        print("Скорость: " + str(self.speed))
        print("Действия: " + str(self.actions))

    def add_effect(self, effect):
        if type(effect) is Effects.Stun:
            self.atb_position -= effect.amount
            if self.atb_position < 0:
                self.atb_position = 0
        else:
            # Проверка существующего эффекта, обновление при существовании
            f = [a for a in self.effects if a.name == effect.name]   # TODO Переписать
            if f:
                index = self.effects.index(f[0])
                self.effects[index].duration += effect.duration
            else:
                self.effects.append(effect)
                if type(effect) == Effects.CombatEffect:
                    self.bonus_attack = round(self.bonus_attack + effect.attack, 2)
                    self.bonus_defence = round(self.bonus_defence + effect.defence, 2)
                    self.bonus_speed = round(self.bonus_speed + effect.speed, 2)

    def effect_processing(self):
        for a in self.effects:
            if type(a) == Effects.Healing:
                new_health = self.__health__ + a.amount
                if new_health > self.max_health:
                    print("%s исцеляет себе %s здоровья (%s->%s)"
                          % (self.get_name(), str(a.amount), self.__health__, self.max_health))
                    self.__health__ = self.max_health
                else:
                    print("%s исцеляет себе %s здоровья (%s->%s)"
                          % (self.get_name(), str(a.amount), self.__health__, new_health))
                    self.__health__ = new_health

            if type(a) == Effects.Poisoning:
                new_health = self.__health__ - a.amount
                if new_health < 0:
                    print("%s умирает от отравления (%s->%s)"
                          % (self.get_name(), self.__health__, self.__health__ - a.amount))
                    return "DEATH"
                else:
                    print("%s теряет %s здоровья от отравления (%s->%s)"
                          % (self.get_name(), -a.amount, self.__health__, new_health))
                    self.__health__ = new_health

    def action(self, poke):
        action = None
        priority = 5  # 5 - максимальный уровень приоритета
        while not action:
            # TODO Изменить приоритеты, добавить заряд
            priority -= 1
            eligible_actions = list(filter(lambda a: a.priority == priority, self.actions))
            if eligible_actions != []:
                action = eligible_actions[random.randrange(0, len(eligible_actions))]

        if type(action) is Actions.Attack:
            if random.randint(0, 100)/100 < action.accuracy:
                damage = int(action.power
                             * (dmg_matrix[self.type][poke.type] + self.attack + self.bonus_attack)
                             * (1 - poke.defence - poke.bonus_defence))
                for a in action.effects:
                    poke.add_effect(a)
                print("%s наносит %s урона %s способностью %s (%s->%s)"
                      % (self.get_name(), str(damage), poke.get_name(),
                         action.name, str(poke.get_hp()), str(poke.get_hp() - damage)))
                poke.change_hp(-damage)

                if poke.get_hp() <= 0:
                    print("%s убивает %s!" % (self.get_name(), poke.get_name()))
                    self.gain_exp(poke)
                    return "KILL"
            else:
                print("%s попытался использовать способность %s и промахнулся!" % (self.get_name(), action.name))
        elif type(action) is Actions.Defence:
            # TODO Добавить эффекты от защитных способностей
            self.add_effect(Effects.CombatEffect(action.name, 100, defence=action.defence))
            for a in action.effects:
                self.add_effect(a)
            print("%s использует защитную способность %s" % (self.get_name(), action.name))
        else:
            print(self.get_name() + " ожидает")


class Eevee(Pokemon):
    def __init__(self):
        self.__pokename__ = "Eevee_" + str(random.randint(1, 100000))
        self.max_health = self.__health__ = 55
        self.attack = 0.10
        self.speed = 30
        self.actions = list([Actions.Attack("Tail Slash", 1, 10, 0.8),
                             Actions.Attack("Mighty Bite", 1, 18, 0.6),
                             Actions.Defence("Tail Propeller", 1, 0.1, effects=[
                                 Effects.CombatEffect("Damage Boost", 250, attack=0.3)
                             ]),
                             Actions.Defence("Tail Dome", 1, 0.2, effects=[
                                 Effects.Healing("Healing", 150, 10)
                             ]),
                             Actions.Waiting()])
        self.effects = list()

    def level_up(self, level):
        if 2 == level:
            self.max_health = 75
            self.attack = 0.20
            self.speed = 35
            self.defence = 0.10
            self.actions.append(Actions.Attack("Ear Flop", 1, 10, 0.8, effects=[
                Effects.Stun("Ear Flop", 70)
            ]))


class Krabby(Pokemon):
    def __init__(self):
        self.__pokename__ = "Krabby_" + str(random.randint(1, 100000))
        self.max_health = self.__health__ = 75
        self.attack = 0.20
        self.defence = 0.10
        self.speed = 20
        self.type = PokemonType.WATER
        self.actions = list([Actions.Attack("Claw Bite", 1, 12, 0.8),
                             Actions.Attack("Claw Smash", 1, 17, 0.5, effects=[
                                 Effects.Stun("Claw Smash", 100)
                             ]),
                             Actions.Defence("Crab Defence", 1, 0.2),
                             Actions.Defence("Super Crab Defence", 1, 0.4),
                             Actions.Waiting()])
        self.effects = list()

    def level_up(self, level):
        if 2 == level:
            self.max_health = 100
            self.attack = 0.30
            self.defence = 0.20
            self.speed = 25
            self.actions.append(Actions.Attack("Claw Slash", 1, 14, 0.8, effects=[
                Effects.Poisoning("Отравление", 150, 6)
            ]))


class Electrode(Pokemon):
    def __init__(self):
        self.__pokename__ = "Electrode_" + str(random.randint(1, 100000))
        self.max_health = self.__health__ = 40
        self.attack = 0.30
        self.defence = 0.10
        self.speed = 25
        self.type = PokemonType.ELECTRIC
        self.actions = list([Actions.Attack("Electrospit", 1, 14, 0.7),
                             Actions.Attack("Electroblow", 1, 22, 0.6),
                             Actions.Defence("Electroshield", 1, 0.1),
                             Actions.Defence("Electrobulb", 1, 0.3),
                             Actions.Waiting()])
        self.effects = list()

    def level_up(self, level):
        if 2 == level:
            self.max_health = 70
            self.attack = 0.40
            self.defence = 0.15
            self.speed = 30
            self.actions.append(Actions.Attack("Electroshock", 1, 14, 0.8, effects=[
                Effects.CombatEffect("Electrostun", 200, speed=-10)
            ]))


class Pokeball(object):
    @classmethod
    def pull_out_pokemon(cls):
        return selection[random.randrange(0, len(selection))]()

    @staticmethod
    def pick_pokemon(poketype):
        return poketype()


selection = [Eevee, Krabby, Electrode]
