from django.contrib.auth.models import User
from django.db import models

class UserNetworkManager(models.Manager):
    def get_by_network_id(self, token, network):
        users = self.filter(network_id = token, network_name = network)

        if users.count() == 0:
        	return None

        return users[0]

class UserNetwork(models.Model):
	user = models.OneToOneField(User)
	network_id = models.CharField(max_length=50)
	network_token = models.CharField(max_length=50)
	network_name = models.CharField(max_length=20)

	objects = UserNetworkManager()