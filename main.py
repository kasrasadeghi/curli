#!/bin/python3
"""
This is a curl replacement for interactive use.

Features:
 - set a URL
 - set auth
 - cache a get request and mangle it

"""

import os
import json
import re
import pprint

import getpass
import requests

import json_table

LOADPATH = '/home/kasra/projects/curli/cache'

CACHE = ['URL', 'JSON']
URL = ''
JSON = ''

AUTH = None


def load():
    global URL
    global JSON
    if os.path.isfile(LOADPATH):
        with open(LOADPATH) as f:
            data = json.load(f)
    else:
        return f'load cache does not exist @ {loadpath}'

    success = []
    
    try:
        URL = data['URL']
        success += ['URL']
    except:
        pass

    try:
        JSON = data['JSON']
        success += ['JSON']
    except:
        pass
    
    return 'loaded ' + ", ".join(success) + ' from cache'


def save():
    with open(LOADPATH, 'w+') as f:
        json.dump({'URL': URL, 'JSON': JSON}, f)
    return 'saved ' + ", ".join(CACHE)


def auth():
    username = input("Username: ")
    password = getpass.getpass()
    AUTH = username, password
    return 'auth\'d ' + AUTH[0]


def get(url):
    global URL
    global JSON
    if not URL:
        return 'error: set URL first'
    if not AUTH:
        JSON = requests.get(URL + url, auth=AUTH).json()
    JSON = requests.get(URL + url).json()
    return JSON


def set_url(url):
    global URL
    if not re.search(r'://', url):
        URL = 'https://' + url
    else:
        URL = url
    return 'url set to ' + url


def before_space(string):
    try:
        key, rest = string.strip().split(' ', 1)
        return key, rest
    except ValueError:
        return string.strip(), ''


def evaluate(read):
    global URL
    key, rest = before_space(read)
    try:
        if key == 'set':
            return set_url(rest)
        if key == 'get':
            return get(rest)
        if key == 'auth':
            return auth()
        if key == 'load':
            return load()
        if key == 'save':
            return save()

        if key == 'table':
            return tablify(JSON)

        if key == 'url':
            return URL
        if key == 'json':
            return JSON
    except Exception as e:
        print(e)
    
 
def repl():
    while True:
        try:
            read = input(' > ')
        except EOFError:
            print()
            print(save())
            break
        response = evaluate(read)
        print(response)


def main():
    print(load())
    repl()

    
if __name__ == '__main__':
    main()
