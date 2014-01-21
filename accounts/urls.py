from django.conf.urls import patterns


urlpatterns = patterns('accounts.views',
    (r'^$', 'oauth_start'),
    (r'^save$', 'save_settings'),
    (r'revoke', 'oauth_revoke_auth'),
    (r'authorize$', 'oauth_authorize'),
    (r'oauth2callback$', 'oauth_callback'),
    (r'template', 'assignTemplateForView'),
    (r'settings/toggle/(.*)/(.*)', 'settings_update'),
    (r'settings/(.*)', 'settings_update'),
)
