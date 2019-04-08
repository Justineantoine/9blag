#!/usr/bin/env python3
# coding: utf-8

import json
from flask import Flask
from flask import abort, request, make_response
from flask import render_template, redirect, url_for

from data import USERS

# Set API dev in an another file
from api import SITE_API

app = Flask(__name__)
# Add the API
app.register_blueprint(SITE_API)

def fctSortDict(value):
    return value["dislike"]-value["like"]

@app.route('/')
def index(users=[u for u in USERS]):
    users_inv = []
    for i in range(1,len(users)+1):
        users_inv.append(users[-i])
    return render_template('index.html',users=users_inv)

@app.route('/indexapi')
def indexapi(users=[u for u in USERS]):
    return render_template('indexapi.html',users=sorted(users,key=fctSortDict))

@app.route('/search/', methods=['GET'])
def search():
    app.logger.debug(request.args)
    if "pattern" not in request.args:
        return abort(400)
    pattern = request.args.get("pattern")
    users = [u for u in USERS if pattern.lower() in u.get('tags').lower()]
    app.logger.debug(users)
    return render_template('index.html',pattern=pattern,users=users)

@app.route('/publish/', methods=['GET'])   
def publish():
    app.logger.debug(request.args)
    if ("url" not in request.args) or ("titre" not in request.args):
        return abort(400)
    url = request.args.get("url")
    titre = request.args.get("titre")
    tags = []
    if ("tags" in request.args):
        tags = request.args.get("tags").split(", ")
    users = [u for u in USERS]
    app.logger.debug(users)
    ajout = {'url': url, 'title': titre, 'tags': tags, 'like': 0, 'dislike': 0}
    users.append(ajout)
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump({"USERS":users}, f, indent=4)
    return index(users)
    


# Script starts here
if __name__ == '__main__':
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
