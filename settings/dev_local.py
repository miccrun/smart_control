from settings import *

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db',
        'USER': 'db_user',
        'PASSWORD': 'db_pwd',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}
