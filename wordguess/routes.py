#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time

from flask import Flask, jsonify, request, make_response

import wordguess.game.game as game
import wordguess.game.scoreboard as scoreboard
from wordguess.common.connector import get_word_list
import wordguess.common.utils as utils
from wordguess.common.exceptions import TokenError, DbError

app = Flask(__name__)

def message_to_dict(message):
    # format is word|life|spaces|secs|guesses
    m = message.split(utils.DELIM)
    return {
        'word': m[0],
        'life': int(m[1]),
        'spaces': [i for i in m[2]],
        'start_time': float(m[3]),
        'guesses': [i for i in m[4]]
    }

def tokenize_message(gs):
    life = str(gs['life'])
    spaces = ''.join(gs['spaces'])
    guesses = ''.join(gs['guesses'])
    st = str(gs['start_time'])
    message = utils.create_message(gs['word'], life, spaces, st, guesses)
    return utils.encode_message(message).decode('utf-8')

def add_to_response(res, gs):
    res['life'] = gs['life']
    res['spaces'] = ''.join(gs['spaces'])
    res['guesses'] = ''.join(gs['guesses'])
    return res

def game_lost():
    res = {'alert': 'You made too many incorrect guesses. Game over.'}
    return make_response(jsonify(res), 200)

def game_won(gs):
    res = {'alert': 'Congratulations, you won!'}
    message = utils.create_message(gs['life'], time.time())
    res['token'] = utils.encode_message(message).decode('utf-8')
    res = add_to_response(res, gs)
    return make_response(jsonify(res), 200)

@app.route('/')
def start_game():
    word_list = get_word_list()
    word = random.choice(word_list)
    life = 5
    spaces = ''.join(['_' for i in word])
    guesses = ''.join([])
    # start time included in message so tokens aren't the same for each word
    message = utils.create_message(word, life, spaces, time.time(), guesses)
    response = {
        'spaces': spaces,
        'life': life,
        'guesses': guesses,
        'token': utils.encode_message(message).decode('utf-8')
    }
    return make_response(jsonify(response), 200)

@app.route('/api/v1/word', methods=['POST'])
def check_letter():
    req = request.get_json(force=True)
    res = {}
    decoded_message = None
    try:
        decoded_message = utils.decode_token(req['token'])
    except TokenError as e:
        res['alert'] = e.message
        return make_response(jsonify(res), 400)
    # game state
    gs = message_to_dict(decoded_message)
    if 'char' not in req or 'token' not in req:
        res['alert'] = 'No <char> or <token> in request body.'
        return make_response(jsonify(res), 400)
    if len(req['char']) != 1:
        res['alert'] = 'Please enter a single alphanumeric character.'
        res['token'] = req['token']
        res = add_to_response(res, gs)
        return make_response(jsonify(res), 400)
    if utils.is_letter(req['char']):
        if req['char'] in gs['guesses']:
            res['alert'] = ('You already entered this letter, please try again.')
            res['token'] = req['token']
            res = add_to_response(res, gs)
            return make_response(jsonify(res), 200)
        elif req['char'] not in gs['guesses'] and req['char'] in gs['word']:
            indicies = game.get_character_indicies(gs['word'], req['char'])
            for i in indicies:
                gs['spaces'][i] = gs['word'][i]
            gs['guesses'].append(req['char'])
        else:
            if gs['life'] <= 0:
                game_lost()
            gs['life'] -= 1
            res['alert'] = ('You have %s incorrect guesses remaining.' 
                    % gs['life'])
            gs['guesses'].append(req['char'])
        res['token'] = tokenize_message(gs)
    else:
        res['alert'] = ('You have entered invalid char <%s>, please try again.' 
                % req['char'])
    if gs['life'] < 0:
        return game_lost()
    spaces_word = ''.join(gs['spaces'])
    if spaces_word == gs['word']:
        return game_won(gs)
    res = add_to_response(res, gs)
    return make_response(jsonify(res), 200)

@app.route('/api/v1/score', methods=['POST'])
def score():
    req = request.get_json(force=True)
    res = {}
    if 'name' not in req or 'token' not in req:
        res['alert'] = 'No <name> or <token> in request body.'
        return make_response(jsonify(res), 400)
    try:
        decoded_message = utils.decode_token(req['token'])
        m = decoded_message.split(utils.DELIM)
        res['score'] = int(m[0])
    except TokenError as e:
        res['alert'] = e.message
        return make_response(jsonify(res), 400)
    try:
        scoreboard.save_to_db(req['name'], res['score'])
        res['name'] = req['name']
    except DbError as e:
        res = {'alert': e.message}
        return make_response(jsonify(res), 500)
    return make_response(jsonify(res), 201)