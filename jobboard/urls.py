"""jobboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.contrib.auth.views import (
    login, logout, password_reset, password_reset_complete,
    password_reset_confirm, password_reset_done
)
from django.core.urlresolvers import reverse_lazy

import jobmanagement.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^', include(jobmanagement.urls, namespace='jobmanagement')),  # le namespace se met ici car il s'applique à une famille d'urls
    url(r'^login/?$', login, name='login'),
    url(r'^logout/?$', logout, {'template_name': 'registration/logout.html'},
        name='logout'),
    url(r'^password-reset/?$', password_reset,
        {'post_reset_redirect':
         reverse_lazy('password_reset_done')},
        name='password_reset'),
    url(r'^password-reset/complete?$', password_reset_complete,
        name='password_reset_complete'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        {'post_reset_redirect':
         reverse_lazy('password_reset_complete')},
        name='password_reset_confirm'),
    url(r'^password-reset/done/?$', password_reset_done,
        name='password_reset_done'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]