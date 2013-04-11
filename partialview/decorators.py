#coding=ISO-8859-1

class Partialhandled(object):
	def __init__(self, full_template, partial_template):
		self.full_template = full_template
		self.partial_template = partial_template

	def __call__(self, func):

		def wrapped(*args, **kwargs):
			respose_handler = func(*args, **kwargs)

			if not hasattr(respose_handler, 'buildHttpResponse'):
				return respose_handler

			request = args[0]
			base_template = self.full_template if not request.GET.has_key('partial') else self.partial_template
			respose_handler.request_context['base_template'] = base_template

			return respose_handler.buildHttpResponse()
	
		return wrapped