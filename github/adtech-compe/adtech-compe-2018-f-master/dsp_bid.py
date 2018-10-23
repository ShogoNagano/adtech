#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''API for DSP
'''

from flask import Flask, request, jsonify, json
# import requests
import redis


app = Flask(__name__)

# constants
nurl_url = "http://35.200.55.101:3000/"
budget_dict = {}
r = redis.StrictRedis(host='10.0.0.3', port='6379', db=0)
adv_list = ["adv01",
            "adv02",
            "adv03",
            "adv04",
            "adv05",
            "adv06",
            "adv07",
            "adv08",
            "adv09",
            "adv10",
            "adv11",
            "adv12",
            "adv13",
            "adv14",
            "adv15",
            "adv16",
            "adv17",
            "adv18",
            "adv19",
            "adv20",
            ]


def pred_price(data_dict):
    '''return price
    '''
    # print(data_dict)
    return data_dict['floorPrice'] + 100000
#
#
# def dec_budget(user):
#     '''decrease budget for user
#     '''
#     if user in budget_dict.keys():
#         budget_dict[user]['budget'] = budget_dict[user]['budget'] - budget_dict[user]['cpc']
#         print(budget_dict)


# @app.route('/budget', methods=['POST'])
# def change_budget():
#     if request.headers['Content-Type'] != "application/json":
#         return '', 400
#     budget_ad = request.data.decode('utf-8')
#     budget_ad = json.loads(budget_ad)
#     print(budget_ad)
#     dec_budget(budget_ad['user'])
#     return '', 200


@app.route('/', methods=['POST'])
def dsp_bid():
    # format data
    #if request.headers['Content-Type'] != "application/json":
    #    return '', 400
    data_r = request.data.decode('utf-8')
    data_dict = json.loads(data_r)
    data_dict['floorPrice'] = float(data_dict['floorPrice'])
    data_dict['timestamp'] = int(data_dict['timestamp'])
    data_dict['bannerSize'] = int(data_dict['bannerSize'])
    data_dict['bannerPosition'] = int(data_dict['bannerPosition'])
    if 'deviceType' in data_dict.keys():
        data_dict['deviceType'] = int(data_dict['deviceType'])
    else:
        data_dict['deviceType'] = int(data_dict['deviceToken'])
        data_dict.pop('deviceToken')

    # get budget
    budget_dict = {}
    for user in adv_list:
        budget_dict[user] = r.hget(user, 'budget')
    # print(budget_dict)
    price = pred_price(data_dict)
    if price == -1:
        return '', 204
    else:
        response = jsonify({
            "id": data_dict['id'],
            "bidPrice": price,
            "advertiserId": "adv01",
            "nurl": nurl_url + "win/adv01"})
        response.status_code = 200
        return response


# @app.route('/', methods=['GET'])
# def health_check():
#    return "Hello World!"


if __name__ == '__main__':
    # get_budget
    # budget_dict = requests.get(nurl_url + "/budget").json()
    # print(budget_dict)
    # run app
    #app.run(host='0.0.0.0', port=3000, processes=8, threaded=False)
    app.run()
