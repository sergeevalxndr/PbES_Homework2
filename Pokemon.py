import Actions
import random
import Effects
import copy
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
    _level = 1
    _health = _max_health = 50
    attack = bonus_attack = 0.0
    defence = bonus_defence = 0.0
    poketype = PokemonType.NORMAL
    speed = _bonus_speed = 0
    atb_position = 0
    _wins = 0
    _losses = 0

    actions = []
    effects = []

    def _gain_exp(self, poke):
        step = int(poke.get_level()) / int(self._level) / 5
        new_level = round(self._level + step, 2)
        if int(self._level) < int(new_level):
            self._level_up(int(new_level))
            print("%s получает новый уровень!" % self.get_name())
        self._level = new_level

    def atb_init(self):
        self.atb_position += random.randint(0, 10)

    def atb_step(self):
        for a in self.effects:
            a.duration -= self.speed
            if a.duration <= 0:
                if type(a) is Effects.CombatEffect:
                    self.bonus_attack = round(self.bonus_attack - a.attack, 2)
                    self.bonus_defence = round(self.bonus_defence - a.defence, 2)
                    self._bonus_speed = round(self._bonus_speed - a.speed, 2)
                self.effects.remove(a)
        self.atb_position += self.speed + self._bonus_speed

    def refresh(self):
        self._health = self._max_health
        self.atb_position = 0
        self.effects.clear()
        self.bonus_attack = 0
        self.bonus_defence = 0
        self._bonus_speed = 0

    def _level_up(self, level):
        pass

    def win(self, poke=None):
        self._gain_exp(poke)
        self._wins += 1
        if poke:
            poke.loss()

    def loss(self, poke=None):
        self._losses += 1
        if poke:
            poke.win()

    def get_atb_position(self):
        return self.atb_position

    def get_hp(self):
        return self._health

    def get_name(self):
        return self.__pokename__

    def get_level(self):
        return self._level

    def _change_hp(self, step):
        self._health += step

    def introduce_yourself(self):
        print("Имя: %s" % self.__pokename__)
        print("Уровень: %s" % self._level)
        print("Тип: %s" % self.poketype)
        print("Атака: %s" % self.attack)
        print("Защита: %s" % self.defence)
        print("Здоровье: %s" % self._max_health)
        print("Скорость: %s" % self.speed)
        print("Действия: %s" % self.actions)
        print("Побед: %s \nПоражений: %s\n" % (self._wins, self._losses))

    def add_effect(self, effect):
        if type(effect) is Effects.Stun:
            self.atb_position -= effect.amount
            if self.atb_position < 0:
                self.atb_position = 0
        else:
            # Проверка существующего эффекта, обновление при существовании
            f = [a for a in self.effects if a.name == effect.name]
            if f:
                index = self.effects.index(f[0])
                self.effects[index].duration += effect.duration
            else:
                self.effects.append(copy.copy(effect))
                if type(effect) == Effects.CombatEffect:
                    self.bonus_attack = round(self.bonus_attack + effect.attack, 2)
                    self.bonus_defence = round(self.bonus_defence + effect.defence, 2)
                    self._bonus_speed = round(self._bonus_speed + effect.speed, 2)

    def effect_processing(self):
        for a in self.effects:
            if type(a) == Effects.Healing:
                new_health = self._health + a.amount
                if new_health > self._max_health:
                    print("%s исцеляет себе %s здоровья (%s->%s)"
                          % (self.get_name(), a.amount, self._health, self._max_health))
                    self._health = self._max_health
                else:
                    print("%s исцеляет себе %s здоровья (%s->%s)"
                          % (self.get_name(), a.amount, self._health, new_health))
                    self._health = new_health

            if type(a) == Effects.Poisoning:
                new_health = self._health - a.amount
                if new_health < 0:
                    print("%s умирает от отравления (%s->%s)"
                          % (self.get_name(), self._health, self._health - a.amount))
                    return "DEATH"
                else:
                    print("%s теряет %s здоровья от отравления (%s->%s)"
                          % (self.get_name(), -a.amount, self._health, new_health))
                    self._health = new_health

    def action(self, poke):
        action = None
        priority = 5
        while not action:
            # TODO Изменить приоритеты, добавить заряд
            priority -= 1
            eligible_actions = list(filter(lambda a: a.priority == priority, self.actions))
            if eligible_actions != []:
                action = eligible_actions[random.randrange(0, len(eligible_actions))]

        if type(action) is Actions.Attack:
            if random.randint(0, 100)/100 < action.accuracy:
                damage = int(action.power
                             * (dmg_matrix[self.poketype][poke.poketype] + self.attack + self.bonus_attack)
                             * (1 - poke.defence - poke.bonus_defence))
                for a in action.effects:
                    poke.add_effect(a)
                print("%s наносит %s урона %s способностью %s (%s->%s)"
                      % (self.get_name(), str(damage), poke.get_name(),
                         action.name, str(poke.get_hp()), str(poke.get_hp() - damage)))
                poke._change_hp(-damage)

                if poke.get_hp() <= 0:
                    print("%s убивает %s!" % (self.get_name(), poke.get_name()))
                    self.win(poke)
                    return "KILL"
            else:
                print("%s попытался использовать способность %s и промахнулся!" % (self.get_name(), action.name))
        elif type(action) is Actions.Defence:
            self.add_effect(Effects.CombatEffect(action.name, 100, defence=action.defence))
            for a in action.effects:
                self.add_effect(a)
            print("%s использует защитную способность %s" % (self.get_name(), action.name))
        else:
            print(self.get_name() + " ожидает")


class Eevee(Pokemon):
    def __init__(self):
        self.__pokename__ = "Eevee_" + str(random.randint(1, 100000))
        self._max_health = 50
        self.attack = 0.15
        self.defence = 0.0
        self.speed = 30
        self.actions = list([Actions.Attack("Tail Slash", 1, 10, 0.8),
                             Actions.Attack("Mighty Bite", 1, 18, 0.6),
                             Actions.Defence("Tail Propeller", 1, 0.1, effects=[
                                 Effects.CombatEffect("Damage Boost", 120, attack=0.3)
                             ]),
                             Actions.Defence("Tail Dome", 1, 0.2, effects=[
                                 Effects.Healing("Healing", 150, 3)
                             ]),
                             Actions.Waiting()])
        self.effects = list()

    def _level_up(self, level):
        if 2 == level:
            self._max_health = 65
            self.attack = 0.30
            self.speed = 35
            self.defence = 0.05
            self.actions.append(Actions.Attack("Ear Flop", 1, 10, 0.8, effects=[
                Effects.Stun("Ear Flop", 70)
            ]))
        if 3 == level:
            self._max_health = 80
            self.attack = 0.45
            self.speed = 40
            self.defence = 0.10
            self.actions.append(Actions.Attack("Tail Spin", 1, 18, 0.8, effects=[
                Effects.Poisoning("Tail Spin", 120, 4)
            ]))


class Krabby(Pokemon):
    def __init__(self):
        self.__pokename__ = "Krabby_" + str(random.randint(1, 100000))
        self._max_health = 75
        self.attack = 0.15
        self._defence = 0.10
        self.speed = 17
        self.poketype = PokemonType.WATER
        self.actions = list([Actions.Attack("Claw Bite", 1, 12, 0.8),
                             Actions.Attack("Claw Smash", 1, 17, 0.6, effects=[
                                 Effects.Stun("Claw Smash", 100)
                             ]),
                             Actions.Defence("Crab Defence", 1, 0.2),
                             Actions.Defence("Super Crab Defence", 1, 0.4),
                             Actions.Waiting()])
        self.effects = list()

    def _level_up(self, level):
        if 2 == level:
            self._max_health = 100
            self.attack = 0.20
            self._defence = 0.15
            self.speed = 21
            self.actions.append(Actions.Attack("Claw Slash", 1, 14, 0.7, effects=[
                Effects.Poisoning("Отравление", 150, 6)
            ]))
        if 3 == level:
            self._max_health = 130
            self.attack = 0.30
            self._defence = 0.20
            self.speed = 25
            self.actions.append(Actions.Attack("Mighty Smash", 1, 28, 0.8))


class Electrode(Pokemon):
    def __init__(self):
        self.__pokename__ = "Electrode_" + str(random.randint(1, 100000))
        self._max_health = 50
        self.attack = 0.20
        self.defence = 0.10
        self.speed = 23
        self.poketype = PokemonType.ELECTRIC
        self.actions = list([Actions.Attack("Electrospit", 1, 14, 0.7),
                             Actions.Attack("Electroblow", 1, 22, 0.6),
                             Actions.Defence("Electroshield", 1, 0.1),
                             Actions.Defence("Electrobulb", 1, 0.3),
                             Actions.Waiting()])
        self.effects = list()

    def _level_up(self, level):
        if 2 == level:
            self._max_health = 65
            self.attack = 0.30
            self.defence = 0.15
            self.speed = 27
            self.actions.append(Actions.Attack("Electrostun", 1, 14, 0.8, effects=[
                Effects.CombatEffect("Electrostun", 200, speed=-10)
            ]))
        if 3 == level:
            self._max_health = 80
            self.attack = 0.40
            self.defence = 0.20
            self.speed = 30
            self.actions.append(Actions.Attack("Electrodrain", 1, 12, 0.8, effects=[
                Effects.Poisoning("Electrodrain", 200, 7)
            ]))


class PokeBall(object):
    selection = [Eevee, Krabby, Electrode]

    @classmethod
    def pull_out_pokemon(cls):
        return cls.selection[random.randrange(0, len(cls.selection))]()

    @staticmethod
    def pick_pokemon(poketype):
        return poketype()
