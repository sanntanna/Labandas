#coding=ISO-8859-1
from labandas import settings
from models import UserNetwork

class UserFinder(object):

	def get_user(self, token, network):
		user = UserNetwork.objects.get_by_token(token, network)

		if not user is None:
			return user

		if not hasattr(self, network):
			raise ValueError('Rede %s nao encontrada'% network)

		return getattr(self, network)(token)

	def facebook(self, token):
		print token
		return None