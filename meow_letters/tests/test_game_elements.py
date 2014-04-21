import unittest

from meow_letters.game_elements import Letter, LetterChain, LetterBoard, is_valid_gap


class TestLetter(unittest.TestCase):
    def test_init(self):
        self.assertRaises(TypeError, Letter)
        self.assertRaises(ValueError, Letter, 1)
        letter = Letter('A')
        self.assertEqual(letter.letter, 'A')
        self.assertFalse(letter.selected)

    def test_selection(self):
        letter = Letter('A')
        self.assertFalse(letter.selected)
        self.assertFalse(letter.is_selected())
        letter.select()
        self.assertTrue(letter.selected)
        self.assertTrue(letter.is_selected())
        letter.unselect()
        self.assertFalse(letter.selected)
        self.assertFalse(letter.is_selected())

    def test_next(self):
        letter_g = Letter('G')
        self.assertEqual(letter_g.next, Letter("H"))
        letter_z = Letter('Z')
        self.assertIsNone(letter_z.next)

    def test_previous(self):
        letter_g = Letter('G')
        self.assertEqual(letter_g.previous, Letter("F"))
        letter_a = Letter('A')
        self.assertIsNone(letter_a.previous)

    def test_adjacent(self):
        letter_a = Letter('A')
        self.assertEqual(letter_a.adjacent, [None, Letter("B")])
        letter_t = Letter("T")
        self.assertEqual(letter_t.adjacent, [Letter("S"), Letter("U")])
        letter_z = Letter("Z")
        self.assertEqual(letter_z.adjacent, [Letter("Y"), None])

    def test_any_adjacent(self):
        letter_a = Letter('A')
        self.assertEqual(letter_a.any_adjacent, Letter("B"))
        letter_t = Letter("T")
        self.assertIn(letter_t.any_adjacent, [Letter("U"), Letter("S")])
        letter_z = Letter("Z")
        self.assertEqual(letter_z.any_adjacent, Letter("Y"))

    def test_is_first(self):
        letter_a = Letter("A")
        self.assertTrue(letter_a.is_first())
        letter_p = Letter("P")
        self.assertFalse(letter_p.is_first())

    def test_is_last(self):
        letter_p = Letter("P")
        self.assertFalse(letter_p.is_last())
        letter_z = Letter("Z")
        self.assertTrue(letter_z.is_last())

    def test_get_next_letters(self):
        letter_a = Letter("A")
        self.assertEqual(letter_a.get_next_letters(1), [Letter("B")])
        self.assertEqual(letter_a.get_next_letters(2), [Letter("B"), Letter("C")])
        letter_y = Letter("Y")
        self.assertEqual(letter_y.get_next_letters(1), [Letter("Z")])
        self.assertIsNone(letter_y.get_next_letters(2))
        self.assertRaises(ValueError, letter_y.get_next_letters, 0)

    def test_get_adjacent_letters(self):
        letter_a = Letter("A")
        letter_z = Letter("Z")
        self.assertRaises(ValueError, letter_a.get_adjacent_letters, 0)
        self.assertRaises(ValueError, letter_a.get_adjacent_letters, 27)
        self.assertEqual(letter_a.get_adjacent_letters(3), [letter_a, Letter("B"), Letter("C")])
        self.assertEqual(letter_z.get_adjacent_letters(3), [Letter("X"), Letter("Y"), letter_z])

        letter_b = Letter("B")
        adjacents = letter_b.get_adjacent_letters(6)
        self.assertEqual(len(adjacents), 6)
        for a in adjacents:
            self.assertIn(a, [letter_a, letter_b, Letter("C"), Letter("D"),
                              Letter("E"), Letter("F"), Letter("G")])

        letter_h = Letter("H")
        adjacents = letter_h.get_adjacent_letters(3)
        self.assertEqual(len(adjacents), 3)
        for a in adjacents:
            self.assertIn(a, [Letter("F"), Letter("G"), letter_h, Letter("I"), Letter("J")])



class TestLetterChain(unittest.TestCase):
    def setUp(self):
        self.chain = LetterChain()

    def test_add(self):
        letter_a = Letter("A")
        letter_b = Letter("B")
        self.chain.add(letter_a)
        self.assertEqual(self.chain.chain, [letter_a])
        self.chain.add(letter_b)
        self.assertEqual(self.chain.chain, [letter_a, letter_b])

    def test_is_valid(self):
        letter_a = Letter("A")
        letter_b = Letter("B")
        letter_d = Letter("D")
        self.assertTrue(self.chain.is_valid())
        self.chain.add(letter_a)
        self.assertTrue(self.chain.is_valid())
        self.chain.add(letter_b)
        self.assertTrue(self.chain.is_valid())
        self.chain.add(letter_d)
        self.assertFalse(self.chain.is_valid())
        self.chain.chain = [letter_a, letter_a]
        self.assertFalse(self.chain.is_valid())

class TestLetterBoard(unittest.TestCase):
    def setUp(self):
        self.board = LetterBoard()

    def test_setup(self):
        self.assertRaises(ValueError, self.board.setup, 0)
        self.assertRaises(ValueError, self.board.setup, 2)
        for i in xrange(3, 6):
            self.board.setup(i)
            self.assertEqual(len(self.board.letters), i)
            combinations = self.board.find_consecutive_combinations(2)
            self.assertIsNotNone(combinations)
            comb_lens = []
            for comb in combinations:
                comb_lens.append(len(comb))
            self.assertIn(2, comb_lens)
            self.board.clear()

    def test_clear(self):
        self.board.letters.add(Letter("A"))
        self.assertEqual(len(self.board.letters), 1)
        self.board.clear()
        self.assertEqual(len(self.board.letters), 0)

    def test_add_letters(self):
        letter_a = Letter("A")
        letter_b = Letter("B")
        letter_a2 = Letter("A")

        tests = [[], [letter_a], [letter_a, letter_a2], [letter_a, letter_b]]
        results = [set(), 
                   {letter_a},
                   {letter_a, letter_a2},
                   {letter_a, letter_b, letter_a2}]
        for i, test in enumerate(tests):
            self.board.add_letters(test)
            self.assertEqual(self.board.letters, results[i])

    def test_remove_letters(self):
        letter_a = Letter("A")
        letter_b = Letter("B")
        letter_a2 = Letter("A")
        self.board.add_letters([letter_a, letter_b, letter_a2])

        tests = [[], [letter_a], [letter_b, letter_a2]]
        results = [{letter_a, letter_b, letter_a2},
                   {letter_b, letter_a2},
                   set()]
        for i, test in enumerate(tests):
            self.board.remove_letters(test)
            self.assertEqual(self.board.letters, results[i])

        self.assertRaises(KeyError, self.board.remove_letters, [1])

    def test_find_consecutive_combinations(self):
        letter_a = Letter("A")
        letter_a2 = Letter("A")
        letter_b = Letter("B")
        letter_c = Letter("C")
        self.board.add_letters([letter_a, letter_a2, letter_b, letter_c])

        self.assertRaises(ValueError, self.board.find_consecutive_combinations, 1)
        self.assertEqual(self.board.find_consecutive_combinations(2), [["A", "B"], ["B", "C"]])
        self.assertEqual(self.board.find_consecutive_combinations(3), [["A", "B", "C"]])
        self.assertEqual(self.board.find_consecutive_combinations(4), [])


class TestHelperFunctions(unittest.TestCase):
    def test_is_valid_gap(self):
        self.assertRaises(ValueError, is_valid_gap, [True], -1)
        argss = [([True, True], 0), ([True, True], 1), ([False, True], 1),
                 ([True, False], 1), ([True, True, False], 1),
                 ([True, False, True], 1),
                 ([True, False, True, False], 1),
                 ([True, False, False, True], 2),
                 ([True, False, True, False, True], 2),
                 ([True, True, True], 1),
                 ([True, True, True, False, True], 2),
                 ([True, False, False, False, False, True], 2)]
        expected_results = [True, False, False, False, False, True, False, True, True, True, True, False]
        for i, args in enumerate(argss):
            result = is_valid_gap(*args)
            self.assertEqual(result, expected_results[i])


if __name__ == '__main__':
    unittest.main()
