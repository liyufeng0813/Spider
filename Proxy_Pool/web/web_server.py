# !/usr/bin/python3
# -*- coding:utf-8 -*-

import json
import random

from flask import Flask, request

from db.mongo_helper import MongoHelper


app = Flask(__name__)

mongo = MongoHelper()


@app.route('/get_proxy/')
def get_proxy():
    try:
        count = int(request.args.get('count', 1))
    except ValueError:
        count = 1

    queryset = mongo.select()
    result_list = []
    for i in range(0, count):
        index = random.randrange(0, len(queryset))
        result_list.append(queryset.pop(index))

    return json.dumps(result_list)


@app.route('/delete_proxy/')
def delete_proxy():
    ip = request.args.get('ip', '')
    condition = {}
    try:
        condition['ip'] = ip.split(':')[0]
        condition['port'] = ip.split(':')[1]
    except IndexError:
        return json.dumps({"delete": "fail"})

    if condition:
        mongo.delete(condition)
        return json.dumps({"delete": "success"})
    return json.dumps({"delete": "fail"})


def start_server():
    app.run()


if __name__ == '__main__':
    app.run(debug=True)
