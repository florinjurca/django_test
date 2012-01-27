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
    


class TestUsersAuthManager(models.Manager):
    '''
    User manager - implementing:
        create_user
        update_user
        delete_user
    
    '''
    
    def create_user(self, data):
        '''
        Create an user 
        '''
        
        username    = data.__getitem__('username')
        password    = data.__getitem__('password')
        email       = data.__getitem__('email')
        first_name  = data.__getitem__('first_name')
        last_name   = data.__getitem__('last_name')
        
        is_admin    = data.__getitem__('is_admin') if data.has_key('is_admin') else False
        
        
        #print username,'|',password,'|',email,'|',first_name,'|',last_name,'|',is_admin
        
        
        now = datetime.datetime.now()
        
        '''
        try:
            email_name, domain_part = email.strip().split('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        '''
        
        
        user = self.model(
            username    = username, 
            email       = email, 
            first_name  = first_name,
            last_name   = last_name,
            is_admin    = is_admin, 
            cr_date     = now
        )
        
        user.set_password(password)
        
        #user.save(using=self._db)
        user.save()
        
        return user
        
    
    def update_user(self,data):
        '''
        Change the user profile
        '''
        
        #print data
        
        id          = data.__getitem__('id')
        #username   = data.__getitem__('username') #the username can't be changed
        password    = data.__getitem__('password')
        email       = data.__getitem__('email')
        first_name  = data.get('first_name','')
        last_name   = data.get('last_name','')
        is_admin    = data.get('is_admin',False)
        
        
        #print username,'|',password,'|',email,'|',first_name,'|',last_name,'|',is_admin
        
        '''
        try:
            email_name, domain_part = email.strip().split('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        '''
        
        
        user = self.model.objects.get(pk=id)
        
        user.email      = email
        user.first_name = first_name
        user.last_name  = last_name
        
        user.set_password(password)
        
        #user.save(using=self._db)
        user.save()
        
        return user
        
    
    def delete_user(self,data):
        '''
        Delete the user
        '''
        user = self.model.objects.get(pk=data.__getitem__('id'))
        user.delete()
        


class TestUsersAuth(models.Model):
    '''
    Test users table
    '''
    id = models.AutoField(primary_key=True)
    username = models.CharField('Username', max_length=30, unique=True)
    password = models.CharField('Password', max_length=256)
    first_name = models.CharField('First name', max_length=30, blank=True)
    last_name = models.CharField('Last name', max_length=30, blank=True)
    email = models.EmailField('E-mail address', max_length=60)
    is_admin = models.BooleanField('is admin', default=False)
    cr_date = models.DateTimeField('creation date', default=datetime.datetime.now, editable=False)
    
    #overloading the default manager
    objects = TestUsersAuthManager()
    
    def set_password(self, raw_password):
        if raw_password is None: 
            self.set_unusable_password()
        else:
            import random
            algo = 'sha1'
            #salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
            salt = get_hexdigest(algo, 'Florin', 'Jurca')[:5]
            hsh = get_hexdigest(algo, salt, raw_password)
            self.password = '%s$%s$%s' % (algo, salt, hsh)
    
    def __unicode__(self):
        return u'%s %s %s %s %s %s' % (
            self.id,
            self.username, 
            self.password, 
            self.email, 
            self.first_name, 
            self.last_name
        )
    

class TestUsersAuthForm(ModelForm):
    password_match=forms.CharField(
        label='Password again',
        min_length=6,
        max_length=16,
        widget=forms.PasswordInput()
    )
    
    class Meta:
        model = TestUsersAuth()
        '''
        try:
            model.test_objects.data = super(TestUsersAuthForm, self).data
        except:
            model.test_objects.data = {}
        '''
        
        #fields used only for changing fields order in form
        #fields = ['username','password','password_match','email','first_name','last_name']
        
        widgets = {
            'password': forms.PasswordInput()
        }
        
    
    def clean(self):
        super(TestUsersAuthForm, self).clean()
        cleaned_data = self.cleaned_data
        
        #print cleaned_data
        
        password_value = cleaned_data.get('password')
        password_match_value = cleaned_data.get('password_match')
        
        #print password_value,'=',password_match_value
        
        if password_value != password_match_value:
            raise forms.ValidationError("Passwords didn't match each other!")
            #raise ValidationError(_("Passwords don't match")) #i18n
        return cleaned_data
    
