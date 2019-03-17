# -*- coding: utf-8 -*-


from flask import Flask, jsonify
from flask import request
import ast
import json

app = Flask(__name__)
counts = 0


@app.route('/')
def hello():
    return "Hello, World!"


@app.route('/method', methods=['GET', 'POST', 'PUT', 'DELETE'])
def request_method():
    return f'{request.method}'


@app.route('/show_data', methods=['POST'])
def post_json():
    assert request.is_json == True, "Pass json data"
    content = request.data
    content = str(content, 'utf-8')
    return f'{content}'

@app.route('/pretty_print_name', methods=['POST'])
def pretty_name():
    content = request.get_json()
    assert "name" in content, "Lack of required key"
    assert "surename" in content, "Lack of required key"
    return f'Na imię mu {content["name"]}, a nazwisko jego {content["surename"]}'


@app.route('/counter')
def counter():
    global counts
    counts = counts + 1
    return str(counts)


if __name__ == '__main__':
    app.run(debug=True)
