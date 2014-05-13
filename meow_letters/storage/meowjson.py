import os
import json


class MeowJson(object):
    """Helper class to work with json stored in a file
    """
    def __init__(self, filename):
        """Class initializer

        :param filename: string filename where from json is or will be stored
        """
        self.filename = filename

    def load(self):
        """Load and deserialize json data from the file

        :return: data object
        """
        with open(self.filename, "rb") as f:
            data = json.load(f)
        return data

    def dumps(self, data):
        """Serialize json object and save to a file

        :param data: data object
        """
        with open(self.filename, "wb") as f:
            f.write(json.dumps(data, indent=4, separators=(',', ': ')))



class SettingsJson(object):
    """Helper class to work with settings stored as a json
    """
    def __init__(self, filename):
        """Class initializer

        :param filename: string filename where from json is or will be stored
        """
        self.filename = filename
        self.meowjson = MeowJson(filename)

    def save_username(self, username):
        """Save username user setting

        :param username: str username
        """
        settings = self.meowjson.load()
        settings['settings']['username'] = str(username)
        self.meowjson.dumps(settings)

    def get_username(self):
        """Return username user setting

        :return: string username
        """
        settings = self.meowjson.load()
        return settings['settings']['username']


class StateJson(object):
    """Helper class to serialize/deserialize game state
    """
    def __init__(self, filename):
        """Class initializer

        :param filename: string filename where from json is or will be stored
        """
        self.filename = filename
        self.meowjson = MeowJson(filename)
        self.state = None

    def save(self, level, score, timer, grid):
        """Save game state

        :param level: int current level
        :param score: int current score
        :param timer: float current timer position
        :param grid: list of lists contains Nones and string letters
        :return: the current instance
        """
        state = {"level": level, "score": score, "timer": timer, "grid": grid}
        self.meowjson.dumps(state)
        return self

    def restore(self):
        """Restore game state and store it as instance variable

        :return: decoded json with game state
        """
        self.state = self.meowjson.load()
        return self.state

    def get_level(self):
        """Get game level

        :return: int level
        """
        if self.state:
            return self.state["level"]
        return self.restore()["level"]

    def get_score(self):
        """Get game score

        :return: int score
        """
        if self.state:
            return self.state["score"]
        return self.restore()["score"]

    def get_timer(self):
        """Get timer position

        :return: float timer position
        """
        if self.state:
            return self.state["timer"]
        return self.restore()["timer"]

    def get_grid(self):
        """Get game grid

        :return: list of lists contains Nones and string letters
        """
        if self.state:
            return self.state["grid"]
        return self.restore()["grid"]

    @property
    def empty(self):
        """Check if the game state json is empty

        :return: True if empty, False - otherwise
        """
        return os.path.getsize(self.filename) == 0

    def clear(self):
        """Clear the json stored state

        :return: the current instance
        """
        open(self.filename, 'w').close()
        return self
