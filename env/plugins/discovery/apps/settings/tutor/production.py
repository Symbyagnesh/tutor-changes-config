from ..production import *

SECRET_KEY = "Gb7oxJPGzNX1QzPYzhPw"
ALLOWED_HOSTS = [
    "discovery",
    "discovery.openelephant.com"
]

PLATFORM_NAME = "OpenElephant"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "discovery",
        "USER": "discovery",
        "PASSWORD": "YiXGMUKu",
        "HOST": "mysql",
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

ELASTICSEARCH_DSL['default'].update({
    'hosts': "http://elasticsearch:9200/"
})



CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "KEY_PREFIX": "discovery",
        "LOCATION": "redis://@redis:6379/1",
    }
}

# Some openedx language codes are not standard, such as zh-cn
LANGUAGE_CODE = {
    "zh-cn": "zh-hans",
    "zh-hk": "zh-hant",
    "zh-tw": "zh-hant",
}.get("en", "en")
PARLER_DEFAULT_LANGUAGE_CODE = LANGUAGE_CODE
PARLER_LANGUAGES[1][0]["code"] = LANGUAGE_CODE
PARLER_LANGUAGES["default"]["fallbacks"] = [PARLER_DEFAULT_LANGUAGE_CODE]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_PRODUCT_SOURCE_SLUG = "edx"
EMAIL_HOST = "smtp"
EMAIL_PORT = "8025"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False

# Get rid of the "local" handler
LOGGING["handlers"].pop("local")
for logger in LOGGING["loggers"].values():
    if "local" in logger["handlers"]:
        logger["handlers"].remove("local")
# Decrease verbosity of algolia logger
LOGGING["loggers"]["algoliasearch_django"] = {"level": "WARNING"}

OAUTH_API_TIMEOUT = 5

import json
JWT_AUTH["JWT_ISSUER"] = "https://openelephant.com/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "v4rDen3yNpHEmmp1p0aVvZ6y"
# TODO assign a discovery-specific public key
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "vyl0MFi-vkqNDlsktTBgoqLhcqXJB5fkSV-f8pwKdRS3DoXpa2KpTMG3l8xQKg3s4XaA2S2K_EFsof924eRAvixvpP9k-VPnGXLYNoZdIbM6tfRC2i7e7JO47gC544ncxsITLWj0lg_i1Tv4hVUJZlRf5ONtqCxvSaUCu_sXzty0hH-9mp3wb0hhwCzXePWIJbjgnRLhro1G3kRjPtnw4SBXruJ8NzQJSIhS_0KMYD7q7zATZvUWYgf5Qk6DCdG8FhAu2DjyO_U-rTIcElPQo-8Zu5d0IqtFgwVEDTHiNVJ9H7lk3719I5ChsH20Vsorhrvey-6qPEU6CxZ3YzgeoQ",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "https://openelephant.com/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "v4rDen3yNpHEmmp1p0aVvZ6y"
    }
]

EDX_DRF_EXTENSIONS = {
    'OAUTH2_USER_INFO_URL': 'https://openelephant.com/oauth2/user_info',
}



BACKEND_SERVICE_EDX_OAUTH2_KEY = "discovery"
BACKEND_SERVICE_EDX_OAUTH2_SECRET = "PjZuQfle"
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = "http://lms:8000/oauth2"

SOCIAL_AUTH_EDX_OAUTH2_KEY = "discovery-sso"
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "sCj1BP1u"
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = "https://openelephant.com"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = SOCIAL_AUTH_EDX_OAUTH2_ISSUER + "/logout"

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

DISCOVERY_BASE_URL = "https://discovery.openelephant.com"
MEDIA_URL = DISCOVERY_BASE_URL + "/media/"

