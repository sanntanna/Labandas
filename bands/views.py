from bands.forms import ExpressRegistrationForm, BandForm, UserInfoForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.context import RequestContext
from http_method.BaseView import BaseView, get, post, ajax, onypostallowed
from jsonui.response import JSONResponse

class UpdateCep(BaseView):
    @ajax
    def update(self, request):
        if request.GET["cep"] == "":
            return JSONResponse({ "success": False })
        
        musician = request.user.get_profile() 
        musician.set_cep(request.GET["cep"])
        musician.save()
        return JSONResponse({ "success": True })
    
class SubscribeMusician(BaseView):
    @ajax
    @onypostallowed
    def subscribe_musician_ajax(self, request):
        form = ExpressRegistrationForm(request.POST)
        
        if not form.is_valid():
            return JSONResponse({'success': False, 'errors': form.errors})
        
        form.save()
        user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
        login(request, user)
        return JSONResponse({'success': True, 'user': user})

class EditMusician(BaseView):
    @get
    def edit_musician(self, request):
        t = loader.get_template('bands/edit-musician.html')
        c = RequestContext(request, {'form': UserInfoForm(instance=request.user)})
        
        return HttpResponse(t.render(c))
    
    @ajax
    @onypostallowed
    def edit_musician_post(self, request):
        form = UserInfoForm(data=request.POST, instance=request.user)
        if not form.is_valid():
            return JSONResponse({'success':False, 'errors': form.errors})
        
        form.save()
        return JSONResponse({'success': True})
    
class AddBand(BaseView):
    @get
    def add_band(self, request):
        t = loader.get_template('bands/new-band.html')
        c = RequestContext(request, {'form': BandForm()})
        
        return HttpResponse(t.render(c))
    @post
    def add_band_post(self, request):
        form = BandForm(request.POST)
        if form.is_valid():
            form.save()
        
        return HttpResponseRedirect("/")
