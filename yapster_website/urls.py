from django.conf.urls import patterns, include, url
from django.contrib import admin
from home.views import home

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^home/', 'home.views.home'),
                       url(r'^about/', 'home.views.about'),
                       url(r'^press/', 'home.views.press'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', 'home.views.main'),
                       )
