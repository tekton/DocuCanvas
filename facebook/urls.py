from django.conf.urls import *

urlpatterns = patterns('',
    (r'^getAccessToken$', 'facebook.views.getAccessToken'),
    (r'^connect$', 'facebook.views.facebookConnect'),
    (r'^notifications_test/([A-Za-z0-9_\.-]+)$', 'facebook.views.sendTestNotification'),
    (r'^getAppAccess/([A-Za-z0-9_\.-]+)$', 'facebook.views.getAppAccessToken'),
    # (r'^updateToken/([A-Za-z0-9_\.-]+)$', 'facebook.views.updateToken'),
    (r'^notification/([A-Za-z0-9_\.-]+)$', 'facebook.views.prepareNotification'),
    (r'^sendNotification/([A-Za-z0-9_\.-]+)$', 'facebook.views.sendNotification'),
)