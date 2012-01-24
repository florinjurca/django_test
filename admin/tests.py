"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.

Test views

    
    verify loading urls - whole page
        /admin/                 = index_1
        /admin/edit/<N>/        = edit_1
        /admin/edit/<N>/save/   = edit_1
        /admin/<N>/             = delete_1
        
    verify content on views
        loading js scripts
        loading css sheets
    
    verify loading right templates
    
    verify the right context
    

Test create_user
    


Test update_user
    


Test delete_user
    


"""

from django.test import TestCase
from django.test.client import Client
from admin.models import TestUsersAuth

'''
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
'''

class AdminViewsTestCase(TestCase):
    """
    Tests views
    """
    fixtures = ['admin_views_testdata.json']
    
    def setUp(self):
        self.client = Client()
        
    def tearDown(self):
        
        users = TestUsersAuth.objects.filter(username__startswith = 'test_')
        users.delete()
        
    def test_index(self):
        """
        Tests that GET /admin/ allways return 200 status_code
        """
        
        #
        resp = self.client.get('/admin/')
        self.assertEqual(resp.status_code, 200)
        
        self.AssertTrue('')