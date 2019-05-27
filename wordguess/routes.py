#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import random

from flask import Flask, jsonify, request, make_response

from wordguess.game.game import Game
from wordguess.common.connector import get_word_list
from wordguess.common.utils import decode_token, encode_word, DELIM, is_letter

app = Flask(__name__)

def request_to_response(data):
    return {
        'token': data['token'],
        'spaces': data['spaces'],
        'life': data['life'],
        'guesses': data['guesses']
    }

@app.route('/')
def start_game():
    word_list = get_word_list()
    game = Game(random.choice(word_list))
    response = {
        'spaces': ''.join(['_' for i in game.word]),
        'life': game.life,
        'guesses': ''.join([]),
        'token': encode_word(game.word, game.life).decode('utf-8')
    }
    return make_response(jsonify(response), 200)

@app.route('/api/v1/word', methods=['POST'])
def check_letter():
    data = request.get_json(force=True)
    decoded_word = decode_token(data['token'])
    print(decoded_word)
    word = decoded_word.split(DELIM)[0]
    life = int(decoded_word.split(DELIM)[1])
    game = Game(word, life)
    spaces = [i for i in data['spaces']]
    guesses = [i for i in data['guesses']]
    # handle case where no char
    if game.life == 0:
        # return lose condition
        return game_lost()
    if data['spaces'] == game.word:
        # return win condition
        return game_won()
    if 'char' not in data:
        data['message'] = 'No <char> in request body.'
        return make_response(jsonify(data), 400)
    if is_letter(data['char']):
        if data['char'] in guesses:
            data['message'] = ('You already entered this letter, please try again.')
        elif data['char'] not in guesses and game.is_in_word(data['char']):
            indicies = game.get_character_indicies(data['char'])
            for i in indicies:
                spaces[i] = game.word[i]
            guesses.append(data['char'])
        else:
            game.decrement_life()
            data['message'] = ('You have %s incorrect guesses remaining.' 
                    % game.life)
            guesses.append(data['char'])
            data['token'] = encode_word(game.word, game.life).decode('utf-8')
    else:
        data['message'] = ('You have entered <%s>, please try again.' 
                % data['char'])
    data['spaces'] = ''.join(spaces)
    data['life'] = game.life
    data['guesses'] = ''.join(guesses)
    data.pop('char', None)
    return make_response(jsonify(data), 200)

@app.route('/api/v1/lose')
def game_lost():
    data = {'message': 'You made too many incorrect guesses. Game over.'}
    return make_response(jsonify(data), 200)

@app.route('/api/v1/win')
def game_won():
    data = {'message': 'Congratulations, you won!'}
    return make_response(jsonify(data), 200)

@app.route('/api/v1/score', methods=['GET', 'POST'])
def save_score(score=None):
    pass