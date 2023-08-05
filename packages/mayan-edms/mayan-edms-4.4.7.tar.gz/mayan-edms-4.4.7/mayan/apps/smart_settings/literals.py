from django.conf import global_settings

COMMAND_NAME_SETTINGS_REVERT = 'settings_revert'
COMMAND_NAME_SETTINGS_SAVE = 'settings_save'

CONFIGURATION_FILENAME = 'config.yml'
CONFIGURATION_LAST_GOOD_FILENAME = 'config_backup.yml'

DEFAULT_ALLOWED_HOSTS = global_settings.ALLOWED_HOSTS
DEFAULT_APPEND_SLASH = global_settings.APPEND_SLASH
DEFAULT_AUTH_PASSWORD_VALIDATORS = global_settings.AUTH_PASSWORD_VALIDATORS
DEFAULT_AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS
DEFAULT_DATABASES = global_settings.DATABASES
DEFAULT_DATA_UPLOAD_MAX_MEMORY_SIZE = global_settings.DATA_UPLOAD_MAX_MEMORY_SIZE
DEFAULT_DEFAULT_FROM_EMAIL = global_settings.DEFAULT_FROM_EMAIL
DEFAULT_DISALLOWED_USER_AGENTS = global_settings.DISALLOWED_USER_AGENTS
DEFAULT_EMAIL_BACKEND = global_settings.EMAIL_BACKEND
DEFAULT_EMAIL_HOST = global_settings.EMAIL_HOST
DEFAULT_EMAIL_HOST_PASSWORD = global_settings.EMAIL_HOST_PASSWORD
DEFAULT_EMAIL_HOST_USER = global_settings.EMAIL_HOST_USER
DEFAULT_EMAIL_PORT = global_settings.EMAIL_PORT
DEFAULT_EMAIL_TIMEOUT = global_settings.EMAIL_TIMEOUT
DEFAULT_EMAIL_USE_SSL = global_settings.EMAIL_USE_SSL
DEFAULT_EMAIL_USE_TLS = global_settings.EMAIL_USE_TLS
DEFAULT_FILE_UPLOAD_MAX_MEMORY_SIZE = global_settings.FILE_UPLOAD_MAX_MEMORY_SIZE
DEFAULT_LOGIN_URL = global_settings.LOGIN_URL
DEFAULT_LOGIN_REDIRECT_URL = global_settings.LOGIN_REDIRECT_URL
DEFAULT_LOGOUT_REDIRECT_URL = global_settings.LOGOUT_REDIRECT_URL
DEFAULT_INTERNAL_IPS = global_settings.INTERNAL_IPS
DEFAULT_LANGUAGES = global_settings.LANGUAGES
DEFAULT_LANGUAGE_CODE = global_settings.LANGUAGE_CODE
DEFAULT_SESSION_COOKIE_NAME = global_settings.SESSION_COOKIE_NAME
DEFAULT_SESSION_ENGINE = global_settings.SESSION_ENGINE
DEFAULT_SECURE_PROXY_SSL_HEADER = global_settings.SECURE_PROXY_SSL_HEADER
DEFAULT_STATIC_URL = global_settings.STATIC_URL
DEFAULT_STATICFILES_STORAGE = global_settings.STATICFILES_STORAGE
DEFAULT_TIME_ZONE = global_settings.TIME_ZONE
DEFAULT_USE_X_FORWARDED_HOST = global_settings.USE_X_FORWARDED_HOST
DEFAULT_USE_X_FORWARDED_PORT = global_settings.USE_X_FORWARDED_PORT
DEFAULT_WSGI_APPLICATION = global_settings.WSGI_APPLICATION

NAMESPACE_VERSION_INITIAL = '0001'
SMART_SETTINGS_NAMESPACES_NAME = 'SMART_SETTINGS_NAMESPACES'
