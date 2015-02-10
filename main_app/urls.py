from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'login/$', 'main_app.views.log_in'),
    url(r'get_playlist/$', 'main_app.views.get_playlist'),
    url(r'forgot/$', 'main_app.views.forgot_password'),
    url(r'library/$', 'main_app.views.library'),
    url(r'post/upload/$', 'main_app.views.post_upload'),

    url(r'get_current_user_details/(?P<user_id>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_current_user_details'),
    url(r'get_preview_libraries/(?P<user_id>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_preview_libraries'),
    url(r'get_subscribed_libraries/(?P<user_id>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_subscribed_libraries'),
    url(r'get_subscribed_users/(?P<user_id>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_subscribed_users'),
    url(r'get_explore_libraries/(?P<user_id>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_explore_libraries'),
    url(r'get_user_details/(?P<user_id>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_user_details'),
    url(r'get_user_libraries/(?P<user_id>[a-zA-Z0-9_.-]+)/(?P<page>[a-zA-Z0-9_.-]+)/(?P<amount>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_user_libraries'),
    url(r'get_library_details/(?P<library_id>[a-zA-Z0-9_.-]+)/(?P<page>[a-zA-Z0-9_.-]+)/(?P<amount>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_library_details'),
    url(r'get_playlist/(?P<library_id>[a-zA-Z0-9_.-]+)/(?P<yap_id>[a-zA-Z0-9_.-]+)/(?P<page>[a-zA-Z0-9_.-]+)/(?P<amount>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_playlist'),
    url(r'', 'main_app.views.main'),
    )