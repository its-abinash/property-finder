import os

DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE"),
        'NAME': os.getenv("DB_NAME", "property_finder"),
        'USER': os.getenv("DB_USER"),
        'HOST': os.getenv("DB_HOST", "127.0.0.1"),
        "PASSWORD": os.getenv("DB_PASSWORD", "pass"),
        "PORT": os.getenv("DB_PORT", "3306")
    }
}

DEFAULT_AUTO_FIELD='django.db.models.AutoField'