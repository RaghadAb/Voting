from QuickPoll.settings.common import *

# Disable password strength check in dev
AUTH_PASSWORD_VALIDATORS = []

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
