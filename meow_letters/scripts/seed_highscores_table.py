from random import randint

from meow_letters.storage.meowdb import MeowDatabase


database = MeowDatabase()
database.insert_highscore("Foo", randint(1, 10000))
database.insert_highscore("Bar", randint(1, 10000))
database.insert_highscore("Foo", randint(1, 10000))
database.insert_highscore("FooBar", randint(1, 10000))
database.insert_highscore("Bar", randint(1, 10000))
database.insert_highscore("Foo", randint(1, 10000))
database.insert_highscore("Bar", randint(1, 10000))
database.insert_highscore("Foo", randint(1, 10000))
database.insert_highscore("FooBar", randint(1, 10000))
database.insert_highscore("Bar", randint(1, 10000))
database.insert_highscore("Foo", randint(1, 10000))
database.insert_highscore("Bar", randint(1, 10000))
database.insert_highscore("Foo", randint(1, 10000))
database.insert_highscore("FooBar", randint(1, 10000))
database.insert_highscore("Bar", randint(1, 10000))
database.insert_highscore("Foo", randint(1, 10000))
database.insert_highscore("Bar", randint(1, 10000))
database.insert_highscore("Foo", randint(1, 10000))
database.insert_highscore("FooBar", randint(1, 10000))
database.insert_highscore("Bar", randint(1, 10000))
database.db.close()
