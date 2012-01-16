from admin.models import TestUsersAuth


try:
    user = TestUsersAuth(
        username='admin',
        password='123456',
        email='admin@django_test.ro1',
        first_name='administrator',
        last_name='reea',
        is_admin=True
    )
    user.save()
except:
    pass

try:
    for i in range(1,101):
        user = TestUsersAuth(
            username='johnsmith_%d' % (i,),
            password='123456',
            email='johnsmith%d@gmail.com' % (i,),
            first_name='John_%d' % (i,),
            last_name='Smith_%d' % (i,)
        )
        user.save()
except:
    pass
    
