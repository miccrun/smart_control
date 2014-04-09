from settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []


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

LOCAL_MODE = False
API_PATH = "http://192.168.1.148/central.php"
