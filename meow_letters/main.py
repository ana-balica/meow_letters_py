import os
import copy
from random import choice
from string import letters

from kivy.animation import Animation
from kivy.app import App
from kivy.base import EventLoop
from kivy.config import Config
from kivy.clock import Clock
from kivy.graphics import Color, BorderImage
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.uix.widget import Widget

from constants.colors import *
from constants.misc import *
from letters import LetterGrid, Letter
from level import Level
from score import Score
from screens import (MenuScreen, GameScreen, GameOverScreen, HighscoresScreen,
                     SettingsScreen)
from storage.meowjson import SettingsJson
from storage.meowdb import MeowDatabase
from meow_letters import PROJECT_PATH


class Game(Widget):
    """ This is the Game widget from the GameScreen.
    All application workflow is defined here.
    """
    tile_size = NumericProperty(10)
    tile_padding = NumericProperty(10)

    def __init__(self, **kwargs):
        """Game class initializer. Initializes the temporary grid.
        """
        super(Game, self).__init__()
        self.grid = [[None for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        self.letter_grid = LetterGrid(GRID_SIZE)
        self.score = Score()
        self.level = Level()
        self.io = MeowDatabase()

    def rebuild_background(self):
        """Rebuilds the canvas background and the elements
        """
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*BLUE)
            BorderImage(pos=self.pos,
                        size=self.size,
                        source=os.path.join(PROJECT_PATH,
                                            'assets/img/mask.png'))
            Color(*LIGHTER_BLUE)
            for ix, iy in self.letter_grid.iterate_pos():
                BorderImage(pos=self.index_to_pos(ix, iy),
                            size=(self.tile_size, self.tile_size),
                            source=os.path.join(PROJECT_PATH,
                                                'assets/img/mask.png'))

    def reposition(self, *args):
        self.rebuild_background()
        # calculate the size of a letter
        l = min(self.width, self.height)
        padding = (l / float(GRID_SIZE)) / float(GRID_SIZE * 2)
        tile_size = (l - (padding * (GRID_SIZE + 1))) / float(GRID_SIZE)
        self.tile_size = tile_size
        self.tile_padding = padding

        for ix, iy, letter in self.iterate():
            letter.size = tile_size, tile_size
            letter.pos = self.index_to_pos(ix, iy)

    def iterate(self):
        """Helper iterator. Iterates through all cells.
        """
        for ix, iy in self.letter_grid.iterate_pos():
            child = self.grid[ix][iy]
            if child:
                yield ix, iy, child

    def iterate_empty(self):
        """Helper iterator. Iterates through empty cells.
        """
        for ix, iy in self.letter_grid.iterate_pos():
            child = self.grid[ix][iy]
            if not child:
                yield ix, iy

    def index_to_pos(self, x, y):
        """Translates mathematical index in the grid to the exact
        pixel position.

        :param x: index on the x axis.
        :param y: index on the y axis.
        """
        padding = self.tile_padding
        tile_size = self.tile_size
        return [
            (self.x + padding) + x * (tile_size + padding),
            (self.y + padding) + y * (tile_size + padding)]

    def pos_to_index(self, coordinates):
        """Translates the pixel coordinates into mathematical indexes.

        :param coordinates: a tuple with (x, y) pixel coordinates.
        """
        grid_length = (
                      self.tile_size + self.tile_padding) * GRID_SIZE + self.tile_padding
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

        :param x: index on X axis
        :param y: index on Y axis
        :param value: the letter
        """
        if self.grid[x][y] is None \
            or self.grid[x][y].letter != self.letter_grid[x][y].letter:
            letter = LetterCell(
                size=(self.tile_size, self.tile_size),
                pos=self.index_to_pos(x, y),
                letter=str(value))
            self.remove_widget(self.grid[x][y])
            self.grid[x][y] = letter
            self.add_widget(letter)

    def on_touch_down(self, touch):
        """Catches the touch event on the grid.
        """
        relative_coordinates = self.to_widget(touch.pos[0], touch.pos[1], True)
        x, y = self.pos_to_index(relative_coordinates)
        if x is not None and y is not None:
            self.toggle(x, y)

        super(Game, self).on_touch_down(touch)
        return True

    def toggle(self, x, y):
        game_screen = self.parent.parent.parent
        decrement = Clock.create_trigger(game_screen.ids.timer.decrement)
        letter = self.letter_grid[x][y]
        if letter is not None:
            if letter.is_selected():
                self.letter_grid.chain.remove(letter)
            else:
                self.letter_grid.chain.add(letter)
                if not self.letter_grid.chain.is_valid():
                    decrement()
                    self.letter_grid.chain.clear()

            if self.letter_grid.is_complete_chain():
                game_screen.ids.timer.reset()
            self.update_grid()

    def update_grid(self):
        for x, y, letter in self.letter_grid.iterate():
            if letter.is_selected():
                self.grid[x][y].select()
            else:
                self.grid[x][y].unselect()

    def end(self):
        """Shows a Game over screen inspired from 2048
        """
        game_screen = self.parent.parent.parent
        game_screen.end = True
        self.save_highscore()
        end = self.ids.end.__self__
        self.remove_widget(end)
        self.add_widget(end)
        text = 'Game\nover!'
        self.ids.end_label.text = text
        Animation(opacity=1., d=.5).start(end)

    def restart(self):
        """Restarts the game. Puts three random letters on the board.
        """
        self.score.reset()
        self.level.reset()
        for ix, iy, child in self.iterate():
            self.remove_widget(child)
        self.grid = [[None for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        self.reposition()
        self.letter_grid = LetterGrid(GRID_SIZE)
        self.letter_grid.setup(3)
        Clock.schedule_once(self.redraw)
        self.ids.end.opacity = 0
        if self.parent:
            game_screen = self.parent.parent.parent
            if game_screen.end == True:
                game_screen.ids.timer.restart()
                Clock.unschedule(game_screen.tick)
                Clock.schedule_interval(game_screen.tick,
                                        game_screen.ids.timer.interval)
                game_screen.end = False

    def resume(self, score, level, grid):
        self.score.points = int(score)
        self.level.set_level(int(level))
        for ix, iy, child in self.iterate():
            self.remove_widget(child)
        self.grid = [[None for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        self.reposition()
        letter_grid = copy.deepcopy(grid)
        for i, row in enumerate(grid):
            letter_grid[i] = [Letter(l) if l is not None else None for l in row]
        self.letter_grid = LetterGrid(GRID_SIZE)
        self.letter_grid.grid = letter_grid
        Clock.schedule_once(self.redraw)
        self.ids.end.opacity = 0

    def redraw(self, *args):
        for x, y in self.letter_grid.iterate_pos():
            if self.letter_grid[x][y] is None:
                if self.grid[x][y] is not None:
                    self.remove_widget(self.grid[x][y])
                    self.grid[x][y] = None
            else:
                self.spawn_letter_at(x, y, self.letter_grid[x][y].letter)

    def cycle_end(self):
        self.score.update(self.letter_grid.chain.length)
        self.level.set_level(self.score.points)
        self.letter_grid.cycle_end(self.level.level)
        self.redraw()
        self.update_grid()

    def save_highscore(self):
        settings = SettingsJson(
            os.path.join(PROJECT_PATH, "data/settings.json"))
        self.io.insert_highscore(settings.get_username(), self.score.points)


class Timer(Widget):
    def __init__(self, **kwargs):
        super(Timer, self).__init__()
        self.redraw()
        self.interval = 0.05
        self.finished = False

    def redraw(self):
        self.opacity = 1
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*PINK)
            BorderImage(pos=self.pos, size=self.size,
                        source=os.path.join(PROJECT_PATH,
                                            'assets/img/mask.png'))

    def tick(self, *args):
        if self.size[0] < 0:
            self.finished = True

        width = self.parent.size[0]
        self.size[0] -= width / (ROUND_SECONDS / self.interval)
        self.redraw()

    def restart(self):
        self.finished = False
        self.size[0] = self.parent.size[0]

    def decrement(self, seconds=1):
        width = self.parent.size[0]
        self.size[0] -= width / ROUND_SECONDS

    def reset(self):
        self.finished = True
        self.size[0] = self.parent.size[0]


class LetterCell(Widget):
    """ This class represents single letter from the grid.
    (WOW! The grid. So much TRON. Very Cycle. Such ISO.)
    """
    letter = StringProperty('A')
    scale = NumericProperty(.1)
    bg_color = ObjectProperty(LIGHT_BROWN)

    def __init__(self, **kwargs):
        """Letter class initializer. Animating letters like 2048.
        """
        super(LetterCell, self).__init__(**kwargs)
        anim = Animation(scale=1., d=.15, t='out_quad')
        anim.bind(on_complete=self.clean_canvas)
        anim.start(self)

    def clean_canvas(self, *args):
        self.canvas.before.clear()
        self.canvas.after.clear()

    def select(self):
        self.bg_color = WHITE

    def unselect(self):
        self.bg_color = LIGHT_BROWN


class MeowLettersApp(App):
    def on_start(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def build(self):
        self.manager = ScreenManager(transition=NoTransition())
        self.manager.add_widget(MenuScreen(name='menu'))
        self.manager.add_widget(GameScreen(name='game'))
        self.manager.add_widget(GameOverScreen(name='gameover'))
        self.manager.add_widget(HighscoresScreen(name='highscores'))
        self.manager.add_widget(SettingsScreen(name='settings'))
        return self.manager

    def hook_keyboard(self, window, key, *args):
        if key == BACK_KEY:
            self.manager.current = 'menu'
            return True


if __name__ == '__main__':
    Config.set('graphics', 'width', '320')
    Config.set('graphics', 'height', '480')
    MeowLettersApp().run()
