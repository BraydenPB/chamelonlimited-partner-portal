from flask import Flask
from flask import Flask, request, jsonify
import requests
app = Flask(__name__)

@app.route('/')
def home():
    return 'Monday to wordpress data sync connector : Working'


import http.client
import json

@app.route('/api/cpt', methods=['POST'])
def cpt_post():
    product= request.form.get('product', 'product'),  # Default value is 'product'
    stage= request.form.get('stage', 'stage'),  # Default value is 'stage'
    parent_item_id= request.form.get('parent_item_id', 'parent_item_id'),  # Default value is 'parent_item_id'
    account_name= request.form.get('account_name', 'account_name'),  # Default value is 'account_name'
    deal_name= request.form.get('deal_name', 'deal_name'),  # Default value is 'deal_name'
    deal_date= request.form.get('deal_date', 'deal_date'),  # Default value is 'deal_date'
    email= request.form.get('newkey', 'deal_date'),  # Default value is 'deal_date'
    # deal_date= request.form.get('deal_date', 'deal_date'),  # Default value is 'deal_date'
    create= request.form.get('create', 'create'),  # Default value is 'deal_date'
    update= request.form.get('update', 'data'),  # Default value is 'deal_date'
       
    method='GET'    
    url = "https://time.webpath.agency/wp-json/wp/v2/account"

    payload = json.dumps({
    "title": f"{product[0]} {account_name[0]}",
    "status": "publish",
    "acf": {
        "product": product[0],
        "stage": stage[0],
        "parent_item_id": parent_item_id[0],
        "account_name": account_name[0],
        "deal_name": deal_name[0],
        "deal_date": deal_date[0]
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic V2ViUGF0aDpQOHVIIDZObUggbnFSOSA1OW1GIEdVVjIgVVlvcQ=='
    }
    status=""
    parent_item_id_wps=[]
    response = requests.request("GET", url, headers=headers, data=payload)
    for items in response.json():
        parent_item_id_wps.append(items['acf']['parent_item_id'])
    
    if parent_item_id[0] in parent_item_id_wps:
        method='POST'
        url = "https://time.webpath.agency/wp-json/wp/v2/account"
        
        response = requests.request("GET", url, headers=headers, data=payload)
        for items in response.json():
            parent_item_id_wp=items['acf']['parent_item_id']
            print(parent_item_id_wp,'parent_item_id_wp---------->')
            if parent_item_id_wp == parent_item_id[0]:
                item_id=items['id']
                print(item_id,'item_id------------------>')
                print('updated')
                try:
                    method="PUT" 
                    url = f"https://time.webpath.agency/wp-json/wp/v2/account/{item_id}"
                    status='updated'
                except:
                    pass
    else:
        method="POST"
        url = "https://time.webpath.agency/wp-json/wp/v2/account"
        print('created')
        status='created'
       
    response = requests.request(method, url, headers=headers, data=payload)
    print('method : ',method)
    print('status : ', status)
    print(response.text)
    
    return jsonify(response.json()) 

def delete_item(id):
    url = f"https://time.webpath.agency/wp-json/wp/v2/account/{id}"

    payload = {}
    headers = {
    'Authorization': 'Basic V2ViUGF0aDpQOHVIIDZObUggbnFSOSA1OW1GIEdVVjIgVVlvcQ=='
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)
    return jsonify(response.json())

@app.route('/api/update', methods=['POST'])
def updates():
    try:
        parent_item_id_wp=[]
        raw_data = request.form.get('ids')
        # print(raw_data ,'raw_data')
        item_ids=raw_data.replace(' ','').split(',')
        print(item_ids,'item_ids,in monday')
        method="PUT" 
        headers = {
        'Authorization': 'Basic V2ViUGF0aDpQOHVIIDZObUggbnFSOSA1OW1GIEdVVjIgVVlvcQ=='
        }    
        url = "https://time.webpath.agency/wp-json/wp/v2/account/"
        payload={}
        response = requests.request("GET", url, headers=headers, data=payload)
        for items in response.json():
            parent_item_id_wp.append(items['acf']['parent_item_id'])
        print(parent_item_id_wp,'parent_item_id_wp in wordpress')
        extra_in_parent_item_id_wp = list(set(parent_item_id_wp) - set(item_ids))

        print(extra_in_parent_item_id_wp,'extra_in_parent_item_id_wp')
        for items in response.json():
                parent_item_id_wp=items['acf']['parent_item_id']
            
                if parent_item_id_wp in extra_in_parent_item_id_wp:
                    item_id=items['id']
                    print(item_id,'item_id------------------>')
                    response=delete_item(item_id)
                    # break
        print(response)  
    except:
        print('Error Deleting Items')       
    # print(parent_item_id_wp,)            
    return jsonify('') 

if __name__ == '__main__':
    app.run(debug=True)
