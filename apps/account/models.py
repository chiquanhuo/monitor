#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField

class CaptchaUserAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField()
