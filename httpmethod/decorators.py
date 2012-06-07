from django.http import HttpResponseNotFound

def onlyajax(func):
    def new(request, *args, **kwargs):
        if not request.is_ajax():
            #TODO: adicionar log de erro aqui
            return HttpResponseNotFound()
        return func(request, *args, **kwargs)
    return new

def onlypost(func):
    def new(request, *args, **kwargs):
        if request.method != 'POST':
            #TODO: adicionar log de erro aqui
            return HttpResponseNotFound()
        return func(request, *args, **kwargs)
    return new