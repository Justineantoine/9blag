#!/usr/bin/env python3
# coding: utf-8

import json
from flask import Flask
from flask import abort, request, make_response
from flask import render_template, redirect, url_for

from data import IMAGES

# Set API dev in an another file
from api import SITE_API

app = Flask(__name__)
# Add the API
app.register_blueprint(SITE_API)

images=[u for u in IMAGES]


def fctSortDict(value):
    return value["dislike"]-value["like"]

@app.route('/')
def latest():
    images_inv = []
    for i in range(1,len(images)+1):
        images_inv.append(images[-i])
    return render_template('latest.html',images=images_inv)

@app.route('/trending')
def trending():
    return render_template('trending.html',images=sorted(images,key=fctSortDict))

@app.route('/search/', methods=['GET'])
def search():
    app.logger.debug(request.args)
    if "pattern" not in request.args:
        return abort(400)
    pattern = request.args.get("pattern")
    images_sorted_tag = [u for u in images if pattern in u["tags"]]
    app.logger.debug(images_sorted_tag)
    return render_template('latest.html',pattern=pattern,images=images_sorted_tag)

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
    n = len(images)
    ajout = {'id': n, 'url': url, 'title': titre, 'tags': tags, 'like': 0, 'dislike': 0}
    images.append(ajout)
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump({"IMAGES":images}, f, indent=4)
    return latest()

#BOUTONS J'AIME/J'AIME PAS POUR LA PAGE FRAIS
@app.route('/like_l/', methods=['GET'])  
def like_latest():
    ID = int(request.args.get("ID"))
    img = images[ID]
    img['like'] += 1
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump({"IMAGES":images}, f, indent=4)
    return latest()
    
@app.route('/dislike_l/', methods=['GET'])  
def dislike_latest():
    ID = int(request.args.get("ID"))
    img = images[ID]
    img['dislike'] += 1
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump({"IMAGES":images}, f, indent=4)
    return latest()


#BOUTONS J'AIME/J'AIME PAS POUR LA PAGE TRENDING
@app.route('/like_t/', methods=['GET'])  
def like_trend():
    ID = int(request.args.get("ID"))
    img = images[ID]
    img['like'] += 1
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump({"IMAGES":images}, f, indent=4)
    return trending()

@app.route('/dislike_t/', methods=['GET'])  
def dislike_trend():
    ID = int(request.args.get("ID"))
    img = images[ID]
    img['dislike'] += 1
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump({"IMAGES":images}, f, indent=4)
    return trending()
    
    
# Script starts here
if __name__ == '__main__':
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
