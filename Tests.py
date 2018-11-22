import unittest
from Pokemon import Pokemon, PokeBall


class PokemonTest(unittest.TestCase):
    def test_gainexp_11_W(self):
        poke1 = PokeBall.pull_out_pokemon()
        poke2 = PokeBall.pull_out_pokemon()
        self.assertEqual(poke1.win(poke2), 1.2, "Победа над покемоном своего уровня "
                                                "должна давать 0.2 очков опыта")

    def test_gainexp_41_W(self):
        poke1 = PokeBall.pull_out_pokemon()
        poke2 = PokeBall.pull_out_pokemon()
        poke1.level = 4
        self.assertEqual(poke1.win(poke2), 4.05, "Победа над покемоном уровня ниже своего"
                                                 "должна давать poke1.level/poke2.level*0.2 очков опыта")

    def test_gainexp_14_W(self):
        poke1 = PokeBall.pull_out_pokemon()
        poke2 = PokeBall.pull_out_pokemon()
        poke2.level = 4
        self.assertEqual(poke1.win(poke2), 1.8, "Победа над покемоном уровня выше своего"
                                                "должна давать poke1.level/poke2.level*0.2 очков опыта")

    def test_gainexp_11_L(self):
        poke1 = PokeBall.pull_out_pokemon()
        poke2 = PokeBall.pull_out_pokemon()
        poke1.win(poke2)
        self.assertEqual(poke2.get_level(), 1, "Очки опыта не должны начисляться при поражении!")


if __name__ == '__main__':
    unittest.main()
