import unittest
import random
import loto_classes as lc

class TestNumGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.gen = lc.NumGenerator(numbers_count=lc.NUMBERS_COUNT)
    
    def test_init(self):
        self.assertEqual(len(self.gen.numbers), lc.NUMBERS_COUNT)

    def test_get_next(self):
        for _ in range(lc.NUMBERS_COUNT):
            self.assertGreater(self.gen.get_next(), 0)
        self.assertEqual(self.gen.get_next(), 0)

    def test_str(self):
        self.assertEqual(str(self.gen).split(', '), [str(i) for i in range(1, lc.NUMBERS_COUNT+1)])

    def test_eq(self):
        gen1 = lc.NumGenerator(numbers_count=lc.NUMBERS_COUNT)
        gen2 = lc.NumGenerator(numbers_count=lc.NUMBERS_COUNT+1)
        self.assertTrue(self.gen == gen1)
        self.assertFalse(self.gen == gen2)
        self.assertFalse(self.gen != gen1)
        self.assertTrue(self.gen != gen2)
        gen1.numbers[0]+=1
        self.assertFalse(self.gen == gen1)
        self.assertFalse(self.gen == gen1.numbers)

    def test_sizeof(self):
        self.assertEqual(len(self.gen), lc.NUMBERS_COUNT)
        self.gen.get_next()
        self.assertNotEqual(len(self.gen), lc.NUMBERS_COUNT)
        self.assertEqual(len(self.gen), lc.NUMBERS_COUNT-1)

class TestCard(unittest.TestCase):
    def setUp(self) -> None:
        self.name = 'Test'
        self.card = lc.Card(player_name=self.name)

    def test_init(self):
        self.assertEqual(self.card.name, self.name)
        self.assertEqual(len(self.card.lines), lc.LINE_COUNT)
        for line in range(lc.LINE_COUNT):
            self.assertEqual(len([n for n in self.card.lines[line] if n==0]), lc.LINE_CELLS_COUNT-lc.LINE_NUMBERS_COUNT)
            self.assertEqual(len([n for n in self.card.lines[line] if n>0]), lc.LINE_NUMBERS_COUNT)
        self.assertEqual(self.card.cross_number_count, 0)
        self.assertFalse(self.card.is_full)

    def test_check_cross_number(self):
        for line in self.card.lines.values():
            n = 0
            while n==0:
                n=line[random.randint(0,lc.LINE_CELLS_COUNT-1)]
            self.assertTrue(self.card.check_number(n))
            count = self.card.cross_number_count
            self.card.cross_number(n)
            self.assertFalse(self.card.check_number(n))
            self.assertEqual(self.card.cross_number_count, count+1)

    def test_str(self):
        s = str(self.card)
        self.assertIn(self.name, s)
        self.assertEqual(s.count(' -'), 0)
        for num_line, line in self.card.lines.items():
            n = 0
            while n==0:
                n=line[random.randint(0,lc.LINE_CELLS_COUNT-1)]
            s = str(self.card)
            self.assertEqual(s.count(' -'), num_line)
            self.card.cross_number(n)
            s = str(self.card)
            self.assertEqual(s.count(' -'), num_line+1)

    def test_eq(self):
        card1 = lc.Card(player_name=self.name)
        card2 = lc.Card(player_name='Test1')
        self.assertTrue(self.card == self.card)
        self.assertFalse(self.card == card1)
        self.assertFalse(self.card == card2)
        self.assertFalse(self.card == card2.lines)

class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.name = 'Test'
        self.player = lc.Player(name=self.name)

    def test_init(self):
        self.assertEqual(self.player.name, self.name)
        self.assertFalse(self.player.is_lost)
        self.assertIsInstance(self.player.card, lc.Card)
        self.assertEqual(self.player.card.name, self.name)

    def test_str(self):
        text_lines = str(self.player).split('\n')
        self.assertTrue(self.name in text_lines[0])
        self.assertTrue(self.player.__class__.__name__ in text_lines[0])
        self.assertTrue(self.name in text_lines[1])

    def test_eq(self):
        player1 = lc.Player(name=self.name)
        player2 = lc.Player(name='Test1')
        self.assertTrue(self.player == self.player)
        self.assertFalse(self.player == player1)
        self.assertFalse(self.player == player2)
        self.assertFalse(self.player == player2.card)

class TestComputer(unittest.TestCase):
    def setUp(self) -> None:
        self.name = 'Test'
        self.player = lc.Computer(name=self.name)

    def test_make_move(self):
        self.assertIsInstance(self.player, lc.Player)
        self.assertIsInstance(self.player.card, lc.Card)
        for line in self.player.card.lines.values():
            n = 0
            while n==0:
                n=line[random.randint(0,lc.LINE_CELLS_COUNT-1)]
            self.assertTrue(self.player.card.check_number(n))
            count = self.player.card.cross_number_count
            self.player.make_move(n)
            self.assertFalse(self.player.card.check_number(n))
            self.assertEqual(self.player.card.cross_number_count, count+1)

    def test_str(self):
        text_lines = str(self.player).split('\n')
        self.assertTrue(self.name in text_lines[0])
        self.assertTrue(self.player.__class__.__name__ in text_lines[0])
        self.assertTrue(self.name in text_lines[1])

    def test_eq(self):
        player1 = lc.Computer(name=self.name)
        player2 = lc.Computer(name='Test1')
        self.assertTrue(self.player == self.player)
        self.assertFalse(self.player == player1)
        self.assertFalse(self.player == player2)
        self.assertFalse(self.player == player2.card)

class TestHuman(unittest.TestCase):
    def setUp(self) -> None:
        self.name = 'Test'
        self.player = lc.Human(name=self.name)

    def test_make_move_choiceTrue(self):
        self.player.get_choice = lambda: True
        self.assertIsInstance(self.player, lc.Player)
        self.assertIsInstance(self.player.card, lc.Card)
        self.assertFalse(self.player.is_lost)

        n = 0
        while n==0:
            n=self.player.card.lines[random.randint(0,lc.LINE_COUNT-1)][random.randint(0,lc.LINE_CELLS_COUNT-1)]

        self.player.make_move(current_number=n)
        self.assertFalse(self.player.is_lost)

        self.player.make_move(current_number=n)
        self.assertTrue(self.player.is_lost)

    def test_make_move_choiceFalse(self):
        self.player.get_choice = lambda: True
        n = 0
        while n==0:
            n=self.player.card.lines[random.randint(0,lc.LINE_COUNT-1)][random.randint(0,lc.LINE_CELLS_COUNT-1)]
        self.player.make_move(current_number=n)
        self.assertFalse(self.player.is_lost)

        self.player.get_choice = lambda: False
        self.player.make_move(current_number=n)
        self.assertFalse(self.player.is_lost)

        n = 0
        while n==0:
            n=self.player.card.lines[random.randint(0,lc.LINE_COUNT-1)][random.randint(0,lc.LINE_CELLS_COUNT-1)]
        self.player.make_move(current_number=n)
        self.assertTrue(self.player.is_lost)

    def test_str(self):
        text_lines = str(self.player).split('\n')
        self.assertTrue(self.name in text_lines[0])
        self.assertTrue(self.player.__class__.__name__ in text_lines[0])
        self.assertTrue(self.name in text_lines[1])

    def test_eq(self):
        player1 = lc.Human(name=self.name)
        player2 = lc.Human(name='Test1')
        self.assertTrue(self.player == self.player)
        self.assertFalse(self.player == player1)
        self.assertFalse(self.player == player2)
        self.assertFalse(self.player == player2.card)

class TestGame(unittest.TestCase):
    def test_game_cc(self):
        class GameCC(lc.Game): # Компьютер - компьютер
            def get_players_count(self)->str:
                return '2'
            def get_player_type(self, player_num:int)->str:
                return 'c'
        self.game = GameCC()

        player1 = self.game.players[0]
        player2 = self.game.players[1]
        self.assertEqual(player1.name, 'Comp-1')
        self.assertEqual(player2.name, 'Comp-2')
        self.assertIsInstance(player1, lc.Computer)
        self.assertIsInstance(player2, lc.Computer)

        text = str(self.game)
        self.assertTrue('Comp-1' in text)
        self.assertTrue('Comp-2' in text)
        self.assertTrue(player1.__class__.__name__ in text)
        self.assertTrue(player2.__class__.__name__ in text)

        self.game.begin()
        self.assertFalse(player1.is_lost)
        self.assertFalse(player2.is_lost)
        self.assertTrue(player1.card.is_full==(not player2.card.is_full))

    def test_game_hh(self):
        class GameHH(lc.Game): # Человек - человек
            def get_players_count(self)->str:
                return '2'
            def get_player_type(self, player_num:int)->str:
                return 'h'
            def get_human_name(self, player_num:int)->str:
                return 'Human-' + str(player_num)

        self.game = GameHH()
        
        player1 = self.game.players[0]
        player2 = self.game.players[1]

        player1.get_choice = lambda: random.randint(1,2)==1
        player2.get_choice = lambda: random.randint(1,2)==1
        
        self.assertEqual(player1.name, 'Human-1')
        self.assertEqual(player2.name, 'Human-2')
        self.assertIsInstance(player1, lc.Human)
        self.assertIsInstance(player2, lc.Human)

        text = str(self.game)
        self.assertTrue('Human-1' in text)
        self.assertTrue('Human-2' in text)
        self.assertTrue(player1.__class__.__name__ in text)
        self.assertTrue(player2.__class__.__name__ in text)

        self.game.begin()
        self.assertTrue(player1.is_lost==(not player2.is_lost))
        self.assertEqual(len(self.game.players), 1)


