from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'login/$', 'content_manager.views.log_in'),
    url(r'forgot/$', 'content_manager.views.forgot_password'),
    url(r'library/$', 'content_manager.views.library'),
    url(r'post/upload/$', 'content_manager.views.post_upload'),
    url(r'', 'content_manager.views.main'),
    )