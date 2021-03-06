import unittest
import tntfl.transforms.rank as rankTransform
from tntfl.game import Game


class TestRank(unittest.TestCase):
    def test(self):
        games = []
        game = Game('red', 6, 'blue', 4, 1)
        game.skillChangeToBlue = -2.5
        games.append(game)
        game = Game('red', 1, 'blue', 9, 1)
        game.skillChangeToBlue = 10.4
        games.append(game)

        games = rankTransform.do(games)

        self.assertEqual(1, games[0].redPosAfter)
        self.assertEqual(2, games[0].bluePosAfter)
        self.assertEqual(2, games[1].redPosAfter)
        self.assertEqual(-1, games[1].redPosChange)
        self.assertEqual(1, games[1].bluePosAfter)
        self.assertEqual(1, games[1].bluePosChange)

    def testInactive(self):
        games = []
        game = Game('red', 6, 'blue', 4, 1)
        game.skillChangeToBlue = -2.5
        games.append(game)
        game = Game('red', 5, 'green', 5, 6000000)
        game.skillChangeToBlue = 0
        games.append(game)

        games = rankTransform.do(games)

        self.assertEqual(1, games[0].redPosAfter)
        self.assertEqual(2, games[0].bluePosAfter)
        self.assertEqual(1, games[1].redPosAfter)
        self.assertEqual(0, games[1].redPosChange)
        self.assertEqual(2, games[1].bluePosAfter)
        self.assertEqual(0, games[1].bluePosChange)

    def testReactive(self):
        games = []
        game = Game('red', 6, 'blue', 4, 1)
        game.skillChangeToBlue = -2.5
        games.append(game)
        game = Game('red', 5, 'green', 5, 6000000)
        game.skillChangeToBlue = 0
        games.append(game)
        game = Game('red', 1, 'blue', 9, 7000000)
        game.skillChangeToBlue = 10.4
        games.append(game)

        games = rankTransform.do(games)

        self.assertEqual(3, games[2].redPosAfter)
        self.assertEqual(-2, games[2].redPosChange)
        self.assertEqual(1, games[2].bluePosAfter)
        self.assertEqual(0, games[2].bluePosChange)
