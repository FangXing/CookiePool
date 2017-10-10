from flask import Flask,g
from db import *
from config import *
import json

app = Flask(__name__)

def get_conn():
    for name in GENERATOR_MAP:
        if not hasattr(g,name):
            setattr(g, name + '_account', AccountRedisClient(name=name))
            setattr(g,name+'_cookies',CookieRedisClient(name=name))

@app.route('/')
def index():
    return '<h2>welcome cookie pool</h2>'

@app.route('/<name>/random')
def random(name):
    get_conn()
    cookie = getattr(g,name + '_cookies').random()
    if cookie:
        return cookie
    else:
        return 'pool is empty'

@app.route('/<name>/add/<username>/<password>')
def add(name,username,password):
    get_conn()
    result =  getattr(g,name + '_account').set(username,password)
    return str(result)

@app.route('/<name>/count')
def count(name):
    get_conn()
    return str(getattr(g,name + '_cookies').count())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
