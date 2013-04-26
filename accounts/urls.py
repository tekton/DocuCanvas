from django.conf.urls import patterns


urlpatterns = patterns('accounts.views',
    (r'^$', 'oauth_start'),
    (r'test$', 'oauth_test'),
    (r'gplus$', 'oauth_gplus_moment'),
    (r'revoke', 'oauth_revoke_auth'),
    (r'authorize$', 'oauth_authorize'),
    (r'oauth2callback$', 'oauth_callback'),
)
