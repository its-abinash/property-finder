import os
from property_finder.middleware import *
from property_finder.apps import *
from property_finder.databases import *
from property_finder.env import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'vl*7k22hul^-vk&eij)oq!h)2!@ete(+nrz$054!(0#kauec%9'

ALLOWED_HOSTS = ["*"]

DJANGO_MODEL_BACKEND = 'django.contrib.auth.backends.ModelBackend'

ROOT_URLCONF = 'property_finder.urls'

WSGI_APPLICATION = 'property_finder.wsgi.application'

AUTH_USER_MODEL = 'authentication.User'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True