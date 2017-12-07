"""
Django settings for DSPProject project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
# import MySQLdb
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#项目跟目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# STATIC_URL = '/static/'
#仅有上面的设置，只说明了样式放在static文件，需要指定和项目根目录的关系

#设置静态文件的目录，设置为列表形式
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1^=fn5ur^&gj=9l(e26@@^anyi-#miw&@eu4^ab))*zet@%dcl'

# SECURITY WARNING: don't run with debug turned on in production!
#抛出异常到页面，正式项目需关闭
DEBUG = True

ALLOWED_HOSTS = ["localhost"]


# Application definition

#Django 应用 apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'message',
]

#工具集
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#url根文件
ROOT_URLCONF = 'DSPProject.urls'

#模板
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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


WSGI_APPLICATION = 'DSPProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
#数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', #主要是这里，将默认的sqlite3改为mysql
        'NAME': "spidertool", #数据库的名字
        'USER': "root",#数据库用户名
        'PASSWORD': "123456",#数据库密码
        'HOST':"localhost",
        # 'HOST': "172.31.33.60",#数据库地址，默认本 机
        'PORT': "3306",#数据库端口，默认3306
    }
}



# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


#
# 作者：海贼之路飞
# 链接：http://www.jianshu.com/p/335121af76d3
# 來源：简书
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
#
# # Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

#静态文件地址
STATIC_URL = '/static/'
