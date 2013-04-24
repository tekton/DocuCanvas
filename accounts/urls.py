from django.conf.urls import patterns


urlpatterns = patterns('',
    (r'test$', 'accounts.views.oauth_test'),
    (r'oauth2callback$', 'accounts.views.oauth_callback'),
)
