import Pokemon
import random


class PokemonEngine(object):
    pokes = list()

    def __init__(self, quantity):
        for a in range(quantity):
            self.pokes.append(Pokemon.Pokeball().pull_out_pokemon())

    def run(self):
        current_round = 1
        while len(self.pokes) > 1:
            print("\nНачинается раунд " + str(current_round) + "!")
            random.shuffle(self.pokes)
            winners = list()
            for a in range(0, len(self.pokes), 2):
                winners.append(self.battle(self.pokes[a], self.pokes[a+1]))
            self.pokes = winners
            current_round += 1
        print("\nКоролем кровавой битвы покемонов становится " + self.pokes[0].name + "!")
        self.pokes[0].introduce_yourself()

    def battle(self, eev1, eev2):
        print("\nБитва между " + eev1.name + " и " + eev2.name + " началась!\n")
        eev1.atb_position += random.randint(0, 10)
        eev2.atb_position += random.randint(0, 10)

        eev1.refresh()
        eev2.refresh()

        while eev1.health > 0 and eev2.health > 0:
            while eev1.atb_position < 100 and eev2.atb_position < 100:
                eev1.atb_step()
                eev2.atb_step()
            if eev1.atb_position >= 100:
                if "KILL" == eev1.action(eev2):
                    return eev1
                eev1.atb_position -= 100
            elif eev2.atb_position >= 100:
                if "KILL" == eev2.action(eev1):
                    return eev2
                eev2.atb_position -= 100
