import unittest

from meow_letters.game_elements import Letter, LetterBoard


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

    def test_get_next_letters(self):
        letter_a = Letter("A")
        self.assertEqual(letter_a.get_next_letters(2), [Letter("B"), Letter("C")])
        letter_y = Letter("Y")
        self.assertEqual(letter_y.get_next_letters(1), [Letter("Z")])
        self.assertIsNone(letter_y.get_next_letters(2))
        self.assertRaises(ValueError, letter_y.get_next_letters, 0)



class TestLetterBoard(unittest.TestCase):
    def setUp(self):
        self.board = LetterBoard()

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


if __name__ == '__main__':
    unittest.main()
