from serpapi import GoogleSearch
import json
import csv
from pprint import pprint
import os
# params = {
#     'api_key': '26d6fb297f43a809731e5d090a6369fcc22ce10a301f8d84f0b7a5e65a1d9389',    
#     'engine': 'home_depot_product',     
#     'q': 'coffe maker',  
#     'page': 1                
# }

# search = GoogleSearch(params)
# results = search.get_dict() 

# home_depot_results = {
#     'search_information': results['search_information'],
#     'filters': results['filters'],
#     'products': []
# }

# while 'error' not in results:
#     home_depot_results['products'].extend(results['products'])

#     params['page'] += 1
#     results = search.get_dict()


# print(json.dumps(home_depot_results, indent=2, ensure_ascii=False))

# with open('test.txt', 'a+', encoding='utf8') as f:
#     f.write(json.dumps(home_depot_results, indent=2, ensure_ascii=False))

# # Open the JSON file & load its data
# with open('data.json') as dat_file:
#     data = json.load(dat_file)
# prod_data = data['products']
 
def create_list_from_json(jsonfile):
    with open(jsonfile) as f:
        data = json.load(f)
        #print(data['products'][0])
    data_file = open('./output/output.csv', 'w') 
    csv_writer = csv.writer(data_file)

    csv_writer.writerow(['position','product_id','title',
                         'model_number','brand', 'collection', 
                         'favorite','rating','reviews',
                         'price','price_was','price_saving',
                         'percentage_off','price_badge','delivery',
                         'pickup','variants'])
    data_file.close()

    
      # create an empty list
    for i in data['products']:
        data_list = []
        # append the items to the list in the same order.
        data_list.append(i['position'])
        data_list.append(i['product_id'])
        data_list.append(i['title'])
        data_list.append(i['model_number'])
        if 'brand' in i:
            data_list.append(i['brand'])
        else:
            data_list.append('')
        data_list.append(i['collection'])
        if 'favorite' in i:
            data_list.append(i['favorite'])
        else:
            data_list.append('')
        data_list.append(i['rating'])
        if 'reviews' in i:
            data_list.append(i['reviews'])
        else:
            data_list.append('')
        data_list.append(i['price'])
        if 'price_was' in i:
            data_list.append(i['price_was'])
        else:
            data_list.append('')
        if 'price_saving' in i:
            data_list.append(i['price_saving'])
        else:
            data_list.append('')
        if 'percentage_off' in i:
            data_list.append(i['percentage_off'])
        else:
            data_list.append('')
        if 'price_badge' in i:
            data_list.append(i['price_badge'])
        else:
            data_list.append('')

        if 'delivery' in i:
            data_list.append(i['delivery'])  
        else:
            data_list.append('')

        if 'pickup' in i:
            data_list.append(i['pickup'])
        else:
            data_list.append('')
        
        if 'variants' in i:
            data_list.append(i['variants'])  
        else:
            data_list.append('')
            
      
        with open('./output/output.csv', 'a') as c:
                writer = csv.writer(c)
                writer.writerow(data_list)
        c.close()


def create_prod_from_json(jsonfile):
    with open(jsonfile) as f:
        data = json.load(f)
        #print(data['products'][0])
    data_file = open('./output/prods.csv', 'w') 
    csv_writer = csv.writer(data_file)

    csv_writer.writerow(['taxonomy','product_id','title','link',
                         'description','model_number',
                         'favorite','rating','reviews',
                         'price','promotion',
                         'highlights', 'brand', 'bullets', 'specifications',
                         'countity','store','deliver options'])
    data_file.close()

    
      # create an empty list
    for i in data:
        data_list = []
        # append the items to the list in the same order.
        taxonomy = ''
        for t in i['alias']['taxonomy']:
            taxonomy+=t['title']
            taxonomy+=','
        data_list.append(taxonomy)

        data_list.append(i['info']['product_id'])
        data_list.append(i['info']['title'])
        data_list.append(i['info']['link'])
        data_list.append(i['info']['description'])
        data_list.append(i['info']['model_number'])

        if 'favorite' in i['info']:
            data_list.append(i['info']['favorite'])
        else:
            data_list.append('')

        if 'rating' in i['info']:
            data_list.append(i['info']['rating'])
        else:
            data_list.append('')

        if 'reviews' in i['info']:
            data_list.append(i['info']['reviews'])
        else:
            data_list.append('')

        data_list.append(i['info']['price'])

        if 'promotion' in i['info']:
            data_list.append(i['info']['promotion'])
        else:
            data_list.append('')
           
        if 'highlights' in i['info']:
            data_list.append(i['info']['highlights'])
        else:
            data_list.append('')
        
        if 'brand' in i['info']:
            data_list.append(i['info']['brand']['name'])
        else:
            data_list.append('')

        if 'bullets' in i['info']:
            data_list.append(i['info']['bullets'])
        else:
            data_list.append('')

        data_list.append(i['info']['specifications'])

        if 'fulfillment' in i['info']:
            if 'countity' in i['info']['fulfillment']:
                data_list.append(i['info']['fulfillment']['countity'])
            else:
                data_list.append('')
            if 'store' in i['info']['fulfillment']:
                data_list.append(i['info']['fulfillment']['store'])
            else:
                data_list.append('')
            if 'options' in i['info']['fulfillment']:
                data_list.append(i['info']['fulfillment']['options'])
            else:
                data_list.append('')
        else:
            data_list.append('')
            data_list.append('')
            data_list.append('')
            

      
        with open('./output/prods.csv', 'a') as c:
                writer = csv.writer(c)
                writer.writerow(data_list)
        c.close()

create_prod_from_json('./output/prod_details.json')