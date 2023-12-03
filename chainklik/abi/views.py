from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import AbiForm

from datetime import datetime
import hashlib
import json
import web3
import re
import requests

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

# local modules
import libs.common.etherscan as etherscan
import libs.common.payload as payload
import config.config as cfg
import eth_abi

es = Elasticsearch("https://localhost:9200",http_auth=('elastic', 'y=fUp=8ucKL18I5K=1Am'),verify_certs=False)
w3 = web3.Web3(web3.Web3.HTTPProvider(cfg.config["http_url"]))


def add_contract_abi(contract_addr, impl_addr, contract_name, author = "rshi"):
    def doc_id(contract_addr, abi):
        return hashlib.md5('{}/{}'.format(contract_addr,str(abi)).encode()).hexdigest()
    # if contract addr is different from impl addr
    pool_contract = etherscan.get_contract(contract_addr,impl_addr)
    # save contract abi
    doc = {
        'author': 'rshi',
        'timestamp': datetime.now(),
        'id' : doc_id(contract_addr, pool_contract.abi),
        'address' : contract_addr,
        'contract' : contract_name,
        'type' : "contract",
        'name' : contract_name,
        'abi': pool_contract.abi
    }
    res = []
    resp = es.index(index='abi', id=doc['id'], document=doc)
    res.append(resp)
    
    # save contract function and event abi
    for abi in pool_contract.abi:
        if abi["type"] != "constructor":
            doc = {
                'author': 'rshi',
                'timestamp': datetime.now(),
                'id' : doc_id(contract_addr, abi),
                'address' : contract_addr,
                'contract' : contract_name,
                'type' : abi["type"],
                'name' : abi["name"],
                'abi': abi
            }
            if abi["type"] == "function":
                doc["stateMutability"] = abi["stateMutability"]
            
            resp = es.index(index='abi', id=doc['id'], document=doc)
            res.append(resp)
    return res

def index(request):
    return HttpResponse("Hello, world. You're at the abi index.")
  
def contract_abi(request, contract_address):
    index_name = 'abi'
    s = Search(using=es, index=index_name)
    query = Q('bool',
        must=[
            Q('match', address=contract_address),  # Match on field1 with value1
            Q('match', type='contract')   # Match on field2 with value2
        ]
    )
    s = s.query(query)
    
    response = s.execute()
    data = json.dumps(response.to_dict()["hits"]["hits"][0])
    return HttpResponse(data, content_type='application/json')
  
def function_abi(request, contract_address, function_name):
    index_name = 'abi'
    s = Search(using=es, index=index_name)
    query = Q('bool',
        must=[
            Q('match', address=contract_address),
            Q('match', type='function'), 
            Q('match', name=function_name)
        ]
    )
    s = s.query(query)
    
    response = s.execute()
    data = json.dumps(response.to_dict()["hits"]["hits"][0])
    return HttpResponse(data, content_type='application/json')
  
def event_abi(request, contract_address, event_name):
    data = json.dumps({"contract_address":contract_address,"event":event_name})
    return HttpResponse(data, content_type='application/json')
  
def add_abi(request):
    success_message = ""
    error_message = ""
    if request.method == 'POST':
        # If the form has been submitted, process the data
        form = AbiForm(request.POST)
        if form.is_valid():
            # Form data is valid, perform actions with the data
            contract_addr = form.cleaned_data['contract_address']
            impl_addr = form.cleaned_data['impl_address']
            contract_name = form.cleaned_data['contract_name']
            res = add_contract_abi(contract_addr, impl_addr, contract_name)
            success_message = f"success {res}"
        else:
            error_message = "Form submission failed. Please check the errors below."
    else:
        # If this is a GET request, create a new form
        form = AbiForm()

    return render(request, 'abi/add_abi_template.html', {'form': form, 'success_message': success_message, 'error_message': error_message})

@csrf_exempt
def call_abi(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        contract_address = data["contract"]
        function_name = data["name"]
        params = data["params"]
        print(params)
        # get function abi
        index_name = 'abi'
        s = Search(using=es, index=index_name)
        query = Q('bool',
            must=[
                Q('match', address=contract_address),
                Q('match', type='function'), 
                Q('match', name=function_name)
            ]
        )
        s = s.query(query)

        response = s.execute()
        
        def parse_function_abi(function_abi):
            inputs = {inp["name"]:inp["type"] for inp in function_abi["inputs"]}
            outputs = {(out["name"] if out["name"] != "" else "value"):out["type"] for out in function_abi["outputs"]}
            return {"inputs":inputs,"outputs":outputs}
        
        function_abi = parse_function_abi(response.to_dict()["hits"]["hits"][0]["_source"]["abi"])
        
        print(function_abi)
        
        def function_call(contract_address, function_name, function_abi, params, block_number):
            val = payload.func_call_payload(0, contract_address, function_name, function_abi, params, block_number)
            resp = requests.post(cfg.config["http_url"], json=val)

            outputs = function_abi["outputs"]
            values = eth_abi.decode(list(outputs.values()), bytes.fromhex(resp.json()["result"][2:]))
            keys = list(outputs.keys())
            result = {keys[i]: values[i] for i in range(len(keys))}
            return result
        
        print(params)
        result = function_call(contract_address, function_name, function_abi, params, hex(w3.eth.get_block("latest")["number"]))
        print(result)
        data = json.dumps(result)
        return HttpResponse(data, content_type='application/json')
    else:
        return render(request, 'abi/call_abi_template.html')
  
def index(request):
    index_name = 'abi'
    s = Search(using=es, index=index_name)
    field_to_match = 'type'  # Replace with the field name you want to match
    value_to_match = 'contract'  # Replace with the value you want to search for

    query = Q('match', type='contract')
    s = s.query(query)
    
    response = s.execute()
    abis = []
    for hit in response:
        abis.append(hit.to_dict())
    
    return render(request, 'abi/index_template.html', {'abis': abis})

def search_abi_with_keywords(keywords):
    print(keywords)
    index_name = 'abi'
    s = Search(using=es, index=index_name)
    keyword_queries = []

    for keyword in keywords:
        if keyword.startswith("0x"):
            keyword_queries.append(Q("multi_match", query=keyword, fields=["address"]))
        else:
            keyword_queries.append(Q("multi_match", query=keyword, fields=["name","contract","type"]))
        
    combined_query = Q('bool', should=keyword_queries)
    s = s.query(combined_query)

    response = s.execute()
    return response
  
@csrf_exempt
def search_abi(request):
    if request.method == 'POST':
        data = json.loads(request.body)        
        keywords = data["keywords"]
        res = search_abi_with_keywords(keywords)
        data = json.dumps(res.to_dict()["hits"]["hits"])
        return HttpResponse(data, content_type='application/json')
    return HttpResponse(json.dumps([]), content_type='application/json')

def search_results(request, keywords):
    res = search_abi_with_keywords(re.split("\s+", keywords))
    abis = []
    print(res)
    for hit in res:
        print(hit)
        abis.append(hit)
    return render(request, 'abi/search_abi_template.html', {'abis': abis})
