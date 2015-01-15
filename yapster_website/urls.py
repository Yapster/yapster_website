from django.conf.urls import patterns, include, url
from django.contrib import admin
import content_manager.urls

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^home/', 'home.views.home'),
                       url(r'^about/', 'home.views.about'),
                       url(r'^press/', 'home.views.press'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^manager/', include(content_manager.urls)),
                       url(r'^', 'home.views.main'),
                       )
