from django.conf.urls.defaults import *
from django.contrib.auth.views import logout
from views import *

urlpatterns = patterns('',
	url(r'register', 'auth.views.register'),
#    url(r'edit',  'auth.views.edit_account', {"post_change_redirect": "campaign.views.home"}),
	url(r'login', 'auth.views.login_func'),
    url(r'account_settings', 'auth.views.account_settings'),
    url(r'change_password', 'auth.views.change_password'),
    url(r'change_email', 'auth.views.change_email'),
#    url(r'forgot_password', 'auth.views.forgot_password'),
    url(r'logout', logout, name="logout"),
    url(r'user/(\d+)', 'auth.views.user_overview'),


#    (r'password/change/$', 'password_change', {'post_change_redirect' : '/accounts/password/done/'}),
#    (r'password/done/$', 'password_change_done'),
#    (r'password/reset/$', "password_reset"),
#    (r'password/reset/confirm/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$','password_reset_confirm'),
)
