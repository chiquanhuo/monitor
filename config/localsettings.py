#!/usr/bin/env python
#-*- coding: utf-8 -*-


ADMIN_DATABASE = "default"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'youmi_monitor',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '172.16.2.2',
        'PORT': '3306',
    },
    'youmi_admin': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'youmi_admin',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '172.16.2.2',
        'PORT': '3306',
    },
}

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DBNAME = 'ym_debug_msg'
MONGO_COLLECTION = 'debug_monitor_ad'
