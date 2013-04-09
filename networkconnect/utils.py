#coding=ISO-8859-1
from django.contrib.auth.models import User
import json
from labandas import settings
from httplib2 import Http
from models import UserNetwork

class UserFinder(object):

	def get_user(self, network, token, user_id):
		user = UserNetwork.objects.get_by_network_id(user_id, network)

		if not user is None:
			return user

		if not hasattr(self, network):
			raise ValueError('Rede %s nao encontrada'% network)

		return getattr(self, network)(user_id, token)

	def facebook(self, user_id, token):
		response, content = Http().request("https://graph.facebook.com/100001327309249?access_token=%s" % token)
		fb_data = json.loads(content)

		stored_users = User.objects.filter(username=fb_data['email'])

		if stored_users.count() > 0:
			user = stored_users[0]
			self.__bind_user_in_network(user, user_id, token, 'facebook')
			return user

		user = User.objects.create_user(fb_data['email'], fb_data['email'], "78%s123%s3˜" % (user_id,user_id), first_name=fb_data['first_name'], last_name=fb_data['last_name'])
		self.__bind_user_in_network(user, user_id, token, 'facebook')

		return user

	def __bind_user_in_network(self, user, network_id, network_token, network_name):
		UserNetwork.objects.create(user=user, network_id=network_id, network_token=network_token, network_name=network_name)