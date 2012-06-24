from django.template.base import Library
from ..utils import PackageManager

register = Library()

@register.simple_tag
def package(package_file):
    manager = PackageManager()
        
    return manager.load(package_file).with_less().build()