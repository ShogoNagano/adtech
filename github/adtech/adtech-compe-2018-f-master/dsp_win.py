#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''API for WIN
'''

from flask import Flask, request, json  # , jsonify
# import requests
# import json as jsond
from werkzeug.routing import BaseConverter
import redis


r = redis.StrictRedis(host='10.0.0.3', port='6379', db=0)
app = Flask(__name__)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


# budget_dict = {}
# server_list = ["http://35.221.95.73:3001",
#                "http://35.200.43.183:3001",
#                "http://35.221.105.45:3001"]


# @app.route('/budget', methods=['GET'])
# def get_budget():
#     response = jsonify(budget_dict)
#     response.status_code = 200
#     return response


# def sync_budget(user):
#     '''send change of budget to all server
#     '''
#     for serv in server_list:
#         url = serv + "/budget"
#         headers = {"Content-Type": "application/json"}
#
#         obj = {"user": user}
#         json_data = json.dumps(obj).encode('utf-8')
#         result = requests.post(url, json_data, headers=headers)
#         print(result.text)


@app.route('/win/<regex("[0-9a-zA-Z]*"):user>', methods=['POST'])
def dsp_bid(user):
    # format data
    if request.headers['Content-Type'] != "application/json":
        return '', 400
    data_r = request.data.decode('utf-8')
    data_dict = json.loads(data_r)
    data_dict['price'] = float(data_dict['price']) * 1000
    data_dict['isClick'] = int(data_dict['isClick'])
    print(data_dict)
    print(user)
    r.hset(user, 'budget', float(r.hget(user, 'budget').decode('utf-8')) - float(data_dict['isClick']) * float(r.hget(user, 'cpc').decode('utf-8')))
    print(r.hget(user, 'budget'))

    return '', 204


if __name__ == '__main__':
    # get budget info
    # budget_f = open("./cpc_budget.json", "r")
    # budget_dict = jsond.load(budget_f)
    # print(budget_dict)
    # run app
    app.run(host='0.0.0.0', port=3000, processes=16, threaded=False)
