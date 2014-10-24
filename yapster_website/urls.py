from django.conf.urls import patterns, include, url
from django.contrib import admin
from home.views import home

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', 'home.views.main'),
    url(r'^home/', 'home.views.home'),
    url(r'^admin/', include(admin.site.urls)),
)
