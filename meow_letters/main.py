from kivy.animation import Animation
from kivy.app import App
from kivy.config import Config
from kivy.clock import Clock
from kivy.graphics import Color, BorderImage
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.widget import Widget
from random import choice
from string import letters

GRID_SIZE = 5

class MenuScreen(Screen):
    pass

class Game(Widget):
    """ This is the Game widget from the GameScreen.
    All application workflow is defined here.
    """
    tile_size = NumericProperty(10)
    tile_padding = NumericProperty(10)
    score = NumericProperty(0)
    level = NumericProperty(1)

    def __init__(self, **kwargs):
        """Game class initializer. Initializes the temporary grid.
        """
        super(Game, self).__init__()
        self.grid = [[None for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        self.restart()

    def rebuild_background(self):
        """Rebuilds the canvas background and the elements
        """
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0x41 / 255., 0x76 / 255., 0x8D / 255.)
            BorderImage(pos=self.pos, size=self.size, source='data/img/mask.png')
            Color(0x63 / 255., 0x94 / 255., 0xA9 / 255.)
            for ix, iy in self.iterate_pos():
                BorderImage(pos=self.index_to_pos(ix, iy), size=(self.tile_size, self.tile_size),
                source='data/img/mask.png')

    def reposition(self, *args):
        self.rebuild_background()
        # calculate the size of a letter
        l = min(self.width, self.height)
        padding = (l / float(GRID_SIZE)) / float(GRID_SIZE * 2)
        tile_size = (l - (padding * (GRID_SIZE+1))) / float(GRID_SIZE)
        self.tile_size = tile_size
        self.tile_padding = padding

        for ix, iy, letter in self.iterate():
            letter.size = tile_size, tile_size
            letter.pos = self.index_to_pos(ix, iy)

    def iterate(self):
        """Helper iterator. Iterates through all cells.
        """
        for ix, iy in self.iterate_pos():
            child = self.grid[ix][iy]
            if child:
                yield ix, iy, child

    def iterate_empty(self):
        """Helper iterator. Iterates through empty cells.
        """
        for ix, iy in self.iterate_pos():
            child = self.grid[ix][iy]
            if not child:
                yield ix, iy

    def iterate_pos(self):
        """Helper iterator. Returns index iterator.
        """
        for ix in range(GRID_SIZE):
            for iy in range(GRID_SIZE):
                yield ix, iy

    def index_to_pos(self, x, y):
        """Translates mathematical index in the grid to the exact
        pixel position.

        :param x index on the x axis.
        :param y index on the y axis.
        """
        padding = self.tile_padding
        tile_size = self.tile_size
        return [
            (self.x + padding) + x * (tile_size + padding),
            (self.y + padding) + y * (tile_size + padding)]

    def pos_to_index(self, coordinates):
        """Translates the pixel coordinates into mathematical indexes.

        :param coordinates a tuple with (x, y) pixel coordinates.
        """
        grid_length = (self.tile_size + self.tile_padding) * GRID_SIZE + self.tile_padding
        if coordinates[0] < 0 \
                or coordinates[1] < 0 \
                or coordinates[0] > grid_length \
                or coordinates[1] > grid_length:
            return (None, None)

        unit = self.tile_size + self.tile_padding
        x = int((coordinates[0] - self.tile_padding) / unit)
        y = int((coordinates[1] - self.tile_padding) / unit)
        return (x, y)

    def spawn_rand_letter(self, *args):
        """Spawns a random letter on the board.
        """
        empty = list(self.iterate_empty())
        if not empty:
            return None
        ix, iy = choice(empty)
        self.spawn_letter_at(ix, iy, choice(letters).upper())

    def spawn_letter_at(self, x, y, value):
        """Spawns a letter to a predefined position.

        :param x index on X axis
        :param y index on Y axis
        :param value the letter
        """
        letter = Letter(
                size=(self.tile_size, self.tile_size),
                pos=self.index_to_pos(x, y),
                letter=str(value))
        self.grid[x][y] = letter
        self.add_widget(letter)

    def on_touch_down(self, touch):
        """Catches the touch event on the grid.
        """
        relative_coordinates = self.to_widget(touch.pos[0], touch.pos[1], True)
        x, y = self.pos_to_index(relative_coordinates)
        if not x is None and not y is None:
            self.spawn_letter_at(x, y, choice(letters).upper())
        return True

    def end(self):
        """Shows a Game over screen inspired from 2048
        """
        end = self.ids.end.__self__
        self.remove_widget(end)
        self.add_widget(end)
        text = 'Game\nover!'
        self.ids.end_label.text = text
        Animation(opacity=1., d=.5).start(end)

    def restart(self):
        """Restarts the game. Puts three random letters on the board.
        """
        self.score = 0
        for ix, iy, child in self.iterate():
            child.destroy()
        self.grid = [[None for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        self.reposition()
        Clock.schedule_once(self.spawn_rand_letter, .1)
        Clock.schedule_once(self.spawn_rand_letter, .1)
        Clock.schedule_once(self.spawn_rand_letter, .1)
        self.ids.end.opacity = 0

class Letter(Widget):
    """ This class represents single letter from the grid.
    (WOW! The grid. So much TRON. Very Cycle. Such ISO.)
    """
    letter = StringProperty('A')
    scale = NumericProperty(.1)

    def __init__(self, **kwargs):
        """Letter class initializer. Animating letters like 2048.
        """
        super(Letter, self).__init__(**kwargs)
        anim = Animation(scale=1., d=.15, t='out_quad')
        anim.bind(on_complete=self.clean_canvas)
        anim.start(self)

    def clean_canvas(self, *args):
        self.canvas.before.clear()
        self.canvas.after.clear()

class GameScreen(Screen):
    pass

class GameOverScreen(Screen):
    pass

class HighscoresScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass


class MeowLettersApp(App):
    def build(self):
        root = ScreenManager(transition=NoTransition())
        root.add_widget(MenuScreen(name='menu'))
        root.add_widget(GameScreen(name='game'))
        root.add_widget(GameOverScreen(name='gameover'))
        root.add_widget(HighscoresScreen(name='highscores'))
        root.add_widget(SettingsScreen(name='settings'))
        return root


if __name__ == '__main__':
    Config.set('graphics', 'width', '320')
    Config.set('graphics', 'height', '480')
    MeowLettersApp().run()
