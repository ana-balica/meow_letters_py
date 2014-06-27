import os
import copy
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

from constants.colors import *
from storage.meowjson import SettingsJson, StateJson
from storage.meowdb import MeowDatabase
from meow_letters import PROJECT_PATH


class MenuButton(Button):
    """Mapping class to the button declared in kv file
    """
    pass


class MenuScreen(Screen):
    """Represents the menu screen of the game
    """
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.state = StateJson(os.path.join(PROJECT_PATH, "data/state.json"))
        self.button = MenuButton(text="Continue")

    def on_enter(self, *args):
        self.ids.new_game_btn.bind(on_press=self.new_game)
        if not self.state.empty:
            self.button.bind(on_press=self.continue_game)
            self.ids.menu.add_widget(self.button, index=3)

    def on_leave(self, *args):
        self.ids.menu.remove_widget(self.button)

    def continue_game(self, *args):
        game_screen = self.parent.get_screen('game')
        game_screen.resume = True
        self.parent.current = 'game'

    def new_game(self, *args):
        game_screen = self.parent.get_screen('game')
        game_screen.resume = False
        self.parent.current = 'game'


class GameScreen(Screen):
    """Represents the game screen
    """
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.state = StateJson(os.path.join(PROJECT_PATH, "data/state.json"))
        self.resume = False
        self.end = False

    def tick(self, *args):
        timer = self.ids.timer
        timer.tick()
        if timer.finished:
            self.ids.game.cycle_end()
            self.ids.score.text = "Score {0}".format(self.ids.game.score.points)
            self.ids.level.text = "Level {0}".format(self.ids.game.level.level)
            if self.ids.game.letter_grid.end:
                self.ids.game.end()
                self.timer_stop()
                timer.opacity = 0
            else:
                timer.restart()

    def timer_stop(self):
        Clock.unschedule(self.tick)

    def on_pre_enter(self, *args):
        self.end = False
        if self.resume:
            self.state.restore()
            self.state.clear()

            score = self.state.get_score()
            level = self.state.get_level()
            grid = self.state.get_grid()
            self.ids.score.text = "Score {0}".format(score)
            self.ids.level.text = "Level {0}".format(level)
            self.ids.timer.size[0] = self.state.get_timer()
            self.ids.game.resume(score, level, grid)
        else:
            self.state.clear()
            self.ids.game.restart()
            self.ids.timer.restart()
            self.ids.score.text = "Score {0}".format(self.ids.game.score.points)
            self.ids.level.text = "Level {0}".format(self.ids.game.level.level)
        Clock.unschedule(self.tick)
        Clock.schedule_interval(self.tick, self.ids.timer.interval)

    def on_pre_leave(self, *args):
        if not self.end:
            score = self.ids.game.score
            level = self.ids.game.level
            timer = self.ids.timer.size[0]
            grid = copy.deepcopy(self.ids.game.letter_grid.grid)
            for i, row in enumerate(grid):
                grid[i] = [l.letter if l is not None else None for l in row]
            self.state.save(level.level, score.points, timer, grid)
        else:
            self.state.clear()
        self.timer_stop()


class GameOverScreen(Screen):
    """Mapping to the GameOverScreen declared in kv file
    """
    pass


class HighscoreLabel(Label):
    """Custom label widget for representing highscores
    """
    def __init__(self, root, text, halign):
        super(HighscoreLabel, self).__init__()
        self.text = text
        self.halign = halign
        self.color = DARK_BLUE
        self.font_size = min(root.height, root.width) / 18.
        self.width = root.width / 2.5
        self.height = min(root.height, root.width) / 16.
        self.text_size = (root.width / 2.5, None)
        self.size_hint = (None, None)


class HighscoresScreen(Screen):
    """Represents game highscores screen
    """
    highscores_layout = ObjectProperty(None)
    io = MeowDatabase()

    def on_enter(self):
        self.highscores_layout.clear_widgets()
        self.append_title()
        highscores = self.io.get_top_highscores()
        for i, entry in enumerate(highscores):
            i += 1
            username = "{0}.  {1}".format(i, entry[0])
            self.highscores_layout.add_widget(
                HighscoreLabel(self.highscores_layout, username, "left"))
            highscore = str(entry[1])
            self.highscores_layout.add_widget(
                HighscoreLabel(self.highscores_layout, highscore, "right"))

    def append_title(self):
        self.highscores_layout.add_widget(
            Label(text="Highscores",
                  color=DARK_BROWN,
                  font_size=min(self.highscores_layout.height,
                                self.highscores_layout.width) / 10.,
                  width=self.highscores_layout.width,
                  size_hint_y=None,
                  height=min(self.highscores_layout.height,
                             self.highscores_layout.width) / 4.))


class SettingsScreen(Screen):
    """Represents game settings screen
    """
    username_input = ObjectProperty(None)
    io = SettingsJson(os.path.join(PROJECT_PATH, "data/settings.json"))

    def on_leave(self):
        self.io.save_username(self.username_input.text)

    def on_pre_enter(self):
        self.username_input.text = self.io.get_username()
