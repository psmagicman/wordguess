#! /usr/bin/env python3
# -*- coding: utf-8 -*-

class Error(Exception):
    """Generic Exception object for the game"""
    pass

class TokenError(Exception):
    """Exception raised for errors with the token

    Attributes:
        token -- token that caused error
        message -- explanation of the error
    """
    def __init__(self, token, message):
        self.token = token
        self.message = message

class DbError(Exception):
    """Exception raised for errors involving the database

    Attributes:
        values -- tuple containing the values in query
        message -- explanation of the error
    """
    def __init__(self, values, message):
        self.values = values
        self.message = message
        