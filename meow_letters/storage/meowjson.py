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
