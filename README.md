Meow Letters
============

Meow Letters is an educational game for children to practice the knowledge of English alphabet.


Prerequisites
------------

1. Kivy 1.8
2. Sqlite3


How to run
----------

1. Create an sqlite database with one empty table. From the root directory run: `python meow_letters/scripts/highscores_table.py`
2. Run the app on your desktop: `python meow_letters/main.py`
3. Optionally the app can be deployed on Android using buildozer. Install [buildozer](http://buildozer.readthedocs.org/en/latest/installation.html). Enable developer mode on your Android phone and run `buildozer android debug deploy` from the directory that contains `main.py`

If you face problems with imports, add the project to `PYTHONPATH`. One possible solution is to create a path configuration file:
```python
SITEDIR=$(python -m site --user-site)
mkdir -p "SITEDIR"
echo "/path/to/meow_letters" > "SITEDIR/meowletters.pth"
```

*The app was tested on Nexus 5 phone.*


How to play
-----------

Let's test how good you are at English alphabet.

Press on **New game** to start Meow Letters. The screen will shown a bunch of letters. The goal of the game is to create chains of consecutive letters. The longer the chain, the better. The minimal chain should consists of 2 letters.

You can set your nickname by pressing **Settings** button. 

Top 10 highscores can be viewed on **Highscores** screen.

Enjoy the game :smiley:

Screenshots
-----------

<img src="http://i.imgur.com/FOtMEFy.png" width="300px"/>&nbsp;
<img src="http://i.imgur.com/i8XC27S.png" width="300px"/>
<img src="http://i.imgur.com/xsRdaa1.png" width="300px"/>&nbsp;
<img src="http://i.imgur.com/HXhSNzE.png" width="300px"/>
<img src="http://i.imgur.com/bopiJNO.png" width="300px"/>&nbsp;
<img src="http://i.imgur.com/2KvmfGq.png" width="300px"/>
<img src="http://i.imgur.com/gxS71pr.png" width="300px"/>&nbsp;
<img src="http://i.imgur.com/buOkgpI.png" width="300px"/>
