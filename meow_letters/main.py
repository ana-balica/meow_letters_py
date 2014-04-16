from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock



class MeowLettersGame(Widget):
	pass


class MeowLettersApp(App):
	def build(self):
		return MeowLettersGame()


if __name__ == '__main__':
	MeowLettersApp().run()