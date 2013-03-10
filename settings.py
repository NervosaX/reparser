import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sqlite.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

USE_HIDDEN_DISPLAY = False
REAL_ESTATE_URL = "http://www.realestate.com.au"
# property-house-with-3-bedrooms-between-0-650000-in-caulfield%2c+vic+3162%3b+caulfield+north%2c+vic+3161%3b+malvern%2c+vic+3144%3b+glen+iris%2c+vic+3146%3b+camberwell%2c+vic+3124%3b+ashburton%2c+vic+3147%3b+carnegie%2c+vic+3163%3b+ormond%2c+vic+3204%3b+mckinnon%2c+vic+3204%3b+bentleigh%2c+vic+3204%3b+moorabbin%2c+vic+3189%3b+highett%2c+vic+3190%3b+cheltenham%2c+vic+3192%3b+mentone%2c+vic+3194%3b+clarinda%2c+vic+3169%3b+oakleigh+south%2c+vic+3167%3b+oakleigh+east%2c+vic+3166%3b+oakleigh%2c+vic+3166%3b+huntingdale%2c+vic+3166%3b+heatherton%2c+vic+3202%3b+clayton+south%2c+vic+3169%3b+chadstone%2c+vic+3148%3b+mount+waverley%2c+vic+3149%3b+ashwood%2c+vic+3147%3b+burwood%2c+vic+3125%3b+burwood+east%2c+vic+3151%3b+notting+hill%2c+vic+3168%3b+mulgrave%2c+vic+3170%3b+springvale%2c+vic+3171%3b+glen+waverley%2c+vic+3150%3b+chelsea%2c+vic+3196%3b+chelsea+heights%2c+vic+3196%3b+/list-1?exteriorFeatures=garage&numParkingSpaces=2&numBaths=2&maxBeds=any&misc=ex-under-contract&source=location-search
REAL_ESTATE_SEARCH_STRING = "property-house-with-3-bedrooms-size-500-between-0-700000-in-malvern%2c+vic+3144%3b+camberwell%2c+vic+3124%3b+box+hill+south%2c+vic+3128%3b+burwood%2c+vic+3125%3b+burwood+east%2c+vic+3151%3b+ashwood%2c+vic+3147%3b+chadstone%2c+vic+3148%3b+carnegie%2c+vic+3163%3b+caulfield+north%2c+vic+3161%3b+caulfield%2c+vic+3162%3b+malvern+east%2c+vic+3145%3b+caulfield+south%2c+vic+3162%3b+elsternwick%2c+vic+3185%3b+gardenvale%2c+vic+3185%3b+brighton+north%2c+vic+3186%3b+brighton%2c+vic+3186%3b+ormond%2c+vic+3204%3b+glen+iris%2c+vic+3146%3b+ripponlea%2c+vic+3185%3b+elwood%2c+vic+3184%3b+bentleigh%2c+vic+3204%3b+bentleigh+east%2c+vic+3165%3b+highett%2c+vic+3190%3b+black+rock%2c+vic+3193%3b+mentone%2c+vic+3194%3b+clarinda%2c+vic+3169%3b+clayton%2c+vic+3168%3b+clayton+north%2c+vic+3168%3b+clayton+south%2c+vic+3169%3b+cheltenham%2c+vic+3192%3b+heatherton%2c+vic+3202%3b+parkdale%2c+vic+3195%3b+dingley+village%2c+vic+3172%3b+springvale+south%2c+vic+3172%3b+springvale%2c+vic+3171%3b+waterways%2c+vic+3195%3b+aspendale%2c+vic+3195%3b+edithvale%2c+vic+3196%3b+chelsea+heights%2c+vic+3196%3b+keysborough%2c+vic+3173%3b+mulgrave%2c+vic+3170%3b+endeavour+hills%2c+vic+3802%3b+knoxfield%2c+vic+3180%3b+vermont+south%2c+vic+3133%3b+blackburn+south%2c+vic+3130%3b+mckinnon%2c+vic+3204%3b+oakleigh%2c+vic+3166%3b+oakleigh+east%2c+vic+3166%3b+oakleigh+south%2c+vic+3167/list-1?numParkingSpaces=2&numBaths=2&maxBeds=any&misc=ex-under-contract&source=refinements"
METLINK_BASE_URL = "http://jp.ptv.vic.gov.au/ptv/"
METLINK_SEARCH_URL = "http://jp.ptv.vic.gov.au/ptv/XSLT_TRIP_REQUEST2?language=en&itdLPxx_view=advanced"
ADSL_URL = "http://www.adsl2exchanges.com.au/"

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8a%u7yz941q-jvyxz%gpiax3pv*p!+j7jf8%-+3+9oyf_44-65'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # Third party apps
    'django_extensions',
    'south',

    # Apps
    'base',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    from local_settings import *
except ImportError:
    pass