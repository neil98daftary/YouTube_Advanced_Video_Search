#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 09:57:42 2020

@author: mana
"""

from flask import Flask, request, jsonify
from utils import *

app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello():
    if "key" in request.args:
        keywords = request.args["key"]
        keywords = keywords.lstrip('[')
        keywords = keywords.rstrip(']')
        keywords = keywords.split(",")
        if "order" in request.args:
            order = request.args["order"]
        else:
            order = "relevance"
            
        return(loop(keywords, order))
    else:
        return 'Hello World!'


if __name__ == '__main__':
    app.run()