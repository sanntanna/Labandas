from bands.forms import ExpressRegistrationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse


def subscribe(request):
    success = "1"
    
    if request.method == 'POST' and request.is_ajax(): 
        form = ExpressRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            login(request, user)
        else:
            success = "0"
        
    #output = serializers.serialize("json", {'success', success})
    output = "{'success', " + success + "})"
    return HttpResponse(output)


#def logout(request):
    
#    return HttpResponse('<script>location.href="/";</script>')