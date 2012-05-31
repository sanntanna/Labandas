from bands.models import Musician
from django.contrib.auth.models import User
from django.test import TestCase
from mockito.mocking import mock
from mockito.mockito import when

class MusicianTests(TestCase):
    def setUp(self):
        user = User()
        when(User).get_full_name().thenReturn("John petrucci")
        self.musician = Musician(user=user)
    
    def test_deve_encodar_url_perfil_corretamente(self):
        url = self.musician.encode_profile()
        self.assertEqual(url, u"/musico/john-petrucci/" + str(self.musician.pk))
