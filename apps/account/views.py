#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.shortcuts import render_to_response
from apps.account.models import CaptchaUserAuthenticationForm
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User

DATE_PATTERN = '%Y-%m-$d'


def redirect(request):
    if request.user:
        return HttpResponseRedirect(
            settings.LOGIN_REDIRECT_URL
        )
    else:
        return HttpResponseRedirect('/account/login/')


def login(request):
    data = {}
    username = request.GET.get('username', '')
    form = CaptchaUserAuthenticationForm(data={'username': username})
    if request.GET.get('newsn') == '1':
        csn = CaptchaStore.generate_key()
        cimageurl = captcha_image_url(csn)
        return HttpResponse(cimageurl)

    if request.method == 'POST':
        post = request.POST.copy()
        redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
        if not redirect_to:
            redirect_to = '/home/'

        form = CaptchaUserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = User.objects.filter(username=post['username'])
            if user.exists():
                auth_login(request, form.get_user())

                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                return HttpResponseRedirect(redirect_to)
            else:
                return HttpResponseRedirect(
                    "/account/login/?error=403&next=%s&username=%s"
                    % (
                        redirect_to,
                        post['username']
                    )
                )
        else:
            print form.errors
            return HttpResponseRedirect('/account/login/')
    else:
        form = CaptchaUserAuthenticationForm()

        data['error'] = request.REQUEST.get("error", "")
        data['next'] = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
        data['form'] = form
        return render_to_response(
            'account/login.html',
            data,
            context_instance=RequestContext(request)
        )


def logout(request):
    """登出用户"""
    auth_logout(request)
    return HttpResponse(
        "/account/login/?error=登出成功"
    )
