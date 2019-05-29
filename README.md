Hangman Game
=====
Just a simple hangman game

python version 3.7.3
sqlite3 version 3.24.0 2018-06-04 14:10:15 95fbac39baaab1c3a84fdfc82ccb7f42398b2e92f18a2a57bce1d4a713cbaapl

##Installation

Running the following commands in the order presented will setup the environment

```
virtualenv --python=python3 ENV
source ENV/bin/activate
pip install -r requirements.txt
python install_db.py
```

Please run the `install_db.py` script to initialize the database. Both the server and command line game will immediately exit otherwise.

To install the frontend, please run the `install_frontend.sh` script. 

##Playing

To play in the command line, please execute `./start cmd` in the `bin` directory.

To start the server, please execute `./start server` in the `bin` directory.

The cmd version of the game uses the same database as the UI version of the game though it does not require the server to be running to play.

To play on the browser please start the server and navigate to the root path (ie. `http://localhost:5000/`).

