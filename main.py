"""
This is a curl replacement for interactive use.

Features:
 - set a URL
 - set auth
 - cache a get request and mangle it

"""

import getpass
import requests
import os
import json
import re

LOADPATH = '/home/kasra/projects/kurl/cache'
URL = ''
AUTH = None


def load():
    if os.path.isfile(LOADPATH):
        with open(LOADPATH) as f:
            data = json.load(f)
    else:
        return f'load cache does not exist @ {loadpath}'
    URL = data['URL']
    return 'loaded cache'


def auth():
    username = input("Username: ")
    password = getpass.getpass()
    AUTH = username, password
    return 'auth\'d ' + AUTH[0]


def get(url):
    if not URL:
        return 'error: set URL first'
    if not AUTH:
        return requests.get(URL + rest, auth=AUTH).text
    return requests.get(ULR + rest).text


def set_url(url):
    if not re.find(r'://'):
        url = 'https://' + url
    URL = url
    return 'url set to ' + url


def save():
    with open(LOADPATH, 'w') as f:
        json.dump(f, {'URL': URL})
    return 'saved url'


def evaluate(read):
    global URL
    key, rest = read.strip().split(' ', 1)
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
    
    
def repl():
    while True:
        try:
            read = input(' > ')
        except EOFError:
            print()
            break
        response = evaluate(read)
        print(response)

        
def main():
    repl()

    
if __name__ == '__main__':
    main()
