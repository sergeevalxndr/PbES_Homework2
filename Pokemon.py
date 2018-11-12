import Actions
import random
import Effects

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
    name = "Default Name"
    max_health = __health__ = 50
    attack = 0.0
    defence = 0.0
    type = PokemonType.NORMAL
    speed = 10
    atb_position = 0
    level = 1

    actions = []
    effects = []

    def gain_exp(self, poke):
        step = int(poke.level)/int(self.level)/5
        new_level = round(self.level + step, 2)
        if int(self.level) < int(new_level):
            self.level_up(int(new_level))
        self.level = new_level

    def atb_step(self):
        self.atb_position += self.speed
        for a in self.effects:
            a.duration -= self.speed
            if a.duration < 0:
                self.effects.remove(a)

    def refresh(self):
        self.__health__ = self.max_health
        self.effects.clear()
        self.atb_position = 0

    def level_up(self, level):
        pass

    def get_hp(self):
        return self.__health__

    def change_hp(self, step):
        self.__health__ += step

    def introduce_yourself(self):
        print("Имя: " + self.name)
        print("Уровень: " + str(self.level))
        print("Тип: " + str(self.type))
        print("Атака: " + str(self.attack))
        print("Защита: " + str(self.defence))
        print("Здоровье: " + str(self.max_health))
        print("Скорость: " + str(self.speed))
        print("Действия: " + str(self.actions))  # TODO вывод действий

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

    def effect_processing(self):
        for a in self.effects:
            if a == Effects.Healing:
                new_health = self.__health__ + a.amount()
                if new_health > self.max_health:
                    self.__health__ = self.max_health
                else:
                    self.__health__ = new_health
            elif True:
                pass

    def action(self, poke):
        action = None
        priority = 5  # 5 - максимальный уровень приоритета
        while not action:
            priority -= 1
            eligible_actions = list(filter(lambda a: a.priority == priority, self.actions))  # TODO Изменить приоритеты, добавить заряд
            if eligible_actions != []:
                action = eligible_actions[random.randrange(0, len(eligible_actions))]

        if type(action) is Actions.Attack:
            if random.randint(0, 100)/100 < action.accuracy:
                damage = int(action.power
                             * (dmg_matrix[self.type][poke.type] + self.attack)
                             * (1 - poke.defence))
                for a in action.effects:
                    poke.add_effect(a)
                print("%s наносит %s урона %s способностью %s (%s->%s)"
                      % (self.name, str(damage), poke.name, action.name, str(poke.get_hp()), str(poke.get_hp() - damage)))
                poke.change_hp(-damage)

                if poke.get_hp() <= 0:
                    print("%s убивает %s!" % (self.name, poke.name))
                    self.gain_exp(poke)
                    return "KILL"
            else:
                print("%s попытался использовать способность %s и промахнулся!" % (self.name, action.name))
        elif type(action) is Actions.Defence:
            self.add_effect(Effects.CombatEffect(action.name, 100, defence=action.defence))
            print("%s использует защитную способность %s" % (self.name, action.name))
        else:
            print(self.name + " ожидает")


class Eevee(Pokemon):
    def __init__(self):
        self.name = "Eevee_" + str(random.randint(1, 100000))
        self.max_health = self.health = 55
        self.attack = 0.10
        self.speed = 30
        self.actions = list()
        self.effects = list()
        self.actions.extend([Actions.Attack("Tail Slash", 1, 10, 0.8),
                             Actions.Attack("Mighty Bite", 1, 20, 0.6),
                             Actions.Defence("Tail Propeller", 1, 0.1),
                             Actions.Defence("Tail Dome", 1, 0.2),
                             Actions.Waiting()])

    def level_up(self, level):
        if 2 == level:
            self.max_health = 75
            self.attack = 0.20
            self.speed = 35
            self.defence = 0.10
            self.actions.append(Actions.Attack("Ear Flop", 1, 10, 0.8, effects=[
                Effects.Stun("Ear Flop", 50)
            ]))


class Krabby(Pokemon):
    def __init__(self):
        self.name = "Krabby_" + str(random.randint(1, 100000))
        self.max_health = self.health = 75
        self.attack = 0.20
        self.defence = 0.10
        self.speed = 20
        self.type = PokemonType.WATER
        self.actions = list()
        self.effects = list()
        self.actions.extend([Actions.Attack("Claw Bite", 1, 12, 0.8),
                             Actions.Attack("Claw Smash", 1, 17, 0.7),
                             Actions.Defence("Crab Defence", 1, 0.2),
                             Actions.Defence("Super Crab Defence", 1, 0.4),
                             Actions.Waiting()])

    def level_up(self, level):
        if 2 == level:
            self.max_health = 100
            self.attack = 0.30
            self.defence = 0.20
            self.speed = 25
            self.actions.append(Actions.Attack("Attack level 2", 1, 14, 0.8))


class Electrode(Pokemon):
    def __init__(self):
        self.name = "Electrode_" + str(random.randint(1, 100000))
        self.max_health = self.health = 40
        self.attack = 0.30
        self.defence = 0.10
        self.speed = 25
        self.type = PokemonType.ELECTRIC
        self.actions = list()
        self.effects = list()
        self.actions.extend([Actions.Attack("Electrospit", 1, 14, 0.7),
                             Actions.Attack("Electroblow", 1, 22, 0.6),
                             Actions.Defence("Electroshield", 1, 0.1),
                             Actions.Defence("Electrobulb", 1, 0.3),
                             Actions.Waiting()])

    def level_up(self, level):
        if 2 == level:
            self.max_health = 70
            self.attack = 0.40
            self.defence = 0.15
            self.speed = 30
            self.actions.append(Actions.Attack("Attack level 2", 1, 14, 0.8))


class Pokeball(object):
    @classmethod
    def pull_out_pokemon(cls):
        return selection[random.randrange(0, len(selection))]()

    @staticmethod
    def pick_pokemon(poketype):
        return poketype()


selection = [Eevee, Krabby, Electrode]
