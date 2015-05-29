from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'share_yap/(?P<yap_id>[a-zA-Z0-9_.-]+)/$', 'share.views.share_yap'),
    )