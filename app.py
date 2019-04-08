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


@app.route('/hello_world')
def hello_world():
    app.logger.debug('Hello world')
    return 'Hello, World!', 200


@app.route('/')
def index():
    app.logger.debug('serving root URL /')
    return render_template('index.html')


@app.route('/indexapi')
def indexapi():
    return render_template('indexapi.html')


@app.route('/about')
def about():
    app.logger.debug('about')
    return render_template('about.html')


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/users/')
@app.route('/users/<username>/')
def users(username=None):
    if not username:
        return render_template('users.html')
    abort(404)


@app.route('/search/', methods=['GET'])
def search():
    app.logger.debug(request.args)
    abort(make_response('Not implemented yet ;)', 501))


# Script starts here
if __name__ == '__main__':
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
