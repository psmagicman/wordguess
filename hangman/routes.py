#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time

from flask import Flask, jsonify, request, make_response, render_template
from flask_cors import CORS

import hangman.game.game as game
import hangman.game.scoreboard as scoreboard
from hangman.common.connector import get_word_list, db_file_exists
import hangman.common.utils as utils
from hangman.common.exceptions import TokenError, DbError
import hangman.common.messages as alerts

if not db_file_exists():
    print("No db file found, please set it up and try again.")
    exit(1)

app = Flask(__name__)
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})

game_status = {
    'start': 0,
    'progress': 1,
    'lose': 2,
    'win': 3,
}

def message_to_dict(message):
    # format is word|life|spaces|secs|status|guesses
    m = message.split(utils.DELIM)
    return {
        'word': m[0],
        'life': int(m[1]),
        'spaces': [i for i in m[2]],
        'start_time': float(m[3]),
        'status': int(m[4]),
        'guesses': [i for i in m[5]]
    }

def tokenize_message(gs):
    life = str(gs['life'])
    spaces = ''.join(gs['spaces'])
    guesses = ''.join(gs['guesses'])
    start = str(gs['start_time'])
    status = str(gs['status'])
    message = utils.create_message(gs['word'], life, 
            spaces, start, status, guesses)
    return utils.encode_message(message).decode('utf-8')

def add_to_response(res, gs):
    res['life'] = gs['life']
    res['spaces'] = ''.join(gs['spaces'])
    res['guesses'] = ''.join(gs['guesses'])
    return res

def game_lost(gs):
    res = {'alert': alerts.LOSE_MESSAGE, 
           'status': game_status['lose']}
    res = add_to_response(res, gs)
    return make_response(jsonify(res), 200)

def game_won(gs):
    res = {'alert': alerts.WIN_MESSAGE + ' [SCORE: %s]' % gs['life'], 
           'status': game_status['win']}
    message = utils.create_message(gs['life'], time.time())
    res['stoken'] = utils.encode_message(message).decode('utf-8')
    res = add_to_response(res, gs)
    return make_response(jsonify(res), 200)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/start')
def start_game():
    word_list = get_word_list()
    word = random.choice(word_list)
    life = 5
    spaces = ''.join(['_' for i in word])
    guesses = ''.join([])
    status = game_status['start']
    # start time included in message so tokens aren't the same for each word
    message = utils.create_message(word, life, spaces, 
            time.time(), status, guesses)
    response = {
        'spaces': spaces,
        'life': life,
        'guesses': guesses,
        'token': utils.encode_message(message).decode('utf-8'),
        'status': status,
        'alert': '',
    }
    return make_response(jsonify(response), 200)

@app.route('/api/v1/word', methods=['POST'])
def check_letter():
    req = request.get_json(force=True)
    res = {'status': game_status['progress']}
    decoded_message = None
    try:
        decoded_message = utils.decode_token(req['token'])
    except TokenError as e:
        res['alert'] = e.message
        return make_response(jsonify(res), 400)
    except KeyError as e:
        res['alert'] = alerts.NO_TOKEN
        return make_response(jsonify(res), 400)
    # game state
    gs = message_to_dict(decoded_message)
    if 'char' not in req or 'token' not in req:
        res['alert'] = alerts.MISSING_CHAR_TOKEN
        return make_response(jsonify(res), 400)
    if req['token'] == '':
        res['alert'] = alerts.ALPHANUMERIC_ONLY
        res = add_to_response(res, gs)
        return make_response(jsonify(res), 400)
    if len(req['char']) != 1:
        res['alert'] = alerts.ALPHANUMERIC_ONLY
        res['token'] = req['token']
        res = add_to_response(res, gs)
        return make_response(jsonify(res), 400)

    if utils.is_letter(req['char']):
        if req['char'] in gs['guesses']:
            res['alert'] = alerts.DUPLICATE_CHAR
            res['token'] = req['token']
            res = add_to_response(res, gs)
            return make_response(jsonify(res), 200)
        elif req['char'] not in gs['guesses'] and req['char'] in gs['word']:
            indicies = game.get_character_indicies(gs['word'], req['char'])
            for i in indicies:
                gs['spaces'][i] = gs['word'][i]
            gs['guesses'].append(req['char'])
        else:
            if gs['life'] < 1:
                game_lost(gs)
            gs['life'] -= 1
            res['alert'] = alerts.INCORRECT
            gs['guesses'].append(req['char'])
        res['token'] = tokenize_message(gs)
    else:
        res['alert'] = alerts.ALPHANUMERIC_ONLY

    if gs['life'] < 1:
        return game_lost(gs)
    spaces_word = ''.join(gs['spaces'])
    if spaces_word == gs['word']:
        return game_won(gs)
    res = add_to_response(res, gs)
    return make_response(jsonify(res), 200)

@app.route('/api/v1/score', methods=['POST'])
def score():
    req = request.get_json(force=True)
    res = {}
    if 'name' not in req or 'stoken' not in req:
        res['alert'] = alerts.MISSING_NAME_TOKEN
        return make_response(jsonify(res), 400)
    try:
        decoded_message = utils.decode_token(req['stoken'])
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