from django.conf.urls import patterns


urlpatterns = patterns('',
    (r'^$', 'accounts.views.oauth_start'),
    (r'test$', 'accounts.views.oauth_test'),
    (r'authorize$', 'accounts.views.oauth_authorize'),
    (r'oauth2callback$', 'accounts.views.oauth_callback'),
)
