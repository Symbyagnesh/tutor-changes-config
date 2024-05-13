# -*- coding: utf-8 -*-
import os
from lms.envs.production import *

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "db": "openedx",
    "host": "mongodb",
    "port": 27017,
    "user": None,
    "password": None,
    # Connection/Authentication
    "connect": False,
    "ssl": False,
    "authsource": "admin",
    "replicaSet": None,
    
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Elasticsearch connection parameters
ELASTIC_SEARCH_CONFIG = [{
  
  "host": "elasticsearch",
  "port": 9200,
}]

# Common cache config
CACHES = {
    "default": {
        "KEY_PREFIX": "default",
        "VERSION": "1",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "general": {
        "KEY_PREFIX": "general",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "mongo_metadata_inheritance": {
        "KEY_PREFIX": "mongo_metadata_inheritance",
        "TIMEOUT": 300,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "configuration": {
        "KEY_PREFIX": "configuration",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "celery": {
        "KEY_PREFIX": "celery",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "course_structure_cache": {
        "KEY_PREFIX": "course_structure",
        "TIMEOUT": 604800, # 1 week
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "ora2-storage": {
        "KEY_PREFIX": "ora2-storage",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    }
}

# The default Django contrib site is the one associated to the LMS domain name. 1 is
# usually "example.com", so it's the next available integer.
SITE_ID = 2

# Contact addresses
CONTACT_MAILING_ADDRESS = "EdLearn - https://edlearn.in"
DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

# ORA2
ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
FILE_UPLOAD_STORAGE_BUCKET_NAME = "openedxuploads"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]

# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)
LOGGING["loggers"]["blockstore.apps.bundles.storage"] = {"handlers": ["console"], "level": "WARNING"}

# These warnings are visible in simple commands and init tasks
import warnings

from django.utils.deprecation import RemovedInDjango50Warning, RemovedInDjango51Warning
warnings.filterwarnings("ignore", category=RemovedInDjango50Warning)
warnings.filterwarnings("ignore", category=RemovedInDjango51Warning)

warnings.filterwarnings("ignore", category=DeprecationWarning, module="wiki.plugins.links.wiki_plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="boto.plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="botocore.vendored.requests.packages.urllib3._collections")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fs")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fs.opener")
SILENCED_SYSTEM_CHECKS = ["2_0.W001", "fields.W903"]

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LOCALE_PATHS.append("/openedx/locale/contrib/locale")
LOCALE_PATHS.append("/openedx/locale/user/locale")
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "https://edlearn.in/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "v4rDen3yNpHEmmp1p0aVvZ6y"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "F5EVPWabcVtAg44R-vJxX2uELr2oiHKd1rvevKqnEWMR5Ez3B2Gc7JUPPLwX_-9CjlMtNFkMgufP7DLR5axdnPReeTFxMdm5qmYBqMsszRxK9yabXUmc-v6FNHZLdHVJDgncEmOXj656sP4ZN9rRc1egkNfG64461BHvQdyFRV-yda3DvD0TWftf9VtuKM9mMREm99HWtyw30zI0DZEuchNSvihcLsqba38O_ebyoT-LMZH4ZphDJZK0l_c4K7TA251CyuwKJ1mz34IHA4ZMs6Xf3R7Ttgxqt0Rcpi1EwSt_S-IAzkzn5mvPs7rtelyRO8zudKSXwHMMElH7xL52Hw",
        "n": "vyl0MFi-vkqNDlsktTBgoqLhcqXJB5fkSV-f8pwKdRS3DoXpa2KpTMG3l8xQKg3s4XaA2S2K_EFsof924eRAvixvpP9k-VPnGXLYNoZdIbM6tfRC2i7e7JO47gC544ncxsITLWj0lg_i1Tv4hVUJZlRf5ONtqCxvSaUCu_sXzty0hH-9mp3wb0hhwCzXePWIJbjgnRLhro1G3kRjPtnw4SBXruJ8NzQJSIhS_0KMYD7q7zATZvUWYgf5Qk6DCdG8FhAu2DjyO_U-rTIcElPQo-8Zu5d0IqtFgwVEDTHiNVJ9H7lk3719I5ChsH20Vsorhrvey-6qPEU6CxZ3YzgeoQ",
        "p": "yzdo1vxBZNjrOX4SqS9xmh5omS9lJDDDgT3xiirYMtrYE5ZON-T9K7z3LslnLVVuHIRJytKSCChaAr-M0vnjyhBsrBWnbqEyzc_YHQ5IdVeIHtvpqnyoKR0CAYFpQ4hOswR0tT1byg_eVh_xMQLByRI6n3uyN8g3PFdUP-8Nmk8",
        "q": "8NB_FZNrl8S6WFlQrb-y81IwxF0hGsmxJxeqLhzKwJlG5Llw-YYKwMWVRtftowAp-FlndvbwOJPkTDKhfcfAztL0X8opjYJ2Ku3Mnc3eY2VJ3Gidrl8c1LR-jKgEieBiXuNJevrW_dPgPBXL7JfKOy-BWaAk_NIqdZ5msPmRrA8",
        "dq": "g43C_yxryJtGGWGhe2mP_vDVh1BA93tbdbmt1EcSVCjn26eamhWp5imKJQts3HEIfI2KwiigjqfsPdwi8K2hHNuNeI7eKFou58DE2ShP5wi8UtYr3chD3cdEot5erFuSIbgUukQyErQeeXSG1JcPeUm4ZhfgXOULIPoJq4CLHe0",
        "dp": "LnMn35whRm_etHGAynMxwEybFAilUbRju7Lw9uf8KwOiyDdfAZ-xzsGOrn8SumYAmTwTseyXvI2cpWwrQD4mNxWyAVOhxcPK3QhZGaseHNQ5JPSXYITF2z_qKXXvHaSWeIzYMGUqCfG-nGkItG8w5EjqZXHctqtpFL3RYBvAPDk",
        "qi": "X5v3bzk_5eHnHJUJXMyXmH3rT9tdopigSBewt0kPVTuPGZHHgg9SX6ryQpCaGZwOlHOdg1DjFFno9BP-JsQxFXH8zkODeChygb25gPuH4OmEmpfxrZKwSar4PTElwbalJg4mV_52m-eRfmTTJ9Qqz-eHvpmQzRYjq8GVEgHgpbs",
    }
)
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
        "ISSUER": "https://edlearn.in/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "v4rDen3yNpHEmmp1p0aVvZ6y"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False
FEATURES["ENABLE_CORS_HEADERS"] = True

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_INSECURE = False
CORS_ALLOW_HEADERS = corsheaders_default_headers + ('use-jwt-cookie',)

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}

FEATURES["ENABLE_DISCUSSION_SERVICE"] = True
######## End of settings common to LMS and CMS

######## Common LMS settings
LOGIN_REDIRECT_WHITELIST = ["studio.edlearn.in"]

# Better layout of honor code/tos links during registration
REGISTRATION_EXTRA_FIELDS["terms_of_service"] = "hidden"
REGISTRATION_EXTRA_FIELDS["honor_code"] = "hidden"

# Fix media files paths
PROFILE_IMAGE_BACKEND["options"]["location"] = os.path.join(
    MEDIA_ROOT, "profile-images/"
)

COURSE_CATALOG_VISIBILITY_PERMISSION = "see_in_catalog"
COURSE_ABOUT_VISIBILITY_PERMISSION = "see_about_page"

# Allow insecure oauth2 for local interaction with local containers
OAUTH_ENFORCE_SECURE = False

# Email settings
DEFAULT_EMAIL_LOGO_URL = LMS_ROOT_URL + "/theming/asset/images/logo.png"
BULK_EMAIL_SEND_USING_EDX_ACE = True
FEATURES["ENABLE_FOOTER_MOBILE_APP_LINKS"] = False

# Branding
MOBILE_STORE_ACE_URLS = {}
SOCIAL_MEDIA_FOOTER_ACE_URLS = {}

# Make it possible to hide courses by default from the studio
SEARCH_SKIP_SHOW_IN_CATALOG_FILTERING = False

# Caching
CACHES["staticfiles"] = {
    "KEY_PREFIX": "staticfiles_lms",
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "staticfiles_lms",
}

# Create folders if necessary
for folder in [DATA_DIR, LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE, ORA2_FILEUPLOAD_ROOT]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

FEATURES['ENABLE_SPECIAL_EXAMS'] = True
SKIP_EMAIL_VALIDATION = True
FEATURES["ENABLE_COURSE_DISCOVERY"] = True
# MFE: enable API and set a low cache timeout for the settings. otherwise, weird
# configuration bugs occur. Also, the view is not costly at all, and it's also cached on
# the frontend. (5 minutes, hardcoded)
ENABLE_MFE_CONFIG_API = True
MFE_CONFIG_API_CACHE_TIMEOUT = 1

# MFE-specific settings

FEATURES['ENABLE_AUTHN_MICROFRONTEND'] = True


FEATURES['ENABLE_NEW_BULK_EMAIL_EXPERIENCE'] = True


LEARNER_HOME_MFE_REDIRECT_PERCENTAGE = 100


######## End of common LMS settings

ALLOWED_HOSTS = [
    ENV_TOKENS.get("LMS_BASE"),
    FEATURES["PREVIEW_LMS_BASE"],
    "lms",
]
CORS_ORIGIN_WHITELIST.append("https://edlearn.in")


# Properly set the "secure" attribute on session/csrf cookies. This is required in
# Chrome to support samesite=none cookies.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"


# CMS authentication
IDA_LOGOUT_URI_LIST.append("https://studio.edlearn.in/logout/")

# Required to display all courses on start page
SEARCH_SKIP_ENROLLMENT_START_DATE_FILTERING = True

# Dynamic config API settings
# https://openedx.github.io/frontend-platform/module-Config.html
MFE_CONFIG = {
    "BASE_URL": "apps.edlearn.in",
    "CSRF_TOKEN_API_PATH": "/csrf/api/v1/token",
    "CREDENTIALS_BASE_URL": "",
    "DISCOVERY_API_BASE_URL": "https://discovery.edlearn.in",
    "FAVICON_URL": "https://edlearn.in/favicon.ico",
    "INFO_EMAIL": "contact@example.com",
    "LANGUAGE_PREFERENCE_COOKIE_NAME": "openedx-language-preference",
    "LMS_BASE_URL": "https://edlearn.in",
    "LOGIN_URL": "https://edlearn.in/login",
    "LOGO_URL": "https://edlearn.in/theming/asset/images/logo.png",
    "LOGO_WHITE_URL": "https://edlearn.in/theming/asset/images/logo.png",
    "LOGO_TRADEMARK_URL": "https://edlearn.in/theming/asset/images/logo.png",
    "LOGOUT_URL": "https://edlearn.in/logout",
    "MARKETING_SITE_BASE_URL": "https://edlearn.in",
    "PASSWORD_RESET_SUPPORT_LINK": "mailto:contact@example.com",
    "REFRESH_ACCESS_TOKEN_ENDPOINT": "https://edlearn.in/login_refresh",
    "SITE_NAME": "EdLearn",
    "STUDIO_BASE_URL": "https://studio.edlearn.in",
    "USER_INFO_COOKIE_NAME": "user-info",
    "ACCESS_TOKEN_COOKIE_NAME": "edx-jwt-cookie-header-payload",
}

# MFE-specific settings


AUTHN_MICROFRONTEND_URL = "https://apps.edlearn.in/authn"
AUTHN_MICROFRONTEND_DOMAIN  = "apps.edlearn.in/authn"
MFE_CONFIG["DISABLE_ENTERPRISE_LOGIN"] = True



ACCOUNT_MICROFRONTEND_URL = "https://apps.edlearn.in/account/"
MFE_CONFIG["ACCOUNT_SETTINGS_URL"] = ACCOUNT_MICROFRONTEND_URL



MFE_CONFIG["ENABLE_NEW_EDITOR_PAGES"] = True
MFE_CONFIG["ENABLE_PROGRESS_GRAPH_SETTINGS"] = True
MFE_CONFIG["COURSE_AUTHORING_MICROFRONTEND_URL"] = "https://apps.edlearn.in/course-authoring"



DISCUSSIONS_MICROFRONTEND_URL = "https://apps.edlearn.in/discussions"
MFE_CONFIG["DISCUSSIONS_MFE_BASE_URL"] = DISCUSSIONS_MICROFRONTEND_URL
DISCUSSIONS_MFE_FEEDBACK_URL = None



WRITABLE_GRADEBOOK_URL = "https://apps.edlearn.in/gradebook"



LEARNER_HOME_MICROFRONTEND_URL = "https://apps.edlearn.in/learner-dashboard/"



LEARNING_MICROFRONTEND_URL = "https://apps.edlearn.in/learning"
MFE_CONFIG["LEARNING_BASE_URL"] = "https://apps.edlearn.in/learning"



ORA_GRADING_MICROFRONTEND_URL = "https://apps.edlearn.in/ora-grading"



PROFILE_MICROFRONTEND_URL = "https://apps.edlearn.in/profile/u/"
MFE_CONFIG["ACCOUNT_PROFILE_URL"] = "https://apps.edlearn.in/profile"



COMMUNICATIONS_MICROFRONTEND_URL = "https://apps.edlearn.in/communications"
MFE_CONFIG["SCHEDULE_EMAIL_SECTION"] = True


LOGIN_REDIRECT_WHITELIST.append("apps.edlearn.in")
CORS_ORIGIN_WHITELIST.append("https://apps.edlearn.in")
CSRF_TRUSTED_ORIGINS.append("https://apps.edlearn.in")


