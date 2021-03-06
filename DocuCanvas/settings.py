# Generic Django settings
# Part of tekton/tools!
from datetime import timedelta

import os

INSTALL_NAME = "DocuCanvas"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

# Set the project managers to be the same as the admins...
MANAGERS = ADMINS

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'database.txt',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Los_Angeles'

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
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/Media/'

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
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'kx@yh#=m3q6@z6sb2++u2%)vaj7)w6^p^xm96!yl+^(t(g690&'

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

ROOT_URLCONF = 'DocuCanvas.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'DocuCanvas.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates'),
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
    'django.contrib.admindocs',
    ### will be depricated in 1.6, will ahve to find a new way to do this...
    #'django.contrib.markup',
    ### The following are base apps that make things easier...
    'south',
    'gunicorn',
    'djcelery',
    ### other basic modules/apps
    'accounts',)

INSTALLED_APPS += (### Add project specifics apps here
    'markdown',
    'projects',
    'issues',
    'notifications',
    'newsfeed',
    'checklists',
    'dashboard',
    'nodes',
    'daily_reports',
    'boards',
    'food',
    'helpdesknew',
    'gapps',
    'tinymce',
    'charts',
    #'facebook',
    #'twitter',
    'socialplatform',
    'django.contrib.humanize', ## wjmazza - 2013-07-02
    'django.contrib.webdesign', ## wjmazza - 2013-07-09
    'polls',
    'feedback',
    'search',
    'communications',
    'taxes',
    'sprints',
    'system_settings',
    'gitHooks',
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


### Caches and Celery

###  CELERY ###
import djcelery
djcelery.setup_loader()
### given the prevelance of heroku usage, this is just an easy way to use that and fall back to localhost for dev
BROKER_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
# CELERY_RESULT_BACKEND = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
CELERY_IMPORTS = ("communications.views", "accounts.views", "search.views")  # Uncomment line to add where the tasks are! A suggest default is in there
CELERYBEAT_SCHEDULE = {}
CELERY_TASK_SERIALIZER = "json"
### /CELERY ###

TINYMCE_DEFAULT_CONFIG ={
    'theme': 'advanced',
    # 'theme_advanced_toolbar_location': 'top',
    # 'theme_advanced_buttons1': 'bold, italic, underline, separator, outdent, indent, separator, undo, redo',
    # 'theme_advanced_buttons2': '',
    # 'theme_advanced_buttons3': '',
}

'''
    This allows people to have local settings different from default settings; ie e-mail and database settings
'''
try:
    from local_settings import *
except ImportError:
    print("Can't import local settings for some reason...")
