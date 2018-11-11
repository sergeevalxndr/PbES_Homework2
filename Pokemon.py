import Actions
import random


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
    max_health = health = 50
    attack = 0
    defence = 0.0
    type = PokemonType.NORMAL
    speed = 10
    atb_position = 0
    level = 1

    actions = list()
    effects = list()

    def level_up(self):
        pass

    def atb_step(self):
        self.atb_position += self.speed

    def refresh(self):
        self.health = self.max_health
        self.atb_position = 0

    def get_hp(self):
        return self.health

    def change_hp(self, step):
        self.health += step

    def introduce_yourself(self):
        print("Имя: " + self.name)
        print("Уровень: " + str(self.level))
        print("Тип: " + str(self.type))
        print("Атака: " + str(self.attack))
        print("Защита: " + str(self.defence))
        print("Здоровье: " + str(self.max_health))
        print("Скорость: " + str(self.speed))
        print("Действия: " + str(self.actions))  # TODO вывод действий

    def set_effect(self, effect):
        self.effects.append(effect)

    def action(self, poke):
        action = None
        priority = 5  # Почему 5?
        while not action:
            priority -= 1
            el_actions = list(filter(lambda a: a.priority == priority, self.actions))  # TODO Изменить приоритеты
            if el_actions != []:
                action = el_actions[random.randrange(0, len(el_actions))]

        if type(action) is Actions.Attack:
            if random.randint(0, 100)/100 < action.accuracy:
                damage = int(action.power*(dmg_matrix[self.type][poke.type] + self.attack)
                             *(1 - poke.defence))
                print(self.name + " наносит " + str(damage) + " урона " + poke.name
                      + " способностью " + action.name + " (" + str(poke.health)
                      + "->" + str(poke.health - damage) + ")")
                poke.change_hp(-damage)

                if 0 >= poke.health:
                    print(self.name + " убивает " + poke.name + "!")
                    return "KILL"
            else:
                print(self.name + " попытался использовать способность "
                      + action.name + " и промахнулся!")
        elif type(action) is Actions.Defence:
            # TODO Тут применение эффекта
            print(self.name + " использует защитную способность " + action.name)
        else:
            print(self.name + " ожидает")


class Effect(object):
    duration = 1
    name = "Null effect"


class Eevee(Pokemon):
    def __init__(self):
        self.name = "Eevee_" + str(random.randint(1, 10000))
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

    def level_up(self):
        if 2 <= self.level:
            self.max_health = 75
            self.attack = 0.20
            self.speed = 35
            self.defence = 0.10
            self.actions.append(Actions.Attack("Ear Flop", 1, 14, 0.8))  # TODO Тут должно быть оглушение


class Krabby(Pokemon):
    def __init__(self):
        self.name = "Krabby_" + str(random.randint(1, 10000))
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
                             Actions.Defence("Super Crab Defence", 1, 0.4),  # TODO Тут тоже какая-то способность
                             Actions.Waiting()])

    def level_up(self):
        if 2 <= self.level:
            self.max_health = 100
            self.attack = 0.30
            self.defence = 0.20
            self.speed = 25
            self.actions.append(Actions.Attack("Attack level 2", 1, 14, 0.8))


class Electrode(Pokemon):
    def __init__(self):
        self.name = "Electrode_" + str(random.randint(1, 10000))
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
                             Actions.Defence("Electrobulb", 1, 0.3),  # TODO Тут тоже какая-то способность
                             Actions.Waiting()])

    def level_up(self):
        if 2 <= self.level:
            self.max_health = 70
            self.attack = 0.40
            self.defence = 0.15
            self.speed = 30
            self.actions.append(Actions.Attack("Attack level 2", 1, 14, 0.8))


class Pokeball(object):
    def pull_out_pokemon(self):
        poke = selection[random.randrange(0, len(selection))]
        return self.pick_pokemon(poke)

    def pick_pokemon(self, poketype):
        return poketype()


selection = [Eevee, Krabby, Electrode]
