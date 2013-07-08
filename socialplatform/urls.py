from django.conf.urls import *

urlpatterns = patterns('',
    (r'^getAccessToken$', 'socialplatform.views.getAccessToken'),
    (r'^connect$', 'socialplatform.views.facebookConnect'),
    (r'^notifications_test/([A-Za-z0-9_\.-]+)$', 'socialplatform.views.sendTestNotification'),
    (r'^getAppAccess/([A-Za-z0-9_\.-]+)$', 'socialplatform.views.getAppAccessToken'),
    # (r'^updateToken/([A-Za-z0-9_\.-]+)$', 'socialplatform.views.updateToken'),
    (r'^broadcastNotification/([A-Za-z0-9_\.-]+)$', 'socialplatform.views.access_for_broadcast'),
    (r'^broadcast/([A-Za-z0-9_\.-]+)$', 'socialplatform.views.social_broadcast'),
)