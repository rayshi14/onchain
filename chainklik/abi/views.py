from django.http import HttpResponse
import json

def index(request):
    return HttpResponse("Hello, world. You're at the abi index.")
  
def contract_abi(request, contract_address):
    data = json.dumps({"contract":contract_address})
    return HttpResponse(data, content_type='application/json')
  
def function_abi(request, contract_address, function_name):
    data = json.dumps({"contract_address":contract_address,"function":function_name})
    return HttpResponse(data, content_type='application/json')
  
def event_abi(request, contract_address, event_name):
    data = json.dumps({"contract_address":contract_address,"event":event_name})
    return HttpResponse(data, content_type='application/json')