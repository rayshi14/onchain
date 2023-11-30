from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import AbiForm

from datetime import datetime
import hashlib
import json

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

# local modules
import libs.common.etherscan as etherscan
import libs.common.payload as payload
import eth_abi

es = Elasticsearch("https://localhost:9200",http_auth=('elastic', 'y=fUp=8ucKL18I5K=1Am'),verify_certs=False)

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
            Q('match', name=function_name), 
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
        params = json.loads(request.body)
        contract_addr = params["contract"]
        function_name = params["name"]
        
        def parse_function_abi(function_abi):
            inputs = {(inp["name"] if inp["name"] != "" else "value"):inp["type"] for inp in function_abi["inputs"]}
            outputs = {(out["name"] if out["name"] != "" else "value"):out["type"] for out in function_abi["outputs"]}
            return {"inputs":inputs,"outputs":outputs}
        # get function abi
        # 
        return render(request, 'abi/call_abi_template.html')
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
