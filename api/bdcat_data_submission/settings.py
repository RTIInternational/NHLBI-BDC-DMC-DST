"""
Django settings for BioData Catalyst Data Submission Tool project.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(env_file):
    print(
        "Using local .env file: " + env_file
    )
    # if local env file
    env.read_env(env_file)
else:
    print(
        "No local .env detected. Using container environment variables."
    )

# Set variables from .env file or container environment
DEBUG = env("DEBUG") == True
DEPLOYED = env("DEPLOYED") == True
SECRET_KEY = env("SECRET_KEY")
AWS_SITE_URL = env("AWS_SITE_URL")

JIRA_BASE_URL = env("JIRA_BASE_URL")
JIRA_TOKEN = env("JIRA_TOKEN")
JIRA_BOARD_ID = env("JIRA_BOARD_ID")
JIRA_PROJECT = env("JIRA_PROJECT")
JIRA_EPIC_ISSUETYPE = env("JIRA_EPIC_ISSUETYPE")

FRESHDESK_BASE_URL = env("FRESHDESK_BASE_URL")
FRESHDESK_AUTH_USER = env("FRESHDESK_AUTH_USER")
FRESHDESK_AUTH_PASSWORD = env("FRESHDESK_AUTH_PASSWORD")
FRESHDESK_GROUP_ID = env("FRESHDESK_GROUP_ID")

AWS_SITE_URL = env("AWS_SITE_URL")

# Application definition

INSTALLED_APPS = [
    "tracker",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "widget_tweaks",
    # all auth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # custom nih sso provider
    "nihsso",
    # audit log
    "simple_history",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "tracker.middleware.CustomHeaderMiddleware",
    "allauth.account.middleware.AccountMiddleware"
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "templates", "allauth"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

TEST_RUNNER = 'testrunner.GetStaticTestRunner'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} [{module}] {message}',
            'style': '{',
        },
    },
    "handlers": { 
        "console": {
            "level": os.getenv("DJANGO_LOG_LEVEL", "DEBUG"),
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },        
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "DEBUG"),
            "propagate": True,
        },
    },
}

# Enable debug tools if DEBUG is True
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

# SECURITY WARNING: App Engine's security features ensure that it is safe to
# have ALLOWED_HOSTS = ['*'] when the app is deployed. If you deploy a Django
# app not on App Engine, make sure to set an appropriate host here
ALLOWED_HOSTS = ["*"]

# Check if we're running in a Docker container
if os.environ.get("SUMMARY", None):
    postgres_host = os.environ.get("POSTGRES_HOST")
else:
    postgres_host = "localhost"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
if os.environ.get("POSTGRES_HOST", None):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": env("POSTGRES_DB"),
            "USER": env("POSTGRES_USER"),
            "PASSWORD": env("POSTGRES_PASSWORD"),
            "HOST": env("POSTGRES_HOST"),
            "PORT": env("POSTGRES_PORT"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# django-allauth
# https://github.com/pennersr/django-allauth
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_PROVIDERS = {}

if os.environ.get("NIH_CLIENT_ID", None):
    nih_settings = {
        "SCOPE": ["openid", "profile", "email", "member"],
        "APP": {
            "client_id": env("NIH_CLIENT_ID"),
            "secret": env("NIH_CLIENT_SECRET"),
            "key": "",
        },
    }
    SOCIALACCOUNT_PROVIDERS['nihsso'] = nih_settings
    NIH_OAUTH_SERVER_TOKEN_URL = os.environ.get("NIH_OAUTH_SERVER_TOKEN_URL")
    NIH_OAUTH_SERVER_INFO_URL = os.environ.get("NIH_OAUTH_SERVER_INFO_URL")
    NIH_OAUTH_SERVER_AUTH_URL = os.environ.get("NIH_OAUTH_SERVER_AUTH_URL")
    print("Adding NIH SSO as an Account Provider")

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "development_backend.DevelopmentBackend",
    # NOTE: Deployment
    # Commented out the allauth backend to allow to run for dev. Uncomment for production/deployment.
    #    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = int(os.environ.get("ALLAUTH_SITE_ID", 3))
AUTH_USER_MODEL = "tracker.User"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"


ACCOUNT_DEFAULT_HTTP_PROTOCOL = os.environ.get("ACCOUNT_DEFAULT_HTTP_PROTOCOL", "https")
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_ADAPTER = "nihsso.adapters.NIHSSOSocialAccountAdapter"

SESSION_COOKIE_AGE = 30 * 60  # 30 minutes in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

if DEPLOYED:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSRF_TRUSTED_ORIGINS = [AWS_SITE_URL]
    

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_L10N = True
USE_TZ = True

DATE_FORMAT = 'N j, Y, P T'
DATETIME_FORMAT = 'N j, Y, P T'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Whitenoise
WHITENOISE_AUTOREFRESH = True
WHITENOISE_MANIFEST_STRICT = False


# Misc
ROOT_URLCONF = "bdcat_data_submission.urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
WSGI_APPLICATION = "bdcat_data_submission.wsgi.application"
