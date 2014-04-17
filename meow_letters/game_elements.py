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
