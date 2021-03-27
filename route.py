import bmr
import json

def hello_world():
    return json.dumps(bmr.i_index)


def name(name):
    return "Hello, "+name