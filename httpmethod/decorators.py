#coding=ISO-8859-1
from django.http import HttpResponseNotFound
import logging

logger = logging.getLogger('labandas')

def onlyajax(func):
    def new(request, *args, **kwargs):
        if not request.is_ajax():
            logger.warn("url %s, Requisicao invalida, deveria ser ajax" % request.path)
            return HttpResponseNotFound()
        return func(request, *args, **kwargs)
    return new

def onlypost(func):
    def new(request, *args, **kwargs):
        if request.method != 'POST':
            logger.warn("[url:%s] Requisicao invalida, deveria ser post" % request.path)
            return HttpResponseNotFound()
        return func(request, *args, **kwargs)
    return new