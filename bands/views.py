from bands.forms import ExpressRegistrationForm
from django.core import serializers
from django.http import HttpResponse


def subscribe(request):
    success = "1"
    
    if request.method == 'POST' and request.is_ajax(): 
        form = ExpressRegistrationForm(request.POST)
        if not form.is_valid():
            success = "0"
            
    #output = serializers.serialize("json", {'success', success})
    output = "{'success', " + success + "})"
    return HttpResponse(output)
