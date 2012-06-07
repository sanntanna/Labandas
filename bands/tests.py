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
        
        cls.dream_theater = Band.objects.create(name="Dream theater")
        
        cls._add_into_band_(cls.petrucci, cls.dream_theater)
        cls._add_into_band_(cls.portnoy, cls.dream_theater, is_admin=True)
        cls._add_into_band_(cls.rudess, cls.dream_theater, active=False)
    
    def test_deve_salvar_slugificar_e_salvar_url_musico(self):
        self.assertEqual(self.portnoy.url, "mike-portnoy")
    
    def test_deve_encodar_urls_perfis_musicos(self):
        self.assertEqual(self.petrucci.encode_profile(), u"/musico/john-petrucci/1")
        self.assertEqual(self.portnoy.encode_profile(), u"/musico/mike-portnoy/2")
    
    def test_deve_listar_bandas_ativas_do_musico(self):
        lte = Band.objects.create(name="Liquid Tension Experiment")
        self._add_into_band_(self.petrucci, lte, active=False)
        
        bands = self.petrucci.bands_list
        
        self.assertTrue(self.dream_theater in bands)
        self.assertFalse(lte in bands)
        
        self.assertEqual(len(bands), 1)
    
    def test_deve_verificar_se_musico_esta_na_banda(self):
        self.assertTrue(self.petrucci.is_in_band(self.dream_theater))
    
    def test_deve_verificar_se_musico_nao_esta_na_banda(self):
        clapton = self._musician_("Eric Clapton", "clapton")
        self.assertFalse(clapton.is_in_band(self.dream_theater))
    
    def test_deve_listar_apenas_musicos_ativos(self):
        musicians = self.dream_theater.musicians_list
        
        self.assertTrue(self.petrucci in musicians)
        self.assertTrue(self.portnoy in musicians)
        self.assertFalse(self.rudess in musicians)
        
    def test_deve_verificar_se_musico_eh_admin_da_banda(self):
        self.assertTrue(self.dream_theater.is_admin(self.portnoy))
    
    def test_deve_verificar_se_musico_nao_eh_admin_da_banda(self):
        self.assertFalse(self.dream_theater.is_admin(self.petrucci))
    
    def test_nao_deve_permitir_que_nao_admin_adicione_musico(self):
        labrie = self._musician_("James Labrie", "james")
        with self.assertRaises(ValueError):
            self.dream_theater.add_musician(labrie, self.petrucci)
        
    def test_deve_adicionar_musico_na_banda(self):
        labrie = self._musician_("James Labrie", "james")
        
        self.dream_theater.add_musician(labrie, self.portnoy)
        self.assertTrue(labrie in self.dream_theater.musicians_list)
    
    def test_nao_deve_permitir_adicionar_musico_que_ja_esta_na_banda(self):
        with self.assertRaises(ValueError):
            self.dream_theater.add_musician(self.petrucci, self.portnoy)
    