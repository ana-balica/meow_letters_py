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
                   set([letter_a]), 
                   set([letter_a, letter_a2]), 
                   set([letter_a, letter_b, letter_a2])]
        for i, test in enumerate(tests):
            self.board.add_letters(test)
            self.assertEqual(self.board.letters, results[i])


if __name__ == '__main__':
    unittest.main()
