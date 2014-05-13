import os
import sqlite3


PROJECT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")


class SqliteDatabase(object):
    """Wrapper class for working with sqlite databases
    """
    def __init__(self, dbname):
        """Initializes a connection to the database and creates a cursor to it

        :param dbname: string name of database
        """
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=()):
        """Execute a query

        :param query: string sqlite valid query
        :param params: tuple of parameters
        """
        self.cursor.execute(query, params)
        self.conn.commit()

    def executemany(self, query, values):
        """Execute many query simultaneously

        :param query: string sqlite valid query
        :param values: list of values to fill in the query
        """
        self.cursor.executemany(query, values)
        self.conn.commit()

    def fetch(self, type='all'):
        """Commit transactions

        :param type: string type of fetch - one, all, many
        :return: fetched data
        """
        if type == 'all':
            return self.cursor.fetchall()
        elif type ==  'one':
            return self.cursor.fetchone()
        elif type == 'many':
            return self.cursor.fetchmany()
        else:
            raise ValueError("Unknown type of fetch - {}".format(type))

    def close(self):
        """Close the connection
        """
        self.conn.close()


class MeowDatabase(object):
    """Meow Letters game database
    """
    def __init__(self):
        """Initialize a connection to 'meowletters.db'
        """
        self.dbname = os.path.join(PROJECT_PATH, 'meowletters.db')
        self.db = SqliteDatabase(self.dbname)

    def _sanitize_highscores(self):
        """Sanitize the highscores table by deleting entries with lower score than
        the last entry from the top ten hits

        :return: the current instance
        """
        query = "SELECT highscore FROM highscores ORDER BY highscore DESC LIMIT 10"
        self.db.execute(query)
        min_highscore = self.db.fetch('all')[-1][0]
        query = "DELETE FROM highscores WHERE highscore < {0}".format(min_highscore)
        self.db.execute(query)
        return self

    def insert_highscore(self, username, highscore):
        """Insert a highscore entry

        :param username: string username
        :param highscore: int highscore value
        :return: the current instance
        """
        query = """INSERT INTO highscores VALUES (Null, ?, ?)"""
        params = (username, highscore)
        self.db.execute(query, params)
        self._sanitize_highscores()
        return self

    def get_top_highscores(self):
        """Get top 10 highscores. If table contains less than 10 hits, return all
        of them

        :return: list of hits containing (username, highscore)
        """
        query = "SELECT username, highscore FROM highscores ORDER BY highscore DESC LIMIT 10"
        self.db.execute(query)
        return self.db.fetch('all')
