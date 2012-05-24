from django.http import HttpResponseNotFound
_class_view_registry = {}

class BaseView(object):
    
    def __new__(cls, *args, **kwargs):
        instance = super(BaseView, cls).__new__(cls)

        # Try to get the view registry for this class from the global view 
        # registry. If it's not there, create one - just a dict - then iterate
        # through the class's members looking for objects which have been
        # annotated with an _httpmethod_name attribute. The value of this 
        # attribute is the HTTP method name that we want to associate this
        # method with.
        # 
        # If the registry is there, then we've processed this class before
        # and so all the mappings should be there.
        view_registry = _class_view_registry.get(cls, None)
        if view_registry is None:
            _class_view_registry[cls] = view_registry = {}
            
            for name in dir(instance):
                obj = getattr(instance, name)
                httpmethod_name = getattr(obj, '_httpmethod_name', None)
                if httpmethod_name is not None:
                    view_registry[httpmethod_name] = obj

        return instance

    def __call__(self, request, *args, **kwargs):
        methodname = request.method.strip().upper()
        if request.is_ajax():
            methodname = "AJAX"
        
        method = _class_view_registry.get(self.__class__).get(methodname)
        
        if method == None:
            print("Nenhum metodo mapeado para " + methodname)
            return HttpResponseNotFound()
        
        return method(request, *args, **kwargs)

def httpmethod(name, func):
    if not name:
        raise ValueError, 'name must be set'

    func._httpmethod_name = name
    return func

# Decorators for HTTP methods as defined in:
#  http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html
def post(func):
    return httpmethod('POST', func)

def get(func):
    return httpmethod('GET', func)

def ajax(func):
    return httpmethod('AJAX', func)

def head(func):
    return httpmethod('HEAD', func)
    
def delete(func):
    return httpmethod('DELETE', func)
    
def options(func):
    return httpmethod('OPTIONS', func)
    
def put(func):
    return httpmethod('PUT', func)
    
def trace(func):
    return httpmethod('TRACE', func)
    
def connect(func):
    return httpmethod('CONNECT', func)

def onypostallowed(func):
    def new(obj, request, *args, **kwargs):
        if request.method != 'POST':
            print "requisicao nao foi enviada via post. Url = " + request.path_info
            return HttpResponseNotFound()
        return func(obj, request, *args, **kwargs)
    
    return new