#coding=ISO-8859-1
from django.http import HttpResponse


class HttpPartialResponseHandler():
	template = None
	request_context = None
	
	def __init__(self, template, request_context):
		self.template = template
		self.request_context = request_context

	def buildHttpResponse(self):
		return HttpResponse(self.template.render(self.request_context))
