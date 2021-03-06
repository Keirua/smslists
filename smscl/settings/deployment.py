from base import *

#ALLOWED_HOSTS += ['']

MINIFIED_JS = True

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Process should have write privileges, web server should have read privileges
MEDIA_ROOT = '/var/www/smscl/media'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'localhost'
EMAIL_PORT = '25'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'smslists',
        'USER': 'smslists',
        'PASSWORD': 'LVAGVdAl1t',
        'HOST': 'localhost',
        'PORT': '',
    }
}

RAVEN_CONFIG = {
    # Use "?verify_ssl=0" at the end of the url if you don't have a valid certificate
    'dsn': 'https://',
}

PLIVO_NUMBER = "17472221816"

# This MUST be set to the domain names this instance is allowed to serve, otherwise
#  all requests will result in HTTP/400
ALLOWED_HOSTS = ['api.worlddev.io']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

GOOGLE_TRACKING_ID = 'UA-'
