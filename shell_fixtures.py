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
    user = TestUsersAuth(
        username='florinjurca',
        password='',
        email='florinjurca@gmail.com',
        first_name='Florin',
        last_name='Jurca'
    )
    user.save()
except:
    pass

try:
    user = TestUsersAuth(
        username='jijiz',
        password='123456',
        email='jijizumba@yahoo.com',
        first_name='Jiji',
        last_name='Zumba'
    )
    user.save()
except:
    pass

try:
    user = TestUsersAuth(
        username='ionz',
        password='123456',
        email='ionzabrea@yahoo.com',
        first_name='Ion',
        last_name='Zabrea'
    )
    user.save()
except:
    pass

try:
    user = TestUsersAuth(
        username='mischie',
        password='123456',
        email='valentinmischie@gmail.com',
        first_name='Valentin',
        last_name='Mischie'
    )
    user.save()
except:
    pass
