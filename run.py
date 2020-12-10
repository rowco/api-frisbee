#! /usr/bin/env python

import sys,os,re

import random
import time
import logging

from flask import Flask, current_app, render_template, \
     request, session, flash, redirect, url_for, jsonify

import api_frisbee.main

api_frisbee.main.setup_logging()
logger = logging.getLogger('api-frisbee.run')
app = Flask(__name__)

@app.route("/",methods=['get','post'])
def home():
    if request.method == 'POST':
        post = request.get_json()
        if 'targets' in post:
            frisbee = api_frisbee.main.start_frisbee(post['targets'])
            return jsonify(frisbee.id)
    return jsonify({})

@app.route("/catch",methods=['post'])
def catch():
    if request.method == 'POST':
        post = request.get_json()
        if 'targets' in post:
            frisbee = api_frisbee.main.catch_frisbee(post,request=request)
            return jsonify(dict(frisbee))
    return jsonify({})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=sys.argv[1],debug=True)