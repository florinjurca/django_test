from exadmin.models import TestUsersAuth
from django.http import QueryDict

try:
    user = {
        'id':1,
        'username':'admin',
        'password':'123456',
        'email':'admin@django_test.ro1',
        'first_name':'administrator',
        'last_name':'reea',
        'is_admin':True
    }
    
    out = ''
    for key in user:
        out += '%s=%s&' % (key,user[key])
    
    TestUsersAuth.objects.create_user(QueryDict(out))
    
except:
    pass

try:
    for i in range(1,8):
        user = {
            'id': i+1,
            'username':'johnsmith_%d' % (i,),
            'password':'123456',
            'email':'johnsmith%d@gmail.com' % (i,),
            'first_name':'John_%d' % (i,),
            'last_name':'Smith_%d' % (i,)
        }
        
        out = ''
        for key in user:
            out += '%s=%s&' % (key,user[key])
        
        TestUsersAuth.objects.create_user(QueryDict(out))
except:
    pass
    
