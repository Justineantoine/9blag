#!/usr/bin/env python3
# coding: utf-8

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
def index():
    return render_template('index.html',users=USERS)

#@app.route('/tendance/')
#def tendance(username=None):
#    return render_template('index.html',users=sorted(USERS,key=fctSortDict))

@app.route('/indexapi')
def indexapi():
    return render_template('indexapi.html',users=sorted(USERS,key=fctSortDict))

@app.route('/search/', methods=['GET'])
def search():
    app.logger.debug(request.args)
    #abort(make_response('Not implemented yet ;)', 501))
    if "pattern" not in request.args:
        return abort(400)
    pattern = request.args.get("pattern")
    usrs = [u for u in USERS if pattern.lower() in u.get('tags').lower()]
    app.logger.debug(usrs)
    return render_template('index.html',pattern=pattern,users=usrs)

'''def deal_with_post():
    form = request.form
    app.logger.debug('Hey')'''

@app.route('/test', methods=['GET','POST'])
def test():
    '''app.logger.debug('Running')
    app.logger.debug('client'.format(request.method))
    if request.method == 'POST':
        return deal_with_post()'''

# Script starts here
if __name__ == '__main__':
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
