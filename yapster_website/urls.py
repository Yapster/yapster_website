from django.conf.urls import patterns, include, url
from django.contrib import admin
import main_app.urls

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^home/', 'home.views.home'),
                       url(r'^about/', 'home.views.about'),
                       url(r'^press/', 'home.views.press'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^app/', include(main_app.urls)),
                       url(r'^', 'home.views.main'),
                       )
