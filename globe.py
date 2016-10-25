#!/usr/bin/env python3

import os
import sys
import json
import requests
import ntpath


home_directory = os.path.expanduser("~") + '/'
GLOBEFILE = home_directory + '.globe.json'

if not os.path.isfile(GLOBEFILE):
    if not len(sys.argv) == 2:
        print("Supply your Glot API key as the second argument\nHint: 'globe API_KEY'")
        exit(1)
    
    globe_json = open(GLOBEFILE, 'w+')

    apiKey = sys.argv[1]

    languages = []

    req = requests.get('https://run.glot.io/languages').json()

    for language in req:
        language_name_tmp = language['name']
        languages.append(language_name_tmp)

    data = {
        'apiKey': apiKey,
        'languages': languages,
    }
    
    data = json.dumps(data)
    globe_json.write(data)
    exit(0)


globe_json = open(GLOBEFILE)
globe_json = json.loads(globe_json.read())

api_token = globe_json['apiKey']


try:
    language = sys.argv[1]
except IndexError:
    print("No language given\nHint: 'globe LANGUAGE FILE'")
    exit(1)

if language not in globe_json['languages']:
    print("Language '{}' not supported...".format(language))
    exit(1)

try:
    file = sys.argv[2]
except IndexError:
    print("No file given.\nHint: 'globe {} FILE'".format(language))
    exit(1)

if not os.path.isfile(file):
    print("File '{}' does not exist.".format(file))
    exit(1)

payload = {
    'files': [
        {
            'name': ntpath.basename(file),
            'content': open(file).read()
        }
    ]
}

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token ' + api_token
}

result = requests.post('https://run.glot.io/languages/{}/latest'.format(language), headers=headers, json=payload).json()

if result['stdout'] != '':
    print('{}'.format(result['stdout']))

if result['stderr'] != '':
    print('stderr: {}'.format(result['stderr']))

if result['error'] != '':
    print('error: {}'.format(result['error']))