from django.template.base import Library
from ..utils import FileOptimizer

register = Library()

@register.simple_tag
def css(file_path):
    compiled_file_path = FileOptimizer().load(file_path).with_less().build()
    return '<link rel="stylesheet" href="%s" />' % compiled_file_path

@register.simple_tag
def js(file_path):
    compiled_file_path = FileOptimizer().load(file_path).build()
    return '<script src="%s"></script>' % compiled_file_path