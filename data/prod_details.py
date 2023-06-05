from serpapi import GoogleSearch
import json
import csv
from pprint import pprint
import os
from pandas import *
 
# reading CSV file
data = read_csv("./output/output.csv")
ids= data['product_id'].tolist()[:100]


def search(id):
    params = {
        "engine": "home_depot_product",
        "product_id": id,
        "api_key": "e3ccf4734f3a657d208e0f77643d62eacd9d7166c273de8c109bb5d4afa8094a"
        }

    search = GoogleSearch(params)
    results = search.get_dict()
    product = {
        'alias': results['search_information'],
        'info': results['product_results']
    }
    return product

res = []
for id in ids:
    res.append(search(id))

with open('test.txt', 'a+', encoding='utf8') as f:
    f.write(json.dumps(res, indent=2, ensure_ascii=False))