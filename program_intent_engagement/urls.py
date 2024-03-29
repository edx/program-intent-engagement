"""
program_intent_engagement URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

import os

from auth_backends.urls import oauth2_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

from program_intent_engagement.apps.api import urls as api_urls
from program_intent_engagement.apps.core import views as core_views

admin.autodiscover()

urlpatterns = oauth2_urlpatterns + [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('api-docs/', get_swagger_view(title='program-intent-engagement API')),
    path('auto_auth/', core_views.AutoAuth.as_view(), name='auto_auth'),
    path('', include('csrf.urls')),  # Include csrf urls from edx-drf-extensions
    path('health/', core_views.health, name='health'),
]

if settings.DEBUG and os.environ.get('ENABLE_DJANGO_TOOLBAR', False):  # pragma: no cover
    # Disable pylint import error because we don't install django-debug-toolbar
    # for CI build
    import debug_toolbar  # isort:skip pylint: disable=import-error,useless-suppression
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
