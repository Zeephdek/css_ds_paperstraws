import json
import time
import os
import re

def json_beautify(data):
    return json.dumps(data, indent=4, sort_keys=True)

def clear():
    os.system('cls')

