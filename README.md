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
```

Please run the `setup.py` script to initialize the database. Both the server and command line game will immediately exit otherwise.

##Playing

To play in the command line, please execute `./start cmd` in the `bin` directory.

To start the server, please execute `./start server` in the `bin` directory.

The cmd version of the game uses the same database as the UI version of the game though it does not require the server to be running to play.

Since the frontend UI is not complete yet, the game can only be played using the command line version or by using `curl` against the framework agnostic API server. 

To play using `curl` commands, you will need to record the `token` in the response body every single time a request is made. Due to this, cheating is still entirely possible by making multiple requests using the exact same token.

Flow is as follows:


```
1. curl -H "Content-Type: application/json" \ 
		http://localhost:5000/api/v1/start
2. curl -H "Content-Type: application/json" \
		-X POST \
		--data '{"char": "x", "token": "PREVIOUS_TOKEN"}'
		http://localhost:5000/api/v1/word
3. Repeat step 2 until win/lose condition met
4. New token generated if win condition is met
5. curl -H "Content-Type: application/json" \
		-X POST \
		--data '{"name": "NAME", "token": "PREVIOUS_TOKEN"}' \
		http://localhost:5000/api/v1/score
```


##Todo

The frontend is still a WIP. It isn't entirely functional yet. The code can be inspected by checking the `frontend` branch and installing the relevant node modules. 
