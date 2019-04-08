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


@app.route('/hello_world', methods=['GET','POST'])
def hello_world():
    app.logger.debug('Hello world')
    resp = make_response('Hello, World!',200)
    resp.headers['X-Something'] = 'A value'
    resp.headers["Content-Type"] = "text"
    #resp.headers["Accept-Language"] = "en_US", "en_EN", "fr_FR"
    resp.headers["Content-Language"] = "en_US"
    user = {'username': 'Lauren'}
    render_template('index.html', title='Home', user=user)
    return resp

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
    return render_template('about.html', page_title="About")


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/users/')
@app.route('/users/<username>/')
def users(username=None):
    if not username:
        return render_template('users.html',users=USERS)
    abort(404)
    return render_template('users.html',users=USERS)

@app.route('/search/', methods=['GET'])
def search():
    app.logger.debug(request.args)
    #abort(make_response('Not implemented yet ;)', 501))
    if "pattern" not in request.args:
        return abort(400)
    pattern = request.args.get("pattern")
    usrs = [u for u in USERS if pattern.lower() in u.get('name').lower()]
    app.logger.debug(usrs)
    return render_template('users.html',pattern=pattern,users=usrs)

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
