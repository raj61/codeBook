"""
Definition of urls for DjangoWebProject2.
"""

from datetime import datetime
from django.conf.urls import url
from django.conf.urls import include
import django.contrib.auth.views
from django.contrib import admin
import app.views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^api/institute/$',app.views.institute_list,name='api_institute_list'),
    url(r'^api/institute/(?P<pk>[0-9]+)$',app.views.Institute_detail,name='api_institute_detail'),
    url(r'^api/users/$',app.views.user_list,name='api_user_list'),
    url(r'^profile$',app.views.profiledefault),
     url(r'^profile/(?P<user>[a-z0-9]+)$',app.views.profile,name='profile'),
    url(r'^profile/complete/$', app.views.addProfile, name='addProfile'),
    # url(r'^profile/$',app.views.profile,name='profile'),
    url(r'^leaderboard$',app.views.leaderboard,name='leaderboard'),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^accounts/', include('registration.backends.default.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)
