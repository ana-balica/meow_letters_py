from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition


class MenuScreen(Screen):
    pass

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
