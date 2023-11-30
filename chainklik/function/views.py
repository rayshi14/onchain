from django.shortcuts import render
from django.http import HttpResponse
from .forms import FunctionForm
from django.template import RequestContext

def index(request):
    return HttpResponse("Hello, world. You're at the abi index.")

# Create your views here.
def call_function(request):
    success_message = ""
    error_message = ""
    if request.method == 'POST':
        # If the form has been submitted, process the data
        form = FunctionForm(request.POST)
        if form.is_valid():
            # Form data is valid, perform actions with the data
            contract_addr = form.cleaned_data['contract_address']
            print(form.cleaned_data)
            success_message = ""
        else:
            error_message = "Form submission failed. Please check the errors below."
    else:
        # If this is a GET request, create a new form
        extra_questions = {"1":"test","2":"test2"}
        form = FunctionForm(extra=extra_questions)
    
    return render(request, 'function/call_function_template.html', {'form': form, 'success_message': success_message, 'error_message': error_message})