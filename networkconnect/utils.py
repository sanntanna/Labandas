#coding=ISO-8859-1
from django.conf import settings as django_settings
from django.contrib.auth.models import User
import json
from labandas import settings
from httplib2 import Http
from models import UserNetwork

class UserFinder(object):

	def get_user(self, network, token, user_id):
		network_user = UserNetwork.objects.get_by_network_id(user_id, network)

		if not network_user is None:
			self.__add_user_backend(network_user.user)
			return network_user.user, None

		if not hasattr(self, network):
			raise ValueError('Rede %s nao encontrada'% network)

		return getattr(self, network)(user_id, token)

	def facebook(self, user_id, token):
		response, content = Http().request("https://graph.facebook.com/%s?access_token=%s" % (user_id, token))
		fb_data = json.loads(content)
		fb_data['avatar_url'] = "http://graph.facebook.com/%s/picture?width=200&height=200" % user_id

		stored_users = User.objects.filter(username=fb_data['email'])

		if stored_users.count() > 0:
			user = stored_users[0]
			self.__bind_user_in_network(user, user_id, 'facebook', fb_data)
			return user, {}

		user = User.objects.create_user(fb_data['email'], fb_data['email'], "78%s123%s309" % (user_id,user_id))
		user.first_name=fb_data['first_name']
		user.last_name=fb_data['last_name']
		user.save()

		self.__bind_user_in_network(user, user_id, 'facebook', fb_data)
		self.__add_user_backend(user)

		return user, fb_data


	def __bind_user_in_network(self, user, network_id, network_name, extra_fields):
		user_network = UserNetwork()
		user_network.user = user
		user_network.network_id = network_id
		user_network.network_name = network_name
		user_network.extra_fields = extra_fields

		user_network.save()

	def __add_user_backend(self, user):
		if hasattr(user, 'backend'):
			return

		from django.contrib.auth import load_backend	
		for backend in django_settings.AUTHENTICATION_BACKENDS:
			if user == load_backend(backend).get_user(user.pk):
				user.backend = backend
				return