import unittest
from Pokemon import Pokemon, PokeBall
import Engine
import math


class PokemonTest(unittest.TestCase):
    def test_gainexp_11_W(self):
        poke1 = PokeBall.pull_out_pokemon()
        poke2 = PokeBall.pull_out_pokemon()
        self.assertEqual(poke1.win(poke2), 1.2, "Неправильное начисление очков опыта! "
                                                "Победа над покемоном одинакового уровня "
                                                "должна давать 0.2 очков опыта")

    def test_gainexp_41_W(self):
        poke1 = PokeBall.pull_out_pokemon()
        poke2 = PokeBall.pull_out_pokemon()
        poke1.level = 4
        self.assertEqual(poke1.win(poke2), 4.05, "Неправильное начисление очков опыта! "
                                                 "Победа над покемоном низкого уровня "
                                                 "должна давать poke1.level/poke2.level*0.2 очков опыта")

    def test_gainexp_14_W(self):
        poke1 = PokeBall.pull_out_pokemon()
        poke2 = PokeBall.pull_out_pokemon()
        poke2.level = 4
        self.assertEqual(poke1.win(poke2), 1.8, "Неправильное начисление очков опыта! "
                                                 "Победа над покемоном высокого уровня "
                                                 "должна давать poke1.level/poke2.level*0.2 очков опыта")

    def test_gainexp_11_L(self):
        poke1 = PokeBall.pull_out_pokemon()
        poke2 = PokeBall.pull_out_pokemon()
        poke1.win(poke2)
        self.assertEqual(poke2.get_level(), 1, "Очки опыта не должны начилсяться при поражении!")



if __name__ == '__main__':
    unittest.main()
