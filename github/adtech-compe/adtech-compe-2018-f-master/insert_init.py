#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''insert budget data to redis
'''

import redis
import json


if __name__ == '__main__':
    r = redis.StrictRedis(host='10.0.0.3', port='6379', db=0)
    budget_f = open("./cpc_budget.json")
    budget_dict = json.load(budget_f)
    for key, value in budget_dict.items():
        r.hmset(key, value)
    print(r.hget('adv01', 'budget'))
