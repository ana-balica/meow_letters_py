from meow_letters.storage.meowdb import MeowDatabase


database = MeowDatabase()
database.db.execute("""CREATE TABLE highscores (id integer primary key autoincrement,
                       username text, highscore integer)""")
database.db.close()
