"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.

Test create_user
Test update_user
Test delete_user
    test values stored in db
        data 
            match
            right length
    
    test displaing right errors


Test password hashing
    test against a withness method
        matching password


Test views
    
    verify loading urls - whole page
        /admin/                 = index_1
        /admin/edit/<N>/        = edit_1
        /admin/edit/<N>/save/   = edit_1
        /admin/<N>/             = delete_1
        
    verify content on views
        loading 
            js scripts
            css sheets
        
    
    verify loading right templates
    
    verify the right context ??? - 
    


Testing new methods must be done in such a manner that allready tested django code will 
be excluded from tests


"""
from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor, sha_constructor

from django.test import TestCase
from django.test.client import Client
from django.db import models 
from exadmin.models import TestUsersAuth
from django.http import QueryDict

from os import system
system('cls')

'''
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
'''


UNUSABLE_PASSWORD = '!'  # This will never be a valid hash 


def get_hexdigest(algorithm, salt, raw_password):
    """
    Returns a string of the hexdigest of the given plaintext password and salt
    using the given algorithm ('md5', 'sha1' or 'crypt').
    """
    raw_password, salt = smart_str(raw_password), smart_str(salt)
    if algorithm == 'crypt':
        try:
            import crypt
        except ImportError:
            raise ValueError('"crypt" password algorithm not supported in this environment')
        return crypt.crypt(raw_password, salt)
    
    if algorithm == 'md5':
        return md5_constructor(salt + raw_password).hexdigest()
    elif algorithm == 'sha1':
        return sha_constructor(salt + raw_password).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")


def set_password(raw_password):
    if raw_password is None: 
        password = UNUSABLE_PASSWORD
    else:
        import random
        algo = 'sha1'
        #salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
        salt = get_hexdigest(algo, 'Florin', 'Jurca')[:5]
        hsh = get_hexdigest(algo, salt, raw_password)
        password = '%s$%s$%s' % (algo, salt, hsh)
        
    return password

class ExadminTestCase(TestCase):
    """
    Tests custom manager methods 
    """
    #fixtures = ['exadmin_views_testdata.json']
    
    def setUp(self):
        """
        Setup the 
        """
        self.users=[]
        
        for i in range(10):
            user = {
                'username'  :'ionion_%d' % i,
                'password'  :'123456',
                'email'     :'ionion_%d@cucu.com' % i,
                'first_name':'Ion_%d' % i,
                'last_name' :'Ion_%d' % i
            }
            
            self.users.append(user)
            
    
    def test_delete_user(self):
        """
        Test delete_user
        """
        user = self.users[0]
        
        out = ''
        for key in user:
            out += '%s=%s&' % (key,user[key])
        
        # Creating a new user
        user_in = TestUsersAuth.objects.create_user(QueryDict(out))
        
        # ###
        # Fetch the id (the user_db.id) before modify 
        try:
            user_db = TestUsersAuth.objects.get(username=user['username'])
        except:
            user_db = False
        
        self.assertNotEqual(user_db,False)
        
        out = ''
        user['id'] = user_db.id
        for key in user:
            out += '%s=%s&' % (key,user[key])
        
        TestUsersAuth.objects.delete_user(QueryDict(out))
        
        try:
            user_db = TestUsersAuth.objects.get(pk=user_db.id)
        except:
            user_db = False
            
        self.assertEqual(user_db,False)
        
        
    
    def test_update_user(self):
        """
        Tests update_user 
            setup user_data
            create new user
            user_data_db = fetch the user for id
            setup new_user_data
            update the user with id
            new_user_data_db = fetch again the same user
            assert new_user_data == new_user_data_db
        """
        
        user = self.users[0]
        
        out = ''
        for key in user:
            out += '%s=%s&' % (key,user[key])
        
        # Creating a new user
        user_in = TestUsersAuth.objects.create_user(QueryDict(out))
        
        # ###
        # Fetch the user before modify - the user.id
        user_db = TestUsersAuth.objects.get(username=user['username'])
        
        # ###
        # Using another values for update
        user = self.users[1]
        # Setting the id in value
        user['id'] = user_db.id
        
        out = ''
        for key in user:
            out += '%s=%s&' % (key,user[key])
        
        # Update will be done
        user_in = TestUsersAuth.objects.update_user(QueryDict(out))
        
        #This is not a test of password hashing so we will use the same hashing method
        #prior to this test a test for password hashing method needs to be done
        user['password'] = user_in.password
        
        # ###
        # Get the new updated values
        user_out = TestUsersAuth.objects.get(pk=user['id'])
        
        for key in user:
            if key != 'username':
                self.assertEqual(eval('user_out.%s' % key),user[key])
        
        self.assertNotEqual(user_out.username,user['username'])
        self.assertEqual(user_out.is_admin,False)
        
    
    def test_create_user(self):
        """
        Tests create_user: admin and regular
            new_user_data
            create_user
            user_data = fetch the newly created <user>
            compare new_user_data with user_data
        """
        
        user = self.users[0]
        user['is_admin'] = True
        
        out = ''
        for key in user:
            out += '%s=%s&' % (key,user[key])
        
        user_in = TestUsersAuth.objects.create_user(QueryDict(out))
        
        #This is not a test of password hashing so we will use the same hashing method
        #prior to this test a test for password hashing method needs to be done
        user['password'] = user_in.password
        
        user_out = TestUsersAuth.objects.get(username=user['username'])
        
        for key in user:
            self.assertEqual(eval('user_out.%s' % key),user[key])
        
        self.assertEqual(user_out.is_admin,True)
        
        # #####
        
        user = self.users[1]
        
        out = ''
        for key in user:
            out += '%s=%s&' % (key,user[key])
        
        user_in = TestUsersAuth.objects.create_user(QueryDict(out))
        
        #This is not a test of password hashing so we will use the same hashing method
        #prior to this test a test for password hashing method needs to be done
        user['password'] = user_in.password
        
        user_out = TestUsersAuth.objects.get(username=user['username'])
        
        for key in user:
            self.assertEqual(eval('user_out.%s' % key),user[key])
        
        self.assertEqual(user_out.is_admin,False)
        
    
    def test_password_hash_user(self):
        """
        Test 
        """
        user = self.users[0]
        
        out = ''
        for key in user:
            out += '%s=%s&' % (key,user[key])
        
        # Creating a new user
        user_in = TestUsersAuth.objects.create_user(QueryDict(out))
        
        password_martor = set_password(user['password'])
        password = user_in.password
        
        self.assertEqual(len(password_martor),len(password))
        self.assertEqual(password_martor,password)
        
    




class ExadminViewsTestCase(TestCase):
    """
    Tests views - tests are processed in reverse order
    """
    fixtures = ['exadmin_views_testdata.json']
    
    def setUp(self):
        """
        Instantiate the client 
        """
        self.client = Client()
        
    '''
    def tearDown(self):
        
        users = TestUsersAuth.objects.filter(username__startswith = 'test_')
        users.delete()
        
    '''
    
    def test_users_delete_index(self):
        users = TestUsersAuth.objects.all()
        for user in users:
            
            resp = self.client.get('/exadmin/%d/' % user.id)
            self.assertRedirects(resp,'/exadmin/',status_code=302,target_status_code=200,
                msg_prefix=''
            )
            
            resp = self.client.get('/exadmin/')
            self.assertNotContains(resp,'<tr id="user_%d">' % user.id, status_code=200,
                msg_prefix=''
            )
        
    
    def test_load_index(self):
        """
        Tests that GET /exadmin/ allways return 200 status_code
        """
        
        #Loading page index_1
        resp = self.client.get('/exadmin/')
        self.assertEqual(resp.status_code, 200)
        
        self.assertTemplateUsed(resp, 'exadmin/users_list.html', 
            msg_prefix=''
        ) 
        
        users = TestUsersAuth.objects.all()
        for user in users:
            self.assertContains(resp,'<tr id="user_%d">' % user.id, count=1, status_code=200,
                msg_prefix=''
            )
        
    
    def test_load_edit(self):
        """
        Tests that the right template was used
        Tests that GET /exadmin/edit/<N>/ allways return 200 status_code
        """
        
        
        #Loading 3 pages
        users = TestUsersAuth.objects.all()
        
        for user in users:
            resp = self.client.get('/exadmin/edit/%d/' % user.id)
            self.assertEqual(resp.status_code, 200)
            
            self.assertTemplateUsed(resp, 'exadmin/user_edit.html', 
                msg_prefix=''
            ) 
        
        
        
        #self.AssertTrue('')
        
    