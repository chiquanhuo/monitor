from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'monitor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'apps.account.views.redirect'),
    url(r'', include('two_factor.urls', 'two_factor')),
    url(r'^account/login/$', 'apps.account.views.login'),
    url(r'^account/login/submit/$', 'apps.account.views.login'),

    url(
        r'^account/password/change/$',
        'django.contrib.auth.views.password_change',
        {
            'post_change_redirect': '/account/logout/'
        }
    ),

    url(
        r'^account/logout/$', 'django.contrib.auth.views.logout_then_login'
    ),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^account/', include('apps.account.urls')),
    url(r'^monitor/', include('apps.monitor.urls')),

    url(r'^captcha/', include('captcha.urls')),

    url(r'^home/', include('apps.monitor.urls')),
)
