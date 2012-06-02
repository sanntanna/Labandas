from bands.models import MusicianBand, Band
from django.contrib.auth.models import User
from django.test import TestCase

class BandsTests(TestCase):
    
    @classmethod
    def _musician_(cls, name, username):
        return User.objects.create(first_name=name, username=username).get_profile()
    
    @classmethod
    def _add_into_band_(cls, musician, band, is_admin=False, active=True):
        return MusicianBand.objects.create(band=band, musician=musician, active=active, is_admin=is_admin)
    
    @classmethod
    def setUpClass(cls):
        cls.petrucci = cls._musician_("John Petrucci","petrucci")
        cls.portnoy = cls._musician_("Mike Portnoy", "portnoy")
        cls.rudess = cls._musician_("Jordan Rudess", "jordan")
        cls.clapton = cls._musician_("Eric Clapton", "clapton")
        
        cls.dream_theater = Band.objects.create(name="Dream theater")
        cls.lte = Band.objects.create(name="Liquid Tension Experiment")
        
        cls._add_into_band_(cls.petrucci, cls.dream_theater)
        cls._add_into_band_(cls.petrucci, cls.lte, active=False)
        cls._add_into_band_(cls.portnoy, cls.dream_theater, is_admin=True)
        cls._add_into_band_(cls.rudess, cls.dream_theater, active=False)
        
    
    def test_deve_salvar_slugificar_e_salvar_url_musico(self):
        self.assertEqual(self.clapton.url, "eric-clapton")
    
    def test_deve_encodar_urls_perfis_musicos(self):
        self.assertEqual(self.petrucci.encode_profile(), u"/musico/john-petrucci/1")
        self.assertEqual(self.portnoy.encode_profile(), u"/musico/mike-portnoy/2")
    
    def test_deve_listar_bandas_ativas_do_musico(self):
        bands = self.petrucci.bands_list
        
        self.assertTrue(self.dream_theater in bands)
        self.assertFalse(self.lte in bands)
        
        self.assertEqual(len(bands), 1)
    
    def test_deve_verificar_se_musico_esta_na_banda(self):
        self.assertTrue(self.petrucci.is_in_band(self.dream_theater))
    
    def test_deve_verificar_se_musico_nao_esta_na_banda(self):
        self.assertFalse(self.clapton.is_in_band(self.dream_theater))
    
    def test_deve_listar_apenas_musicos_ativos(self):
        musicians_in_band = self.dream_theater.musicians
        musicians = [m.musician for m in  musicians_in_band]

        self.assertTrue(self.petrucci in musicians)
        self.assertTrue(self.portnoy in musicians)
        self.assertFalse(self.rudess in musicians)
        
    def test_deve_verificar_se_musico_eh_admin_da_banda(self):
        self.assertTrue(self.dream_theater.is_admin(self.portnoy))
    
    def test_deve_verificar_se_musico_nao_eh_admin_da_banda(self):
        self.assertFalse(self.dream_theater.is_admin(self.petrucci))
    