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

# import djcelery
# djcelery.setup_loader()     #加载djcelery
# BROKER_URL = 'pyamqp://guest@localhost//'    #配置broker
# BROKER_POOL_LIMIT = 0
# CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'  #配置backend

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#项目跟目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# STATIC_URL = '/static/'
#仅有上面的设置，只说明了样式放在static文件，需要指定和项目根目录的关系

#设置项目static地址

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

#设置文件存储位置
FILE_STORE = "D:/work/"
#设置静态文件的目录，设置为列表形式
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR,'static')
# ]

# 文件存储位置为本地/media/spiders_file  还有服务器1、172.31.33.69@/media/spiders_file 2、...
WEB_SERVER_INFO={'Host':'172.31.33.69',
                 'Username':'root',
                 'Password':'syswin#123'}

WEB_SERVER_INFOS = {
    "app1" : {
        "Host" : "172.31.33.69",
        "Username" : "root",
        "Password" : "syswin#123"
         # "Password" :  os.environ.get("app2_password")
        # 由服务器配置文件中读取密码具体参考：http://www.cnblogs.com/longyejiadao/archive/2012/06/28/2567885.html
    },
    "app2" : {
        "ip" : "172.28.50.7",
        "Username" : "root",
        "Password" :  '123456'
    }
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1^=fn5ur^&gj=9l(e26@@^anyi-#miw&@eu4^ab))*zet@%dcl'

# SECURITY WARNING: don't run with debug turned on in production!
#抛出异常到页面，正式项目需关闭
DEBUG = True

# ALLOWED_HOSTS = ["localhost"]


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
    'scheduled_tasks',
    'djcelery',
]

# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

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

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

#静态文件地址
# STATIC_URL = '/static/'




# 第三方 SMTP 服务
mail_host = "smtp.test.163.com"  # 设置服务器
mail_user = "huangxiaoxue"  # 用户名
mail_pass = "Hanson.123"  # 口令

sender = '229396865@qq.com'
# 接收邮件，可设置为你的QQ邮箱或者其他邮箱
# 抄送
cc = []
HANSON = ['229396865@qq.com']

# redis celery
# CELERY STUFF
import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://auth:root@localhost:6379'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  # 定时任务
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = False
CELERYD_CONCURRENCY = 10
CELERYD_MAX_TASKS_PER_CHILD = 1  #  每个worker最多执行1个任务就会被销毁，可防止内存泄露

LOGIN_REDIRECT_URL = '/index/'
UPLOAD_FILE_DIR = os.path.join(BASE_DIR, "people/upload/")
CHANGE_UPLOAD_DIR = os.path.join(BASE_DIR, "change/upload/")
LOG_FILE_DIR = os.path.join(BASE_DIR, "log/")
BACKUP_USER_INFO_DIR = '/home/huangxiaoxue/django/backup/user_info/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
                'format': '%(levelname)s %(asctime)s %(message)s'
                },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter':'standard',
        },
        'people_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':'%s%s' % (LOG_FILE_DIR, 'people.log'),
            'formatter':'standard',
        },
        'report_handler': {
            'level':'DEBUG',
                   'class':'logging.handlers.RotatingFileHandler',
            'filename':'%s%s' % (LOG_FILE_DIR, 'report.log'),
            'formatter':'standard',
        },
        'change_handler': {
            'level':'DEBUG',
                   'class':'logging.handlers.RotatingFileHandler',
            'filename':'%s%s' % (LOG_FILE_DIR, 'change.log'),
            'formatter':'standard',
        },
        'dtmt_handler': {
            'level':'DEBUG',
                   'class':'logging.handlers.RotatingFileHandler',
            'filename':'%s%s' % (LOG_FILE_DIR, 'dtmt.log'),
            'formatter':'standard',
        },
        'scheduled_tasks_handler': {
            'level':'DEBUG',
                   'class':'logging.handlers.RotatingFileHandler',
            'filename':'%s%s' % (LOG_FILE_DIR, 'scheduled_tasks.log'),
            'formatter':'standard',
        },
        'business_query_handler': {
            'level':'DEBUG',
                   'class':'logging.handlers.RotatingFileHandler',
            'filename':'%s%s' % (LOG_FILE_DIR, 'business_query.log'),
            'formatter':'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'people_log':{
            'handlers': ['people_handler'],
            'level': 'INFO',
            'propagate': False
        },
         'report':{
            'handlers': ['report_handler'],
            'level': 'INFO',
                          'propagate': False
        },
         'change':{
            'handlers': ['change_handler'],
            'level': 'INFO',
                          'propagate': False
        },
         'dtmt':{
            'handlers': ['change_handler'],
            'level': 'INFO',
                          'propagate': False
        },
         'scheduled_tasks':{
            'handlers': ['scheduled_tasks_handler'],
            'level': 'INFO',
                          'propagate': False
        },
         'business_query':{
            'handlers': ['business_query_handler'],
            'level': 'INFO',
                          'propagate': False
        },
    }
}