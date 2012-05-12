from bands.forms import ExpressRegistrationForm
from django.contrib.auth import login, authenticate
from jsonui.response import JSONResponse


def subscribe(request):
    data = { "success": True }
    
    if request.method == 'POST': 
        form = ExpressRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            login(request, user)
        else:
            data["errors"] = form.errors
            data["success"] = False

    return JSONResponse(data)