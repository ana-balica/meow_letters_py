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

    def execute(self, query, commit=False):
        """Execute a query

        :param query: string sqlite valid query
        :param commit: bool if True commit the transaction, otherwise don't yet commit
        """
        self.cursor.execute(query)
        if commit:
            self.conn.commit()

    def executemany(self, query, values, commit=True):
        """Execute many query simultaneously

        :param query: string sqlite valid query
        :param values: list of values to fill in the query
        :param commit: bool if True commit the transaction, otherwise don't yet commit
        """
        self.cursor.executemany(query, values)
        if commit:
            self.conn.commit()

    def commit(self):
        """Commit transactions
        """
        self.conn.commit()

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
