from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'unsubscribed_library/$', 'main_app.views.unsubscribe_library'),
    url(r'subscribed_library/$', 'main_app.views.subscribe_library'),

    url(r'login/$', 'main_app.views.log_in'),
    url(r'get_playlist/$', 'main_app.views.get_playlist'),
    url(r'forgot/$', 'main_app.views.forgot_password'),
    url(r'library/$', 'main_app.views.library'),
    url(r'post/pre_upload/$', 'main_app.views.pre_upload'),
    url(r'post/get_library_upload/$', 'main_app.views.get_library_upload'),
    url(r'post/upload/$', 'main_app.views.post_upload'),
    url(r'post/new_cover/$', 'main_app.views.post_new_cover'),
    url(r'post/new_profile_pix/$', 'main_app.views.post_new_pix'),
    url(r'post/edit_current_user_profile/$', 'main_app.views.edit_current_user_profile'),

    url(r'get_current_user_details/(?P<user_id>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_current_user_details'),
    url(r'get_preview_libraries/(?P<user_id>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_preview_libraries'),
    url(r'get_subscribed_libraries/(?P<user_id>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_subscribed_libraries'),
    url(r'get_subscribed_users/(?P<user_id>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_subscribed_users'),
    url(r'get_explore_libraries/(?P<user_id>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_explore_libraries'),
    url(r'get_user_details/(?P<user_id>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_user_details'),
    url(r'get_user_libraries/$', 'main_app.views.get_user_libraries'),
    url(r'get_library_details/(?P<library_id>[a-zA-Z0-9_.-]+)/(?P<page>[a-zA-Z0-9_.-]+)/(?P<amount>[a-zA-Z0-9_.-]+)/$', 'main_app.views.get_library_details'),
    url(r'get_all_users/$', 'main_app.views.get_all_users'),
    url(r'get_all_libraries/$', 'main_app.views.get_all_libraries'),
    url(r'get_search_results/$', 'main_app.views.get_search_results'),
    url(r'get_explore_users/$', 'main_app.views.get_explore_users'),
    url(r'get_explore_libraries/$', 'main_app.views.get_explore_libraries'),

    url(r'subscribed_user_profile/$', 'main_app.views.subscribed_user_profile'),
    url(r'unsubscribed_user_profile/$', 'main_app.views.unsubscribed_user_profile'),

    url(r'', 'main_app.views.main'),
    )

