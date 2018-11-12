import Pokemon
import random
import math


class PokemonEngine(object):
    pokes = list()

    def __init__(self, quantity):
        for a in range(quantity):
            self.pokes.append(Pokemon.Pokeball().pull_out_pokemon())

    def run(self):
        pokes_quantity = math.log2(len(self.pokes))
        if int(pokes_quantity) != float(pokes_quantity):
            raise Exception("Невозможно сформировать турнирную таблицу!")

        self.__introduce_participants__()

        current_round = 1
        while len(self.pokes) > 1:
            print("\nНачинается раунд %s!" % str(current_round))
            random.shuffle(self.pokes)
            winners = list()
            for a in range(0, len(self.pokes), 2):
                winners.append(self.battle(self.pokes[a], self.pokes[a+1]))
            self.pokes = winners
            current_round += 1
        print("\nКоролем кровавой битвы покемонов становится %s!" % self.pokes[0].name)
        self.pokes[0].introduce_yourself()

    def battle(self, eev1, eev2):
        print("\nБитва между %s и %s началась!\n" % (eev1.name, eev2.name))
        eev1.atb_position += random.randint(0, 10)
        eev2.atb_position += random.randint(0, 10)

        eev1.refresh()
        eev2.refresh()

        while True:
            while eev1.atb_position < 100 and eev2.atb_position < 100:  # Turn()
                eev1.atb_step()
                eev2.atb_step()
                # print("%s, %s" % (eev1.atb_position, eev2.atb_position))   # Вывод позиции на atb-шкале
                # print("%s, %s" % (eev1.effects, eev2.effects))  # Вывод текущих эффектов
            if eev1.atb_position >= 100:
                # TODO Effects proceeding
                if "KILL" == eev1.action(eev2):
                    return eev1
                eev1.atb_position -= 100
            elif eev2.atb_position >= 100:
                if "KILL" == eev2.action(eev1):
                    return eev2
                eev2.atb_position -= 100

    def __introduce_participants__(self):
        print("Участники:")
        for a in self.pokes:
            print(a.name)