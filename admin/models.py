import datetime,urllib
from django.db import models
from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor, sha_constructor
from django.forms import ModelForm
from django import forms

# Create your models here.


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


class TestUsersAuth(models.Model):
    '''
    Test users table
    '''
    id = models.AutoField(primary_key=True, editable=False)
    username = models.CharField('Username', max_length=30, unique=True)
    password = models.CharField('Password', max_length=16)
    first_name = models.CharField('First name', max_length=30, blank=True)
    last_name = models.CharField('Last name', max_length=30, blank=True)
    email = models.EmailField('E-mail address', max_length=60)
    is_admin = models.BooleanField('is admin', default=False)
    cr_date = models.DateTimeField('creation date', default=datetime.datetime.now, editable=False)
    
    def set_password(self, raw_password):
        if raw_password is None:
            self.set_unusable_password()
        else:
            import random
            algo = 'sha1'
            salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
            hsh = get_hexdigest(algo, salt, raw_password)
            self.password = '%s$%s$%s' % (algo, salt, hsh)
    

class TestUsersAuthForm(ModelForm):
    password_match=forms.CharField(max_length=16)
    class Meta:
        model = TestUsersAuth
            


class TestUsersManager(models.Manager):
    '''
    User manager 
    '''
    def create_user(self, username, email, password):
        '''
        Create an user 
        '''
        now = datetime.datetime.now()
        
        try:
            email_name, domain_part = email.strip().split('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
            
        user = self.model(username=username, email=email, is_admin=False, cr_date=now)
        
        user.set_password(password)
        
        user.save(using=self._db)
        
    
    def update_user(self,email,password,first_name='',last_name=''):
        '''
        Change the user profile
        '''
        
        try:
            email_name, domain_part = email.strip().split('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        
        user = self.model(email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        
    
    def delete_user(self,username):
        '''
        Delete the user
        '''
        user = self.model(username=username)
        user.delete()
        
    