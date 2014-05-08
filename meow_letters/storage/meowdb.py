import sqlite3


class SqliteDatabase(object):
    """Wrapper class for working with sqlite databases
    """
    def __init__(self, dbname):
        """Initializes a connection to the database and creates a cursor to it

        :param dbname: string name of database
        """
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def execute(self, query):
        """Execute a query

        :param query: string sqlite valid query
        """
        self.cursor.execute(query)
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
        self.dbname = 'meowletters.db'
        self.db = SqliteDatabase(self.dbname)

    def _sanitize(self):
        pass

    def save_highscore(self, username, highscore):
        pass

    def get_top_highscores(self):
        pass
