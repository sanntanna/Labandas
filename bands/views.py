#coding=ISO-8859-1
from bands.forms import ExpressRegistrationForm, BandForm, UserInfoForm, \
    BandMusicianForm
from bands.models import Musician, Band, MusicianBand
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponsePermanentRedirect, \
    HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.template import loader
from django.template.context import RequestContext
from http_method.BaseView import BaseView, get, ajax, onypostallowed
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

class MusicianProfile(BaseView):
    @get
    def show_profile(self, request, user_id, name):
        owner = get_object_or_404(Musician, pk=user_id)
        
        correct_url = owner.encode_profile()
        if correct_url != request.path_info:
            return HttpResponsePermanentRedirect(correct_url)
        
        t = loader.get_template('bands/musician-profile.html')
        
        c = RequestContext(request, {
            'owner': owner,
            'owner_bands': owner.get_musician_bands(),
        })
        
        return HttpResponse(t.render(c))
    
class AddBand(BaseView):
    @get
    def get(self, request):
        t = loader.get_template('bands/edit-band.html')
        c = RequestContext(request, {
            'form': BandForm(), 
            'musician_form':BandMusicianForm()
        })
        
        return HttpResponse(t.render(c))
    
    @ajax
    @onypostallowed
    def post(self, request):
        form = BandForm(data=request.POST)
        band = None
        success = True
        current_musician = request.user.get_profile()
        form_musician = BandMusicianForm(data=request.POST)
        
        if form.is_valid() and form_musician.is_valid():
            band = form.save()
            form_musician.save_admin(band=band, musician=current_musician)
        else:
            success = False
        
        if success:
            return JSONResponse({'success': success})
        
        return JSONResponse({'success': False, 'errors': form.errors})
    
class EditBand(BaseView):
    @get
    def get(self, request, band_id):
        band = get_object_or_404(Band, pk=band_id)
        musician_in_band = None
        
        try:
            musician_in_band = MusicianBand.objects.get(band=band, musician=request.user.get_profile(), active=True)
        except:
            print("Musico nao incluido na banda")
            return HttpResponseNotFound()
        
        t = loader.get_template('bands/edit-band.html')
        
        c = RequestContext(request, {
            'band': band,
            'form': BandForm(instance=band), 
            'musician_form':BandMusicianForm(instance=musician_in_band),
            'edit': True,
            'logged_user_is_admin': musician_in_band.is_admin,
        })
        
        return HttpResponse(t.render(c))
    
    @ajax
    @onypostallowed
    def post(self, request, band_id):
        #TODO: melhorar esse metodo, mover a verificacao de seguranca para outra camada 
        band = get_object_or_404(Band, pk=band_id)
        success = True
        form = BandForm(data=request.POST, instance=band)
        musician_in_band = None
        
        try:
            musician_in_band = MusicianBand.objects.get(band=band, musician=request.user.get_profile(), active=True)
        except:
            print("Musico nao incluido na banda")
            return HttpResponseNotFound()
        
        if form.is_valid():
            form.save()
            musician_form = BandMusicianForm(data=request.POST)
            if musician_form.is_valid():
                musician_in_band.instruments = musician_form.cleaned_data['instruments']
        else:
            success = False
        
        if success:
            return JSONResponse({'success': success})
        
        return JSONResponse({'success': False, 'errors': form.errors})
    
class BandPage(BaseView):
    @get
    def show_page(self, request, band_id, name):
        band = get_object_or_404(Band, pk=band_id)
        
        correct_url = band.encode_page()
        if correct_url != request.path_info:
            return HttpResponsePermanentRedirect(correct_url)
        
        t = loader.get_template('bands/band-page.html')
        c = RequestContext(request, {
            'band': band,
        })
        
        return HttpResponse(t.render(c))

def search_musician(request):
    search = request.GET.get('q')
    musicians = Musician.objects.filter(user__first_name__icontains=search).values('pk', 'user__first_name')
    return JSONResponse({'success': True, 'musicians': musicians}) 

def remove_musician_from_band(request):
    #TODO: adicionar validação para nao remover todos os admins, sempre deve ficar um
    success = MusicianBand.objects.get(pk=request.POST.get('id')).deactivate()
    return JSONResponse({'success': success}) 

def add_musician_in_band(request):
    return JSONResponse({'success': True}) 

                                                                    
def get_bands(request):
    bands = request.user.get_profile().get_bands()
    return JSONResponse({'success': True, 'bands':bands})



