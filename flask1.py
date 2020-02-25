#! /usr/bin/env python2
#
from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    name = request.args.get("name", "World")
    # return f'Hello, {escape(name)}'
    return "Hello, {0}\n".format(name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)


