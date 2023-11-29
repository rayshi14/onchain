from django.http import HttpResponse
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(
    "https://localhost:9200",
    http_auth=('elastic', 'y=fUp=8ucKL18I5K=1Am'),
    verify_certs=False)

def index(request):
    return HttpResponse("Hello, world. You're at the abi index.")
  
def contract_abi(request, contract_address):
    index_name = 'abi'
    body={"size" : 100, "query":{ "match":{ "address": contract_address }, "match":{ "type": "contract" } } }
    resp = es.search(index=index_name, body=body)
    print(len(resp['hits']['hits']))
    if len(resp['hits']['hits']) > 0:
        result = resp['hits']['hits'][0]['_source']
        data = json.dumps([result['_source'] for result in resp['hits']['hits']])
        return HttpResponse(data, content_type='application/json')
    
    data = json.dumps({})
    return HttpResponse(data, content_type='application/json')
  
def function_abi(request, contract_address, function_name):
    data = json.dumps({"contract_address":contract_address,"function":function_name})
    return HttpResponse(data, content_type='application/json')
  
def event_abi(request, contract_address, event_name):
    data = json.dumps({"contract_address":contract_address,"event":event_name})
    return HttpResponse(data, content_type='application/json')