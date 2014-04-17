import random

from meow_letters.data.alphabets import ENGLISH_ALPHABET as ALPHABET


class Letter(object):
    """Represents a single letter from the game
    """
    def __init__(self, letter):
        """Letter class initializer

        :param letter: valid string letter from an alphabet
        """
        if not isinstance(letter, basestring):
            raise ValueError("Letter class should be initialized with a basestring, \
                received type <{0}>".format(type(letter)))
        self.letter = letter
        self.selected = False

    def __repr__(self):
        return "Letter <{0}>".format(self.letter)

    def select(self):
        """Mark a letter as being selected
        """
        self.selected = True

    def unselect(self):
        """Mark a letter as being unselected
        """
        self.selected = False

    def is_selected(self):
        """Check the state of the letter

        :return: True if the letter is selected, False otherwise
        """
        return self.selected


class LetterBoard(object):
    """Represents all available letters on the board
    """
    def __init__(self, letters=[]):
        """LetterBoard class initializer

        :param letters: iterable data structure (i.e. list, set) of Letter objects
        """
        self.letters = set(letters)

    def setup(self):
        """Initializes the board with 5 random letters with a precomputed adjacent 
        pair of letters

        :return: the current instance
        """
        pass

    def clear(self):
        """Clear the board of letters

        :return: the current instance
        """
        self.letters.clear()
        return self

    def add_letters(self, letters):
        """Add some letters to the board

        :param letters: iterable data structure (i.e. list, set) of Letter objects
        :return: the current instance
        """
        letters = set(letters)
        self.letters.update(letters)
        return self

    def remove_letters(self, letters):
        """Remove some letters from the board

        :param letters: iterable data structure (i.e. list, set) of Letter objects
        :return: the current instance
        """
        letters = set(letters)
        for letter in letters:
            self.letters.remove(letter)
        return self

    def find_adjacent_letters(self, n, gap=0):
        """Find n number of adjacent letters with a possible gap between them. 
        For instance, 2 letters with a gap of value 1 are 'A' and 'C'; or 3 letters
        with no gap between them are 'X', 'Y' and 'Z'.

        :param n: int number of adjacent letters to be found on the board
        :param gap: int possible gap between 2 letters
        :return: list of lists with consecutive ordered Letter objects
        """
        pass

    def get_adjacent_letters(self, letters, chain=2):
        """Return adjacent letters in respect to the available letters

        :param letters: iterable data structure (i.e. list, set) of Letter objects
        :param chain: int length of the required final chain to form
        :return: list of adjacent letter objects
        """
        pass
