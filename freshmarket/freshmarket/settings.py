"""
Django settings for freshmarket project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2%efxbt9daw#e_(cm9&o_y_i6ts$rjq)qt&jk97=&b_q#e%i&3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'simpleui',
    'tinymce', #富文本编辑器
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'goods',
    'order',
    'cart',
    'storages',
    'haystack',  # 导入搜索功能模块

]



#后台美化代码
SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode
    'iframe': True,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # Using Summernote Air-mode
    'airMode': False,

    # Use native HTML tags (`<b>`, `<i>`, ...) instead of style attributes
    'styleWithSpan': False,

    # Change editor size
    'width': '80%',
    'height': '480',

    # Use proper language setting automatically (default)
    'lang': 'zh-CN',
}

#富文本编辑器的配置
# settings.py
TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 800,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
        ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            link image media | codesample
        ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor | code
        ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'freshmarket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'freshmarket.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',      # 虚拟环境下的引擎
        'HOST': 'localhost',      # 主机
        'PORT': '3306',           # 端口
        'USER': 'root',           # 用户名
        'PASSWORD': 'As20010504', # 密码
        'NAME': 'dailyfresh1',   # 使用的数据库
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

#静态文件的配置
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#自定义模型
AUTH_USER_MODEL = 'user.User'


#发送邮件服务器配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True  # 推荐使用 SSL
EMAIL_HOST_USER = '2197381455@qq.com'
EMAIL_HOST_PASSWORD = 'sgcaxewrbunaeadf'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#Celery 配置

#CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'




#Django的缓存配置

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # 如果 Redis 设置了密码，取消注释并填入
            # "PASSWORD": "your_password",
        }
    }
}

SESSION_CACHE_ALIAS = "default"
SESSION_ENGINE = "django.contrib.sessions.backends.cache"




LOGIN_URL = '/user/login'



# MinIO  服务器配置
AWS_ACCESS_KEY_ID = 'admin'      # 替换成你的 Access Key
AWS_SECRET_ACCESS_KEY = 'admin123'  # 替换成你的 Secret Key
AWS_STORAGE_BUCKET_NAME = 'django-files'  # 你在 MinIO 上创建的桶名
AWS_S3_ENDPOINT_URL = 'http://192.168.192.158:9000/'  # MinIO 地址（注意是 http 或 https）
AWS_S3_REGION_NAME = 'us-east-1'  # 任意字符串即可，因为 MinIO 不区分区域
AWS_S3_SIGNATURE_VERSION = 's3v4'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = 'http://192.168.144.158:9000/django-files/'


#搜索功能配置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'goods.whoosh_backend_cn.WhooshEngine',  #搜索引擎
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),  # 设置索引路径
    },
}

# 指定实时更新索引，当有数据发生改变时，自动更新索引

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

